from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from domain.dtos.request.saldo import CreateSaldoRequest, UpdateSaldoRequest
from domain.dtos.response.api import ApiResponse, ErrorResponse
from domain.dtos.response.saldo import SaldoResponse
from core.dependencies import get_saldo_service, token_security
from domain.service.saldo import ISaldoService

router = APIRouter()


@router.get("/", response_model=ApiResponse[List[SaldoResponse]])
async def get_saldos(
    token: str = Depends(token_security),
    saldo_service: ISaldoService = Depends(get_saldo_service),
):
    """Retrieve a list of all saldos."""
    try:
        response = await saldo_service.get_saldos()
        if isinstance(response, ErrorResponse):
            raise HTTPException(status_code=500, detail=response.message)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@router.get("/{id}", response_model=ApiResponse[Optional[SaldoResponse]])
async def get_saldo(
    id: int,
    saldo_service: ISaldoService = Depends(get_saldo_service),
    token: str = Depends(token_security),
):
    """Retrieve a single saldo by its ID."""
    try:
        response = await saldo_service.get_saldo(id)
        if isinstance(response, ErrorResponse):
            raise HTTPException(status_code=404, detail=response.message)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@router.get("/user/{user_id}", response_model=ApiResponse[Optional[SaldoResponse]])
async def get_saldo_user(
    user_id: int,
    saldo_service: ISaldoService = Depends(get_saldo_service),
    token: str = Depends(token_security),
):
    """Retrieve a single saldo associated with a specific user ID."""
    try:
        response = await saldo_service.get_saldo_user(user_id)
        if isinstance(response, ErrorResponse):
            raise HTTPException(status_code=404, detail=response.message)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@router.get(
    "/users/{user_id}", response_model=ApiResponse[Optional[List[SaldoResponse]]]
)
async def get_saldo_users(
    user_id: int,
    saldo_service: ISaldoService = Depends(get_saldo_service),
    token: str = Depends(token_security),
):
    """Retrieve all saldos associated with a specific user ID."""
    try:
        response = await saldo_service.get_saldo_users(user_id)
        if isinstance(response, ErrorResponse):
            raise HTTPException(status_code=404, detail=response.message)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@router.post("/", response_model=ApiResponse[SaldoResponse])
async def create_saldo(
    input: CreateSaldoRequest,
    saldo_service: ISaldoService = Depends(get_saldo_service),
    token: str = Depends(token_security),
):
    """Create a new saldo."""
    try:
        response = await saldo_service.create_saldo(input)
        if isinstance(response, ErrorResponse):
            raise HTTPException(status_code=400, detail=response.message)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@router.put("/{id}", response_model=ApiResponse[Optional[SaldoResponse]])
async def update_saldo(
    id: int,
    input: UpdateSaldoRequest,
    saldo_service: ISaldoService = Depends(get_saldo_service),
    token: str = Depends(token_security),
):
    """Update an existing saldo by its ID."""
    try:
        input.id = id  # Ensure the ID in the path matches the request
        response = await saldo_service.update_saldo(input)
        if isinstance(response, ErrorResponse):
            raise HTTPException(status_code=400, detail=response.message)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@router.delete("/{id}", response_model=ApiResponse[None])
async def delete_saldo(
    id: int,
    saldo_service: ISaldoService = Depends(get_saldo_service),
    token: str = Depends(token_security),
):
    """Delete a saldo by its ID."""
    try:
        response = await saldo_service.delete_saldo(id)
        if isinstance(response, ErrorResponse):
            raise HTTPException(status_code=404, detail=response.message)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
