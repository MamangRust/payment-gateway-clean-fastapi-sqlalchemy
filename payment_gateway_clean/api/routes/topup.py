from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from structlog import get_logger
from domain.dtos.request.topup import CreateTopupRequest, UpdateTopupRequest
from domain.dtos.response.api import ApiResponse, ErrorResponse
from domain.dtos.response.topup import TopupResponse
from core.dependencies import get_topup_service, token_security
from domain.service.topup import ITopupService

router = APIRouter()
logger = get_logger()


@router.get("/", response_model=ApiResponse[List[TopupResponse]])
async def get_topups(
    topup_service: ITopupService = Depends(get_topup_service),
    token: str = Depends(token_security)
):
    """Retrieve a list of all topups."""
    logger.info("📦 Fetching all topups")
    try:
        response = await topup_service.get_topups()
        if isinstance(response, ErrorResponse):
            logger.warning("⚠️ Failed to get topups", error=response.message)
            raise HTTPException(status_code=500, detail=response.message)
        logger.info("✅ Topups retrieved successfully")
        return response
    except Exception as e:
        logger.error("🔥 Error while getting topups", error=str(e))
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@router.get("/{id}", response_model=ApiResponse[Optional[TopupResponse]])
async def get_topup(
    id: int,
    topup_service: ITopupService = Depends(get_topup_service),
    token: str = Depends(token_security)
):
    """Retrieve a single topup by its ID."""
    logger.info("🔍 Fetching topup by ID", id=id)
    try:
        response = await topup_service.get_topup(id)
        if isinstance(response, ErrorResponse):
            logger.warning("❌ Topup not found", id=id)
            raise HTTPException(status_code=404, detail=response.message)
        logger.info("✅ Topup retrieved", id=id)
        return response
    except Exception as e:
        logger.error("🔥 Error while getting topup", id=id, error=str(e))
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@router.get("/user/{user_id}", response_model=ApiResponse[Optional[TopupResponse]])
async def get_topup_user(
    user_id: int,
    topup_service: ITopupService = Depends(get_topup_service),
    token: str = Depends(token_security)
):
    """Retrieve a single topup associated with a specific user ID."""
    logger.info("👤 Fetching topup for user", user_id=user_id)
    try:
        response = await topup_service.get_topup_user(user_id)
        if isinstance(response, ErrorResponse):
            logger.warning("❌ Topup for user not found", user_id=user_id)
            raise HTTPException(status_code=404, detail=response.message)
        logger.info("✅ Topup for user retrieved", user_id=user_id)
        return response
    except Exception as e:
        logger.error("🔥 Error while getting topup for user", user_id=user_id, error=str(e))
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@router.get("/users/{user_id}", response_model=ApiResponse[Optional[List[TopupResponse]]])
async def get_topup_users(
    user_id: int,
    topup_service: ITopupService = Depends(get_topup_service),
    token: str = Depends(token_security)
):
    """Retrieve all topups associated with a specific user ID."""
    logger.info("📂 Fetching all topups for user", user_id=user_id)
    try:
        response = await topup_service.get_topup_users(user_id)
        if isinstance(response, ErrorResponse):
            logger.warning("❌ No topups found for user", user_id=user_id)
            raise HTTPException(status_code=404, detail=response.message)
        logger.info("✅ All topups for user retrieved", user_id=user_id)
        return response
    except Exception as e:
        logger.error("🔥 Error while getting topups for user", user_id=user_id, error=str(e))
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@router.post("/", response_model=ApiResponse[TopupResponse])
async def create_topup(
    input: CreateTopupRequest,
    topup_service: ITopupService = Depends(get_topup_service),
    token: str = Depends(token_security)
):
    """Create a new topup."""
    logger.info("📝 Creating new topup", data=input.model_dump())
    try:
        response = await topup_service.create_topup(input)
        if isinstance(response, ErrorResponse):
            logger.warning("❌ Failed to create topup", error=response.message)
            raise HTTPException(status_code=400, detail=response.message)
        logger.info("✅ Topup created successfully")
        return response
    except Exception as e:
        logger.error("🔥 Error while creating topup", error=str(e))
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@router.put("/{id}", response_model=ApiResponse[TopupResponse])
async def update_topup(
    id: int,
    input: UpdateTopupRequest,
    topup_service: ITopupService = Depends(get_topup_service),
    token: str = Depends(token_security)
):
    """Update an existing topup by its ID."""
    input.id = id
    logger.info("✏️ Updating topup", id=id, data=input.model_dump())
    try:
        response = await topup_service.update_topup(input)
        if isinstance(response, ErrorResponse):
            logger.warning("❌ Failed to update topup", id=id, error=response.message)
            raise HTTPException(status_code=400, detail=response.message)
        logger.info("✅ Topup updated", id=id)
        return response
    except Exception as e:
        logger.error("🔥 Error while updating topup", id=id, error=str(e))
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@router.delete("/{id}", response_model=ApiResponse[None])
async def delete_topup(
    id: int,
    topup_service: ITopupService = Depends(get_topup_service),
    token: str = Depends(token_security)
):
    """Delete a topup by its ID."""
    logger.info("🗑️ Deleting topup", id=id)
    try:
        response = await topup_service.delete_topup(id)
        if isinstance(response, ErrorResponse):
            logger.warning("❌ Failed to delete topup", id=id, error=response.message)
            raise HTTPException(status_code=404, detail=response.message)
        logger.info("✅ Topup deleted", id=id)
        return response
    except Exception as e:
        logger.error("🔥 Error while deleting topup", id=id, error=str(e))
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
