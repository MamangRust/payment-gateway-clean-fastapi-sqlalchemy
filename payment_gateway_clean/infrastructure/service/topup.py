from typing import List, Optional, Union
from sqlalchemy.ext.asyncio import AsyncSession
from structlog import get_logger
from domain.repository.user import IUserRepository

from domain.repository.topup import ITopupRepository
from domain.service.topup import ITopupService

from domain.repository.saldo import ISaldoRepository
from domain.service.saldo import ISaldoService

from domain.dtos.request.topup import CreateTopupRequest, UpdateTopupRequest
from domain.dtos.request.saldo import UpdateSaldoBalanceRequest

from domain.dtos.response.api import ApiResponse, ErrorResponse
from core.errors import AppError, NotFoundError
from domain.dtos.response.topup import TopupResponse


logger = get_logger()


class TopupService(ITopupService):
    def __init__(
        self,
        topup_repository: ITopupRepository,
        user_repository: IUserRepository,
        saldo_repository: ISaldoRepository,
    ):
        self.user_repository = user_repository
        self.saldo_repository = saldo_repository
        self.topup_repository = topup_repository

    async def get_topups(
        self,
    ) -> Union[ApiResponse[List[TopupResponse]], ErrorResponse]:

        try:
            # Fetch all topups
            topups = await self.topup_repository.find_all()
            topup_responses = TopupResponse.from_dtos(topups)

            logger.info("Successfully retrieved topups", count=len(topup_responses))

            return ApiResponse(
                status="success",
                message="Topups retrieved successfully",
                data=topup_responses,
            )
        except Exception as e:
            logger.error("Failed to fetch topups", error=str(e))
            return ErrorResponse(
                status="error",
                message="An unexpected error occurred. Please try again later.",
            )

    async def get_topup(
        self, id: int
    ) -> Union[ApiResponse[Optional[TopupResponse]], ErrorResponse]:
        try:
            logger.info("Fetching topup", id=id)

            # Fetch a specific topup by ID
            topup = await self.topup_repository.find_by_id(id)
            if not topup:
                logger.error("Topup not found", id=id)
                raise NotFoundError(f"Topup with id {id} not found")

            logger.info("Successfully retrieved topup", id=id)

            return ApiResponse(
                status="success",
                message="Topup retrieved successfully",
                data=TopupResponse.from_dto(topup),
            )
        except NotFoundError as e:
            return ErrorResponse(status="error", message="Topup not found")
        except Exception as e:
            logger.error("Error fetching topup", id=id, error=str(e))
            return ErrorResponse(
                status="error",
                message="An unexpected error occurred. Please try again later.",
            )

    async def get_topup_users(
        self, user_id: int
    ) -> Union[ApiResponse[Optional[List[TopupResponse]]], ErrorResponse]:
        try:
            user = await self.user_repository.find_by_id(user_id)
            if not user:
                logger.error(f"User with id {user_id} not found")
                raise NotFoundError(f"User with id {user_id} not found")

            topups = await self.topup_repository.find_by_users(user_id)

            if not topups:
                logger.info(f"No topups found for user with id {user_id}")
                return ApiResponse(
                    status="success",
                    message=f"No topups found for user with id {user_id}",
                    data=None,
                )

            topup_response = TopupResponse.from_dtos(topups)
            logger.info(f"Successfully retrieved topups for user with id {user_id}")

            return ApiResponse(
                status="success",
                message="Success",
                data=topup_response,
            )

        except NotFoundError as e:
            return ErrorResponse(status="error", message="Topup or user not found")

        except Exception as e:
            logger.error(f"Failed to fetch topups for user with id {user_id}: {e}")
            return ErrorResponse(
                status="error",
                message="An unexpected error occurred. Please try again later.",
            )

    async def get_topup_user(
        self, user_id: int
    ) -> Union[ApiResponse[Optional[TopupResponse]], ErrorResponse]:
        try:
            user = await self.user_repository.find_by_id(user_id)
            if not user:
                logger.error(f"User with id {user_id} not found")
                raise NotFoundError(f"User with id {user_id} not found")

            topup = await self.topup_repository.find_by_user(user_id)

            if not topup:
                logger.info(f"No topup found for user with id {user_id}")
                raise NotFoundError(f"Topup with user id {user_id} not found")

            topup_response = TopupResponse.from_dto(topup)
            logger.info(f"Successfully retrieved topup for user with id {user_id}")

            return ApiResponse(
                status="success",
                message="Success",
                data=topup_response,
            )

        except NotFoundError as e:
            return ErrorResponse(status="error", message="Topup or user not found")

        except Exception as e:
            logger.error(f"Failed to fetch topup for user with id {user_id}: {e}")
            return ErrorResponse(
                status="error",
                message="An unexpected error occurred. Please try again later.",
            )

    async def create_topup(
        self, input: CreateTopupRequest
    ) -> Union[ApiResponse[TopupResponse], ErrorResponse]:
        try:
            # Check if the user exists
            user = await self.user_repository.find_by_id(input.user_id)
            if not user:
                logger.error(f"User with id {input.user_id} not found")
                raise NotFoundError(f"User with id {input.user_id} not found")

            logger.info(
                f"User with id {input.user_id} found, proceeding with topup creation"
            )

            # Create topup entry
            try:
                topup = await self.topup_repository.create(input)
                logger.info(
                    f"Topup created for user {input.user_id}: topup amount {topup.topup_amount}"
                )
            except Exception as e:
                logger.error(f"Error creating topup for user {input.user_id}: {e}")
                return ErrorResponse(status="error", message="Failed to create topup")

            # Update or create saldo
            saldo = await self.saldo_repository.find_by_user_id(input.user_id)
            try:
                if saldo:
                    new_balance = saldo.total_balance + topup.topup_amount
                    update_request = UpdateSaldoBalanceRequest(
                        user_id=input.user_id, total_balance=new_balance
                    )
                    await self.saldo_repository.update_balance(update_request)
                    logger.info(
                        f"Saldo updated successfully for user {input.user_id}. New balance: {new_balance}"
                    )
                else:
                    create_saldo_request = CreateSaldoRequest(
                        user_id=input.user_id, total_balance=topup.topup_amount
                    )
                    await self.saldo_repository.create(create_saldo_request)
                    logger.info(
                        f"Initial saldo created for user {input.user_id} with balance {topup.topup_amount}"
                    )

            except Exception as db_err:
                logger.error(
                    f"Failed to update/create saldo for user {input.user_id}: {db_err}"
                )
                await self.topup_repository.delete(topup.topup_id)
                return ErrorResponse(
                    status="error",
                    message=f"Failed to update/create saldo for user {input.user_id}",
                )

            logger.info(
                f"Topup successfully created for user {input.user_id}. Total balance updated."
            )
            return ApiResponse(
                status="success",
                message="Topup created successfully",
                data=TopupResponse.from_dto(topup),
            )

        except NotFoundError as e:
            return ErrorResponse(
                status="error",
                message="An error occurred while creating topup. Please try again later.",
            )

        except Exception as e:
            logger.error(f"Error processing topup for user {input.user_id}: {e}")
            return ErrorResponse(
                status="error",
                message="An unexpected error occurred while creating topup",
            )

    async def update_topup(
        self, input: UpdateTopupRequest
    ) -> Union[ApiResponse[Optional[TopupResponse]], ErrorResponse]:
        try:
            logger.info(
                "Input validation passed",
                user_id=input.user_id,
                topup_id=input.topup_id,
            )

            # Verify user existence
            user = await self.user_repository.find_by_id(input.user_id)
            if not user:
                logger.error("User not found", user_id=input.user_id)
                raise NotFoundError(f"User with id {input.user_id} not found")

            logger.info("User found", user_id=input.user_id)

            # Verify topup existence
            existing_topup = await self.topup_repository.find_by_id(input.topup_id)
            if not existing_topup:
                logger.error("Topup not found", topup_id=input.topup_id)
                raise NotFoundError(f"Topup with id {input.topup_id} not found")

            logger.info("Topup found", topup_id=input.topup_id)

            # Calculate topup difference
            topup_difference = input.topup_amount - existing_topup.topup_amount
            logger.info(
                "Calculating topup difference",
                topup_difference=topup_difference,
                new_amount=input.topup_amount,
                old_amount=existing_topup.topup_amount,
            )

            # Update topup amount
            await self.topup_repository.update_amount(
                input=UpdateTopupAmount(
                    topup_id=input.topup_id, topup_amount=input.topup_amount
                )
            )

            # Update saldo
            saldo = await self.saldo_repository.find_by_user_id(input.user_id)
            if not saldo:
                logger.error("Saldo not found", user_id=input.user_id)
                raise NotFoundError(f"Saldo for user {input.user_id} not found")

            new_balance = saldo.total_balance + topup_difference
            saldo_input = UpdateSaldoBalanceRequest(
                user_id=input.user_id, total_balance=new_balance
            )

            await self.saldo_repository.update_balance(saldo_input)

            logger.info("Saldo updated", user_id=input.user_id, new_balance=new_balance)

            # Retrieve updated topup
            updated_topup = await self.topup_repository.find_by_id(input.topup_id)
            if not updated_topup:
                logger.error("Updated topup not found", topup_id=input.topup_id)
                raise NotFoundError(f"Updated topup with id {input.topup_id} not found")

            return ApiResponse(
                status="success",
                message="Topup updated successfully",
                data=TopupResponse.from_dto(updated_topup),
            )

        except AppError as e:
            logger.error("Error during topup update", error=str(e))
            return ErrorResponse(status="error", message="Error during topup update")

        except Exception as e:
            logger.exception("Unexpected error during topup update")
            return ErrorResponse(
                status="error", message="Unexpected error during topup update"
            )

    async def delete_topup(self, id: int) -> Union[ApiResponse[None], ErrorResponse]:
        try:
            # Find user by ID
            user = await self.user_repository.find_by_id(id)
            if not user:
                logger.error(f"User with id {id} not found")
                return ErrorResponse(
                    status="error", message=f"User with id {id} not found"
                )

            # Find topup by user ID
            existing_topup = await self.topup_repository.find_by_user(user.user_id)
            if not existing_topup:
                logger.error(f"Topup with id {id} not found")
                return ErrorResponse(
                    status="error", message=f"Topup with id {id} not found"
                )

            # Delete topup
            await self.topup_repository.delete(existing_topup.topup_id)
            logger.info(f"Topup deleted successfully for id: {id}")

            return ApiResponse[None](
                status="success",
                message="Topup deleted successfully",
                data=None,
            )

        except Exception as e:
            logger.error(f"Failed to delete topup for id {id}: {str(e)}")
            return ErrorResponse(
                status="error", message=f"Failed to delete topup for id {id}"
            )
