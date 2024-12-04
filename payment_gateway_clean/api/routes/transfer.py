from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from domain.dtos.request.transfer import CreateTransferRequest, UpdateTransferRequest
from domain.dtos.response.api import ApiResponse, ErrorResponse
from domain.dtos.response.transfer import TransferResponse
from core.dependencies import get_transfer_service, token_security
from domain.service.transfer import ITransferService

router = APIRouter()


@router.get("/", response_model=ApiResponse[List[TransferResponse]])
async def get_transfers(
    transfer_service: ITransferService = Depends(get_transfer_service),
    token: str = Depends(token_security),
):
    """Retrieve a list of all transfers."""
    try:
        response = await transfer_service.get_transfers()
        if isinstance(response, ErrorResponse):
            raise HTTPException(status_code=500, detail=response.message)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@router.get("/{id}", response_model=ApiResponse[Optional[TransferResponse]])
async def get_transfer(
    id: int,
    transfer_service: ITransferService = Depends(get_transfer_service),
    token: str = Depends(token_security),
):
    """Retrieve a single transfer by its ID."""
    try:
        response = await transfer_service.get_transfer(id)
        if isinstance(response, ErrorResponse):
            raise HTTPException(status_code=404, detail=response.message)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@router.get("/user/{user_id}", response_model=ApiResponse[Optional[TransferResponse]])
async def get_transfer_user(
    user_id: int,
    transfer_service: ITransferService = Depends(get_transfer_service),
    token: str = Depends(token_security),
):
    """Retrieve a single transfer associated with a specific user ID."""
    try:
        response = await transfer_service.get_transfer_user(user_id)
        if isinstance(response, ErrorResponse):
            raise HTTPException(status_code=404, detail=response.message)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@router.get(
    "/users/{user_id}", response_model=ApiResponse[Optional[List[TransferResponse]]]
)
async def get_transfer_users(
    user_id: int,
    transfer_service: ITransferService = Depends(get_transfer_service),
    token: str = Depends(token_security),
):
    """Retrieve all transfers associated with a specific user ID."""
    try:
        response = await transfer_service.get_transfer_users(user_id)
        if isinstance(response, ErrorResponse):
            raise HTTPException(status_code=404, detail=response.message)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@router.post("/", response_model=ApiResponse[TransferResponse])
async def create_transfer(
    input: CreateTransferRequest,
    transfer_service: ITransferService = Depends(get_transfer_service),
    token: str = Depends(token_security),
):
    """Create a new transfer."""
    try:
        response = await transfer_service.create_transfer(input)
        if isinstance(response, ErrorResponse):
            raise HTTPException(status_code=400, detail=response.message)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@router.put("/{id}", response_model=ApiResponse[TransferResponse])
async def update_transfer(
    id: int,
    input: UpdateTransferRequest,
    transfer_service: ITransferService = Depends(get_transfer_service),
    token: str = Depends(token_security),
):
    """Update an existing transfer by its ID."""
    try:
        input.id = id  # Ensure the ID in the path matches the request
        response = await transfer_service.update_transfer(input)
        if isinstance(response, ErrorResponse):
            raise HTTPException(status_code=400, detail=response.message)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@router.delete("/{id}", response_model=ApiResponse[None])
async def delete_transfer(
    id: int,
    transfer_service: ITransferService = Depends(get_transfer_service),
    token: str = Depends(token_security),
):
    """Delete a transfer by its ID."""
    try:
        response = await transfer_service.delete_transfer(id)
        if isinstance(response, ErrorResponse):
            raise HTTPException(status_code=404, detail=response.message)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
