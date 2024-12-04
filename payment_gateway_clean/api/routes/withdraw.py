from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from domain.dtos.request.withdraw import CreateWithdrawRequest, UpdateWithdrawRequest
from domain.dtos.response.api import ApiResponse, ErrorResponse
from domain.dtos.response.withdraw import WithdrawResponse
from core.dependencies import get_withdraw_service, token_security
from domain.service.withdraw import IWithdrawService

router = APIRouter()


@router.get("/", response_model=ApiResponse[List[WithdrawResponse]])
async def get_withdraws(
    withdraw_service: IWithdrawService = Depends(get_withdraw_service),
    token: str = Depends(token_security),
):
    """Retrieve a list of all withdrawal records."""
    try:
        response = await withdraw_service.get_withdraws()
        if isinstance(response, ErrorResponse):
            raise HTTPException(status_code=500, detail=response.message)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@router.get("/{id}", response_model=ApiResponse[Optional[WithdrawResponse]])
async def get_withdraw(
    id: int,
    withdraw_service: IWithdrawService = Depends(get_withdraw_service),
    token: str = Depends(token_security),
):
    """Retrieve a specific withdrawal record by its ID."""
    try:
        response = await withdraw_service.get_withdraw(id)
        if isinstance(response, ErrorResponse):
            raise HTTPException(status_code=404, detail=response.message)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@router.get("/user/{user_id}", response_model=ApiResponse[Optional[WithdrawResponse]])
async def get_withdraw_user(
    user_id: int,
    withdraw_service: IWithdrawService = Depends(get_withdraw_service),
    token: str = Depends(token_security),
):
    """Retrieve a specific withdrawal record for a user by user ID."""
    try:
        response = await withdraw_service.get_withdraw_user(user_id)
        if isinstance(response, ErrorResponse):
            raise HTTPException(status_code=404, detail=response.message)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@router.get(
    "/users/{user_id}", response_model=ApiResponse[Optional[List[WithdrawResponse]]]
)
async def get_withdraw_users(
    user_id: int,
    withdraw_service: IWithdrawService = Depends(get_withdraw_service),
    token: str = Depends(token_security),
):
    """Retrieve all withdrawal records associated with a specific user ID."""
    try:
        response = await withdraw_service.get_withdraw_users(user_id)
        if isinstance(response, ErrorResponse):
            raise HTTPException(status_code=404, detail=response.message)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@router.post("/", response_model=ApiResponse[WithdrawResponse])
async def create_withdraw(
    input: CreateWithdrawRequest,
    withdraw_service: IWithdrawService = Depends(get_withdraw_service),
    token: str = Depends(token_security),
):
    """Create a new withdrawal record."""
    try:
        response = await withdraw_service.create_withdraw(input)
        if isinstance(response, ErrorResponse):
            raise HTTPException(status_code=400, detail=response.message)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@router.put("/{id}", response_model=ApiResponse[Optional[WithdrawResponse]])
async def update_withdraw(
    id: int,
    input: UpdateWithdrawRequest,
    withdraw_service: IWithdrawService = Depends(get_withdraw_service),
    token: str = Depends(token_security),
):
    """Update an existing withdrawal record."""
    try:
        input.id = id  # Ensure the ID in the path matches the request
        response = await withdraw_service.update_withdraw(input)
        if isinstance(response, ErrorResponse):
            raise HTTPException(status_code=400, detail=response.message)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@router.delete("/{id}", response_model=ApiResponse[None])
async def delete_withdraw(
    id: int,
    withdraw_service: IWithdrawService = Depends(get_withdraw_service),
    token: str = Depends(token_security),
):
    """Delete a withdrawal record by its ID."""
    try:
        response = await withdraw_service.delete_withdraw(id)
        if isinstance(response, ErrorResponse):
            raise HTTPException(status_code=404, detail=response.message)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
