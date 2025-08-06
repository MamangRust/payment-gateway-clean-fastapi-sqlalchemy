from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from structlog import get_logger
from domain.dtos.request.transfer import CreateTransferRequest, UpdateTransferRequest
from domain.dtos.response.api import ApiResponse, ErrorResponse
from domain.dtos.response.transfer import TransferResponse
from core.dependencies import get_transfer_service, token_security
from domain.service.transfer import ITransferService

router = APIRouter()
logger = get_logger()


@router.get("/", response_model=ApiResponse[List[TransferResponse]])
async def get_transfers(
    transfer_service: ITransferService = Depends(get_transfer_service),
    token: str = Depends(token_security),
):
    """Retrieve a list of all transfers."""
    logger.info("📦 Fetching all transfers")
    try:
        response = await transfer_service.get_transfers()
        if isinstance(response, ErrorResponse):
            logger.warning("⚠️ Failed to get transfers", error=response.message)
            raise HTTPException(status_code=500, detail=response.message)
        logger.info("✅ Transfers retrieved successfully")
        return response
    except Exception as e:
        logger.error("🔥 Error while getting transfers", error=str(e))
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@router.get("/{id}", response_model=ApiResponse[Optional[TransferResponse]])
async def get_transfer(
    id: int,
    transfer_service: ITransferService = Depends(get_transfer_service),
    token: str = Depends(token_security),
):
    """Retrieve a single transfer by its ID."""
    logger.info("🔍 Fetching transfer by ID", id=id)
    try:
        response = await transfer_service.get_transfer(id)
        if isinstance(response, ErrorResponse):
            logger.warning("❌ Transfer not found", id=id)
            raise HTTPException(status_code=404, detail=response.message)
        logger.info("✅ Transfer retrieved", id=id)
        return response
    except Exception as e:
        logger.error("🔥 Error while getting transfer", id=id, error=str(e))
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@router.get("/user/{user_id}", response_model=ApiResponse[Optional[TransferResponse]])
async def get_transfer_user(
    user_id: int,
    transfer_service: ITransferService = Depends(get_transfer_service),
    token: str = Depends(token_security),
):
    """Retrieve a single transfer associated with a specific user ID."""
    logger.info("👤 Fetching transfer for user", user_id=user_id)
    try:
        response = await transfer_service.get_transfer_user(user_id)
        if isinstance(response, ErrorResponse):
            logger.warning("❌ Transfer for user not found", user_id=user_id)
            raise HTTPException(status_code=404, detail=response.message)
        logger.info("✅ Transfer for user retrieved", user_id=user_id)
        return response
    except Exception as e:
        logger.error("🔥 Error while getting transfer for user", user_id=user_id, error=str(e))
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@router.get("/users/{user_id}", response_model=ApiResponse[Optional[List[TransferResponse]]])
async def get_transfer_users(
    user_id: int,
    transfer_service: ITransferService = Depends(get_transfer_service),
    token: str = Depends(token_security),
):
    """Retrieve all transfers associated with a specific user ID."""
    logger.info("📂 Fetching all transfers for user", user_id=user_id)
    try:
        response = await transfer_service.get_transfer_users(user_id)
        if isinstance(response, ErrorResponse):
            logger.warning("❌ No transfers found for user", user_id=user_id)
            raise HTTPException(status_code=404, detail=response.message)
        logger.info("✅ All transfers for user retrieved", user_id=user_id)
        return response
    except Exception as e:
        logger.error("🔥 Error while getting transfers for user", user_id=user_id, error=str(e))
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@router.post("/", response_model=ApiResponse[TransferResponse])
async def create_transfer(
    input: CreateTransferRequest,
    transfer_service: ITransferService = Depends(get_transfer_service),
    token: str = Depends(token_security),
):
    """Create a new transfer."""
    logger.info("📝 Creating new transfer", data=input.model_dump())
    try:
        response = await transfer_service.create_transfer(input)
        if isinstance(response, ErrorResponse):
            logger.warning("❌ Failed to create transfer", error=response.message)
            raise HTTPException(status_code=400, detail=response.message)
        logger.info("✅ Transfer created successfully")
        return response
    except Exception as e:
        logger.error("🔥 Error while creating transfer", error=str(e))
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@router.put("/{id}", response_model=ApiResponse[TransferResponse])
async def update_transfer(
    id: int,
    input: UpdateTransferRequest,
    transfer_service: ITransferService = Depends(get_transfer_service),
    token: str = Depends(token_security),
):
    """Update an existing transfer by its ID."""
    input.id = id
    logger.info("✏️ Updating transfer", id=id, data=input.model_dump())
    try:
        response = await transfer_service.update_transfer(input)
        if isinstance(response, ErrorResponse):
            logger.warning("❌ Failed to update transfer", id=id, error=response.message)
            raise HTTPException(status_code=400, detail=response.message)
        logger.info("✅ Transfer updated", id=id)
        return response
    except Exception as e:
        logger.error("🔥 Error while updating transfer", id=id, error=str(e))
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@router.delete("/{id}", response_model=ApiResponse[None])
async def delete_transfer(
    id: int,
    transfer_service: ITransferService = Depends(get_transfer_service),
    token: str = Depends(token_security),
):
    """Delete a transfer by its ID."""
    logger.info("🗑️ Deleting transfer", id=id)
    try:
        response = await transfer_service.delete_transfer(id)
        if isinstance(response, ErrorResponse):
            logger.warning("❌ Failed to delete transfer", id=id, error=response.message)
            raise HTTPException(status_code=404, detail=response.message)
        logger.info("✅ Transfer deleted", id=id)
        return response
    except Exception as e:
        logger.error("🔥 Error while deleting transfer", id=id, error=str(e))
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
