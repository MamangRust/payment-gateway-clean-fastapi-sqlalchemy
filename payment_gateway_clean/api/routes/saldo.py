from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from structlog import get_logger
from domain.dtos.request.saldo import CreateSaldoRequest, UpdateSaldoRequest
from domain.dtos.response.api import ApiResponse, ErrorResponse
from domain.dtos.response.saldo import SaldoResponse
from core.dependencies import get_saldo_service, token_security
from domain.service.saldo import ISaldoService

router = APIRouter()
logger = get_logger()


@router.get("/", response_model=ApiResponse[List[SaldoResponse]])
async def get_saldos(
    token: str = Depends(token_security),
    saldo_service: ISaldoService = Depends(get_saldo_service),
):
    """Retrieve a list of all saldos."""
    logger.info("📦 Fetching all saldos")
    try:
        response = await saldo_service.get_saldos()
        if isinstance(response, ErrorResponse):
            logger.warning("⚠️ Failed to get saldos", error=response.message)
            raise HTTPException(status_code=500, detail=response.message)
        logger.info("✅ Saldos retrieved successfully")
        return response
    except Exception as e:
        logger.error("🔥 Error while getting saldos", error=str(e))
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@router.get("/{id}", response_model=ApiResponse[Optional[SaldoResponse]])
async def get_saldo(
    id: int,
    saldo_service: ISaldoService = Depends(get_saldo_service),
    token: str = Depends(token_security),
):
    """Retrieve a single saldo by its ID."""
    logger.info("🔍 Fetching saldo by ID", id=id)
    try:
        response = await saldo_service.get_saldo(id)
        if isinstance(response, ErrorResponse):
            logger.warning("❌ Saldo not found", id=id)
            raise HTTPException(status_code=404, detail=response.message)
        logger.info("✅ Saldo retrieved", id=id)
        return response
    except Exception as e:
        logger.error("🔥 Error while getting saldo by ID", id=id, error=str(e))
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@router.get("/user/{user_id}", response_model=ApiResponse[Optional[SaldoResponse]])
async def get_saldo_user(
    user_id: int,
    saldo_service: ISaldoService = Depends(get_saldo_service),
    token: str = Depends(token_security),
):
    """Retrieve a single saldo associated with a specific user ID."""
    logger.info("🔎 Fetching saldo for user", user_id=user_id)
    try:
        response = await saldo_service.get_saldo_user(user_id)
        if isinstance(response, ErrorResponse):
            logger.warning("❌ Saldo not found for user", user_id=user_id)
            raise HTTPException(status_code=404, detail=response.message)
        logger.info("✅ Saldo for user retrieved", user_id=user_id)
        return response
    except Exception as e:
        logger.error("🔥 Error while getting saldo for user", user_id=user_id, error=str(e))
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@router.get("/users/{user_id}", response_model=ApiResponse[Optional[List[SaldoResponse]]])
async def get_saldo_users(
    user_id: int,
    saldo_service: ISaldoService = Depends(get_saldo_service),
    token: str = Depends(token_security),
):
    """Retrieve all saldos associated with a specific user ID."""
    logger.info("📂 Fetching all saldos for user", user_id=user_id)
    try:
        response = await saldo_service.get_saldo_users(user_id)
        if isinstance(response, ErrorResponse):
            logger.warning("❌ No saldos found for user", user_id=user_id)
            raise HTTPException(status_code=404, detail=response.message)
        logger.info("✅ All saldos for user retrieved", user_id=user_id)
        return response
    except Exception as e:
        logger.error("🔥 Error while getting saldos for user", user_id=user_id, error=str(e))
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@router.post("/", response_model=ApiResponse[SaldoResponse])
async def create_saldo(
    input: CreateSaldoRequest,
    saldo_service: ISaldoService = Depends(get_saldo_service),
    token: str = Depends(token_security),
):
    """Create a new saldo."""
    logger.info("📝 Creating new saldo", data=input.model_dump())
    try:
        response = await saldo_service.create_saldo(input)
        if isinstance(response, ErrorResponse):
            logger.warning("❌ Failed to create saldo", error=response.message)
            raise HTTPException(status_code=400, detail=response.message)
        logger.info("✅ Saldo created successfully", id=response.data.id if hasattr(response, "data") else None)
        return response
    except Exception as e:
        logger.error("🔥 Error while creating saldo", error=str(e))
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@router.put("/{id}", response_model=ApiResponse[Optional[SaldoResponse]])
async def update_saldo(
    id: int,
    input: UpdateSaldoRequest,
    saldo_service: ISaldoService = Depends(get_saldo_service),
    token: str = Depends(token_security),
):
    """Update an existing saldo by its ID."""
    input.id = id
    logger.info("✏️ Updating saldo", id=id, data=input.model_dump())
    try:
        response = await saldo_service.update_saldo(input)
        if isinstance(response, ErrorResponse):
            logger.warning("❌ Failed to update saldo", id=id, error=response.message)
            raise HTTPException(status_code=400, detail=response.message)
        logger.info("✅ Saldo updated", id=id)
        return response
    except Exception as e:
        logger.error("🔥 Error while updating saldo", id=id, error=str(e))
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@router.delete("/{id}", response_model=ApiResponse[None])
async def delete_saldo(
    id: int,
    saldo_service: ISaldoService = Depends(get_saldo_service),
    token: str = Depends(token_security),
):
    """Delete a saldo by its ID."""
    logger.info("🗑️ Deleting saldo", id=id)
    try:
        response = await saldo_service.delete_saldo(id)
        if isinstance(response, ErrorResponse):
            logger.warning("❌ Failed to delete saldo", id=id, error=response.message)
            raise HTTPException(status_code=404, detail=response.message)
        logger.info("✅ Saldo deleted", id=id)
        return response
    except Exception as e:
        logger.error("🔥 Error while deleting saldo", id=id, error=str(e))
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
