from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from domain.dtos.request.topup import CreateTopupRequest, UpdateTopupRequest
from domain.dtos.response.api import ApiResponse, ErrorResponse
from domain.dtos.response.topup import TopupResponse
from core.dependencies import get_topup_service
from domain.service.topup import ITopupService

router = APIRouter()


@router.get("/", response_model=ApiResponse[List[TopupResponse]])
async def get_topups(topup_service: ITopupService = Depends(get_topup_service)):
    """Retrieve a list of all topups."""
    try:
        response = await topup_service.get_topups()
        if isinstance(response, ErrorResponse):
            raise HTTPException(status_code=500, detail=response.message)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@router.get("/{id}", response_model=ApiResponse[Optional[TopupResponse]])
async def get_topup(id: int, topup_service: ITopupService = Depends(get_topup_service)):
    """Retrieve a single topup by its ID."""
    try:
        response = await topup_service.get_topup(id)
        if isinstance(response, ErrorResponse):
            raise HTTPException(status_code=404, detail=response.message)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@router.get("/user/{user_id}", response_model=ApiResponse[Optional[TopupResponse]])
async def get_topup_user(
    user_id: int, topup_service: ITopupService = Depends(get_topup_service)
):
    """Retrieve a single topup associated with a specific user ID."""
    try:
        response = await topup_service.get_topup_user(user_id)
        if isinstance(response, ErrorResponse):
            raise HTTPException(status_code=404, detail=response.message)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@router.get("/users/{user_id}", response_model=ApiResponse[Optional[List[TopupResponse]]])
async def get_topup_users(
    user_id: int, topup_service: ITopupService = Depends(get_topup_service)
):
    """Retrieve all topups associated with a specific user ID."""
    try:
        response = await topup_service.get_topup_users(user_id)
        if isinstance(response, ErrorResponse):
            raise HTTPException(status_code=404, detail=response.message)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@router.post("/", response_model=ApiResponse[TopupResponse])
async def create_topup(
    input: CreateTopupRequest, topup_service: ITopupService = Depends(get_topup_service)
):
    """Create a new topup."""
    try:
        response = await topup_service.create_topup(input)
        if isinstance(response, ErrorResponse):
            raise HTTPException(status_code=400, detail=response.message)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@router.put("/{id}", response_model=ApiResponse[TopupResponse])
async def update_topup(
    id: int,
    input: UpdateTopupRequest,
    topup_service: ITopupService = Depends(get_topup_service),
):
    """Update an existing topup by its ID."""
    try:
        input.id = id  # Ensure the ID in the path matches the request
        response = await topup_service.update_topup(input)
        if isinstance(response, ErrorResponse):
            raise HTTPException(status_code=400, detail=response.message)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@router.delete("/{id}", response_model=ApiResponse[None])
async def delete_topup(id: int, topup_service: ITopupService = Depends(get_topup_service)):
    """Delete a topup by its ID."""
    try:
        response = await topup_service.delete_topup(id)
        if isinstance(response, ErrorResponse):
            raise HTTPException(status_code=404, detail=response.message)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
