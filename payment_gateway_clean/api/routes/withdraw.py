from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from structlog import get_logger
from domain.dtos.request.withdraw import CreateWithdrawRequest, UpdateWithdrawRequest
from domain.dtos.response.api import ApiResponse, ErrorResponse
from domain.dtos.response.withdraw import WithdrawResponse
from core.dependencies import get_withdraw_service, token_security
from domain.service.withdraw import IWithdrawService

router = APIRouter()
logger = get_logger()


@router.get("/", response_model=ApiResponse[List[WithdrawResponse]])
async def get_withdraws(
    withdraw_service: IWithdrawService = Depends(get_withdraw_service),
    token: str = Depends(token_security),
):
    """Retrieve a list of all withdrawal records."""
    logger.info("📄 Fetching all withdrawals")
    try:
        response = await withdraw_service.get_withdraws()
        if isinstance(response, ErrorResponse):
            logger.warning("⚠️ Failed to fetch withdrawals", error=response.message)
            raise HTTPException(status_code=500, detail=response.message)
        logger.info("✅ Withdrawals fetched successfully")
        return response
    except Exception as e:
        logger.error("🔥 Error fetching withdrawals", error=str(e))
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@router.get("/{id}", response_model=ApiResponse[Optional[WithdrawResponse]])
async def get_withdraw(
    id: int,
    withdraw_service: IWithdrawService = Depends(get_withdraw_service),
    token: str = Depends(token_security),
):
    """Retrieve a specific withdrawal record by its ID."""
    logger.info("🔍 Fetching withdrawal by ID", id=id)
    try:
        response = await withdraw_service.get_withdraw(id)
        if isinstance(response, ErrorResponse):
            logger.warning("❌ Withdrawal not found", id=id)
            raise HTTPException(status_code=404, detail=response.message)
        logger.info("✅ Withdrawal found", id=id)
        return response
    except Exception as e:
        logger.error("🔥 Error fetching withdrawal", id=id, error=str(e))
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@router.get("/user/{user_id}", response_model=ApiResponse[Optional[WithdrawResponse]])
async def get_withdraw_user(
    user_id: int,
    withdraw_service: IWithdrawService = Depends(get_withdraw_service),
    token: str = Depends(token_security),
):
    """Retrieve a specific withdrawal record for a user by user ID."""
    logger.info("👤 Fetching withdrawal for user", user_id=user_id)
    try:
        response = await withdraw_service.get_withdraw_user(user_id)
        if isinstance(response, ErrorResponse):
            logger.warning("❌ User withdrawal not found", user_id=user_id)
            raise HTTPException(status_code=404, detail=response.message)
        logger.info("✅ User withdrawal found", user_id=user_id)
        return response
    except Exception as e:
        logger.error("🔥 Error fetching user withdrawal", user_id=user_id, error=str(e))
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@router.get("/users/{user_id}", response_model=ApiResponse[Optional[List[WithdrawResponse]]])
async def get_withdraw_users(
    user_id: int,
    withdraw_service: IWithdrawService = Depends(get_withdraw_service),
    token: str = Depends(token_security),
):
    """Retrieve all withdrawal records associated with a specific user ID."""
    logger.info("👥 Fetching all withdrawals for user", user_id=user_id)
    try:
        response = await withdraw_service.get_withdraw_users(user_id)
        if isinstance(response, ErrorResponse):
            logger.warning("❌ Withdrawals not found for user", user_id=user_id)
            raise HTTPException(status_code=404, detail=response.message)
        logger.info("✅ User withdrawals fetched", user_id=user_id)
        return response
    except Exception as e:
        logger.error("🔥 Error fetching withdrawals by user", user_id=user_id, error=str(e))
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@router.post("/", response_model=ApiResponse[WithdrawResponse])
async def create_withdraw(
    input: CreateWithdrawRequest,
    withdraw_service: IWithdrawService = Depends(get_withdraw_service),
    token: str = Depends(token_security),
):
    """Create a new withdrawal record."""
    logger.info("✍️ Creating withdrawal", payload=input.model_dump())
    try:
        response = await withdraw_service.create_withdraw(input)
        if isinstance(response, ErrorResponse):
            logger.warning("❌ Failed to create withdrawal", error=response.message)
            raise HTTPException(status_code=400, detail=response.message)
        logger.info("✅ Withdrawal created successfully")
        return response
    except Exception as e:
        logger.error("🔥 Error creating withdrawal", error=str(e))
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@router.put("/{id}", response_model=ApiResponse[Optional[WithdrawResponse]])
async def update_withdraw(
    id: int,
    input: UpdateWithdrawRequest,
    withdraw_service: IWithdrawService = Depends(get_withdraw_service),
    token: str = Depends(token_security),
):
    """Update an existing withdrawal record."""
    input.id = id
    logger.info("✏️ Updating withdrawal", id=id, payload=input.model_dump())
    try:
        response = await withdraw_service.update_withdraw(input)
        if isinstance(response, ErrorResponse):
            logger.warning("❌ Failed to update withdrawal", id=id, error=response.message)
            raise HTTPException(status_code=400, detail=response.message)
        logger.info("✅ Withdrawal updated successfully", id=id)
        return response
    except Exception as e:
        logger.error("🔥 Error updating withdrawal", id=id, error=str(e))
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@router.delete("/{id}", response_model=ApiResponse[None])
async def delete_withdraw(
    id: int,
    withdraw_service: IWithdrawService = Depends(get_withdraw_service),
    token: str = Depends(token_security),
):
    """Delete a withdrawal record by its ID."""
    logger.info("🗑️ Deleting withdrawal", id=id)
    try:
        response = await withdraw_service.delete_withdraw(id)
        if isinstance(response, ErrorResponse):
            logger.warning("❌ Failed to delete withdrawal", id=id, error=response.message)
            raise HTTPException(status_code=404, detail=response.message)
        logger.info("✅ Withdrawal deleted", id=id)
        return response
    except Exception as e:
        logger.error("🔥 Error deleting withdrawal", id=id, error=str(e))
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
