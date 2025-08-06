from typing import List, Optional, Union
from sqlalchemy.ext.asyncio import AsyncSession
from structlog import get_logger

from domain.repository.user import IUserRepository
from domain.repository.withdraw import IWithdrawRepository
from domain.service.withdraw import IWithdrawService
from domain.repository.saldo import ISaldoRepository
from domain.service.saldo import ISaldoService
from domain.dtos.request.withdraw import CreateWithdrawRequest, UpdateWithdrawRequest
from domain.dtos.request.saldo import UpdateSaldoBalanceRequest
from domain.dtos.response.api import ApiResponse, ErrorResponse
from domain.dtos.response.withdraw import WithdrawResponse

from core.errors import AppError, NotFoundError, ValidationError


logger = get_logger()


class WithdrawService(IWithdrawService):
    def __init__(
        self,
        withdraw_repository: IWithdrawRepository,
        user_repository: IUserRepository,
        saldo_repository: ISaldoRepository,
    ):
        self.user_repository = user_repository
        self.saldo_repository = saldo_repository
        self.withdraw_repository = withdraw_repository

    async def get_withdraws(
        self,
    ) -> Union[ApiResponse[List[WithdrawResponse]], ErrorResponse]:
        try:
            withdraws = await self.withdraw_repository.find_all()
            withdraw_responses = WithdrawResponse.from_dtos(withdraws)

            logger.info(f"Successfully fetched {len(withdraw_responses)} withdrawals.")
            return ApiResponse(
                status="success",
                message="Withdrawals retrieved successfully.",
                data=withdraw_responses,
            )
        except Exception as e:
            logger.error(f"Failed to fetch withdrawals: {str(e)}")
            return ErrorResponse(
                status="error",
                message="An unexpected error occurred. Please try again later.",
            )

    async def get_withdraw(
        self, id: int
    ) -> Union[ApiResponse[Optional[WithdrawResponse]], ErrorResponse]:
        try:
            withdraw = await self.withdraw_repository.find_by_id(id)

            if withdraw:
                logger.info(f"Successfully retrieved withdrawal with ID: {id}.")
                return ApiResponse(
                    status="success",
                    message="Withdrawal retrieved successfully.",
                    data=WithdrawResponse.from_dto(withdraw),
                )
            else:
                logger.error(f"Withdrawal with ID {id} not found.")
                raise NotFoundError(f"Withdrawal with ID {id} not found.")
        except Exception as e:
            logger.error(f"Failed to retrieve withdrawal with ID {id}: {str(e)}")
            return ErrorResponse(
                status="error",
                message="An unexpected error occurred. Please try again later.",
            )

    async def get_withdraw_users(
        self, user_id: int
    ) -> Union[ApiResponse[Optional[List[WithdrawResponse]]], ErrorResponse]:
        try:
            user = await self.user_repository.find_by_id(user_id)
            if not user:
                logger.error(f"User with ID {user_id} not found.")
                return NotFoundError(f"User with ID {user_id} not found.")

            withdrawals = await self.withdraw_repository.find_by_users(user_id)

            if not withdrawals:
                logger.info(f"No withdrawals found for user with ID {user_id}.")
                return ApiResponse(
                    status="success",
                    message=f"No withdrawals found for user with ID {user_id}.",
                    data=None,
                )

            withdrawal_responses = WithdrawResponse.from_dtos(withdrawals)

            logger.info(
                f"Successfully retrieved withdrawals for user with ID {user_id}."
            )
            return ApiResponse(
                status="success",
                message="Withdrawals retrieved successfully.",
                data=withdrawal_responses,
            )
        except Exception as e:
            logger.error(
                f"Failed to retrieve withdrawals for user with ID {user_id}: {str(e)}"
            )
            return ErrorResponse(
                status="error",
                message="An unexpected error occurred. Please try again later.",
            )

    async def get_withdraw_user(
        self, user_id: int
    ) -> Union[ApiResponse[Optional[WithdrawResponse]], ErrorResponse]:
        try:
            user = await self.user_repository.find_by_id(user_id)
            if not user:
                logger.error(f"User with ID {user_id} not found.")
                raise NotFoundError(f"User with ID {user_id} not found.")

            withdrawal = await self.withdraw_repository.find_by_user(user_id)
            if not withdrawal:
                logger.info(f"No withdrawal found for user with ID {user_id}.")
                raise NotFoundError(f"Withdrawal for user with ID {user_id} not found.")

            withdrawal_response = WithdrawResponse.from_dto(withdrawal)
            logger.info(
                f"Successfully retrieved withdrawal for user with ID {user_id}."
            )

            return ApiResponse(
                status="success",
                message="Withdrawal retrieved successfully.",
                data=withdrawal_response,
            )
        except Exception as e:
            logger.error(
                f"Failed to retrieve withdrawal for user with ID {user_id}: {str(e)}"
            )
            return ErrorResponse(
                status="error",
                message=f"Failed to retrieve withdrawal for user with ID {user_id}",
            )

    async def create_withdraw(
        self, input: CreateWithdrawRequest
    ) -> Union[ApiResponse[WithdrawResponse], ErrorResponse]:
        try:
            logger.info(f"Creating withdraw for user_id: {input.user_id}")

            saldo = await self.saldo_repository.find_by_user_id(input.user_id)
            if not saldo:
                logger.error(f"Saldo with user_id {input.user_id} not found")
                raise NotFoundError(f"Saldo with user_id {input.user_id} not found")

            if saldo.total_balance < input.withdraw_amount:
                logger.error(
                    f"Insufficient balance for user_id {input.user_id}. "
                    f"Attempted withdrawal: {input.withdraw_amount}"
                )
                raise ValidationError("Insufficient balance")

            logger.info("User has sufficient balance for withdrawal")

            new_total_balance = saldo.total_balance - input.withdraw_amount

            try:
                await self.saldo_repository.update_saldo_withdraw(
                    input=UpdateSaldoWithdraw(
                        user_id=input.user_id,
                        withdraw_amount=input.withdraw_amount,
                        withdraw_time=datetime.utcnow(),
                        total_balance=new_total_balance,
                    )
                )
                logger.info(
                    f"Saldo balance updated for user_id {input.user_id}. "
                    f"New balance: {new_total_balance}"
                )
            except Exception as e:
                logger.error(f"Failed to update saldo balance: {e}")
                return ErrorResponse(
                    status="error", message=f"Failed to update saldo balance: {e}"
                )

            try:
                withdraw_record = await self.withdraw_repository.create(input)

                logger.info(
                    f"Withdraw created successfully for user_id {input.user_id}"
                )

                return ApiResponse(
                    status="success",
                    message="Withdraw created successfully",
                    data=WithdrawResponse.from_dto(withdraw_record),
                )
            except Exception as e:
                logger.error(f"Failed to create withdraw: {e}")
                return ErrorResponse(
                    status="error", message=f"Failed to create withdraw: {e}"
                )
        except Exception as e:
            logger.error(
                f"Unexpected error while creating withdraw for user_id {input.user_id}: {str(e)}"
            )
            return ErrorResponse(
                status="error",
                message="An unexpected error occurred. Please try again later.",
            )

    async def update_withdraw(
        self, input: UpdateWithdrawRequest
    ) -> Union[ApiResponse[Optional[WithdrawResponse]], ErrorResponse]:

        try:
            withdraw_record = await self.withdraw_repository.find_by_id(
                input.withdraw_id
            )
            if not withdraw_record:
                logger.error(f"Withdraw with id {input.withdraw_id} not found")
                raise NotFoundError(f"Withdraw with id {input.withdraw_id} not found")

            saldo = await self.saldo_repository.find_by_user_id(input.user_id)

            if not saldo:
                logger.error(f"Saldo with user_id {input.user_id} not found")
                raise NotFoundError(f"Saldo with user_id {input.user_id} not found")

            new_total_balance = saldo.total_balance - input.withdraw_amount

            if new_total_balance < 0:
                logger.error(
                    f"Insufficient balance for user_id {input.user_id}. "
                    f"Attempted withdrawal: {input.withdraw_amount}"
                )
                raise ValidationError("Insufficient balance")

            try:
                updated_withdraw = await self.withdraw_repository.update(input)
            except Exception as e:
                await self.saldo_repository.update_balance(
                    input=UpdateSaldoBalanceRequest(
                        user_id=input.user_id,
                        total_balance=saldo.total_balance,
                    )
                )
                logger.error(
                    f"Rollback: Saldo reverted due to withdraw update failure: {e}"
                )
                return ErrorResponse(
                    status="error",
                    message=f"Rollback: Saldo reverted due to withdraw update failure",
                )

            try:
                await self.saldo_repository.update_saldo_withdraw(
                    input=UpdateSaldoWithdraw(
                        user_id=input.user_id,
                        withdraw_amount=input.withdraw_amount,
                        withdraw_time=datetime.utcnow(),
                        total_balance=new_total_balance,
                    )
                )
            except Exception as e:
                logger.error(
                    f"Failed to update saldo balance after withdrawal update: {e}"
                )
                return ErrorResponse(
                    status="error",
                    message=f"Failed to update saldo balance after withdrawal update",
                )

            logger.info(
                f"Withdraw updated successfully for withdraw_id {input.withdraw_id}"
            )

            return ApiResponse(
                status="success",
                message="Withdraw updated successfully",
                data=WithdrawResponse.from_dto(updated_withdraw),
            )
        except Exception as e:
            logger.error(
                f"Unexpected error while updating withdraw for withdraw_id {input.withdraw_id}: {str(e)}"
            )
            return ErrorResponse(
                status="error",
                message=f"Failed to update withdraw for withdraw_id {input.withdraw_id}",
            )

    async def delete_withdraw(self, id: int) -> Union[ApiResponse[None], ErrorResponse]:
        try:
            existing_withdraw = await self.withdraw_repository.find_by_id(id)

            if not existing_withdraw:
                logger.error(f"Withdraw with id {id} not found")
                raise NotFoundError(f"Withdraw with id {id} not found")

            try:
                await self.withdraw_repository.delete(id)
                logger.info(f"Withdraw deleted successfully for id: {id}")
            except Exception as e:
                logger.error(f"Error deleting withdraw with id {id}: {e}")
                return ErrorResponse(
                    status="error", message=f"Error deleting withdraw with id {id}"
                )

            return ApiResponse(
                status="success",
                message="Withdraw deleted successfully",
                data=None,
            )
        except Exception as e:
            return ErrorResponse(
                status="error", message=f"Failed to delete withdraw with id {id}"
            )
