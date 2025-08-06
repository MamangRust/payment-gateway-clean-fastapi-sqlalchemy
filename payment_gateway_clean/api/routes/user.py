from fastapi import APIRouter, Depends, HTTPException
from typing import List
from structlog import get_logger
from domain.dtos.request.user import CreateUserRequest, UpdateUserRequest
from domain.dtos.response.api import ApiResponse, ErrorResponse
from domain.dtos.response.user import UserResponse
from core.dependencies import get_user_service, token_security
from domain.service.user import IUserService

router = APIRouter()
logger = get_logger()


@router.get("/users", response_model=ApiResponse[List[UserResponse]])
async def get_users(
    user_service: IUserService = Depends(get_user_service),
    token: str = Depends(token_security),
):
    """Get a list of all users."""
    logger.info("📄 Fetching all users")
    try:
        response = await user_service.get_users()
        if isinstance(response, ErrorResponse):
            logger.warning("⚠️ Failed to retrieve users", error=response.message)
            raise HTTPException(status_code=500, detail="Failed to retrieve users")
        logger.info("✅ Users retrieved successfully")
        return response
    except Exception as e:
        logger.error("🔥 Error while retrieving users", error=str(e))
        raise HTTPException(
            status_code=500, detail="An error occurred while retrieving users"
        )


@router.get("/users/{user_id}", response_model=ApiResponse[UserResponse])
async def get_user_by_id(
    user_id: int,
    user_service: IUserService = Depends(get_user_service),
    token: str = Depends(token_security),
):
    """Get a user by their ID."""
    logger.info("🔍 Fetching user by ID", user_id=user_id)
    try:
        response = await user_service.find_by_id(user_id)
        if isinstance(response, ErrorResponse):
            logger.warning("❌ User not found", user_id=user_id)
            raise HTTPException(status_code=404, detail="User not found")
        logger.info("✅ User found", user_id=user_id)
        return response
    except Exception as e:
        logger.error("🔥 Error while retrieving user", user_id=user_id, error=str(e))
        raise HTTPException(
            status_code=500, detail="An error occurred while retrieving the user"
        )


@router.post("/users", response_model=ApiResponse[UserResponse])
async def create_user(
    user_request: CreateUserRequest,
    user_service: IUserService = Depends(get_user_service),
    token: str = Depends(token_security),
):
    """Create a new user."""
    logger.info("📝 Creating new user", data=user_request.model_dump())
    try:
        response = await user_service.create_user(user_request)
        if isinstance(response, ErrorResponse):
            logger.warning("❌ Failed to create user", error=response.message)
            raise HTTPException(status_code=400, detail="Failed to create user")
        logger.info("✅ User created successfully")
        return response
    except Exception as e:
        logger.error("🔥 Error while creating user", error=str(e))
        raise HTTPException(
            status_code=500, detail="An error occurred while creating the user"
        )


@router.put("/users/{user_id}", response_model=ApiResponse[UserResponse])
async def update_user(
    user_id: int,
    user_request: UpdateUserRequest,
    user_service: IUserService = Depends(get_user_service),
    token: str = Depends(token_security),
):
    """Update an existing user's information."""
    user_request.id = user_id
    logger.info("✏️ Updating user", user_id=user_id, data=user_request.model_dump())
    try:
        response = await user_service.update_user(user_request)
        if isinstance(response, ErrorResponse):
            logger.warning("❌ Failed to update user", user_id=user_id, error=response.message)
            raise HTTPException(status_code=400, detail="Failed to update user")
        logger.info("✅ User updated successfully", user_id=user_id)
        return response
    except Exception as e:
        logger.error("🔥 Error while updating user", user_id=user_id, error=str(e))
        raise HTTPException(
            status_code=500, detail="An error occurred while updating the user"
        )


@router.delete("/users/{user_id}", response_model=ApiResponse[None])
async def delete_user(
    user_id: int,
    user_service: IUserService = Depends(get_user_service),
    token: str = Depends(token_security),
):
    """Delete a user by their ID."""
    logger.info("🗑️ Deleting user", user_id=user_id)
    try:
        response = await user_service.delete_user(user_id)
        if isinstance(response, ErrorResponse):
            logger.warning("❌ Failed to delete user", user_id=user_id, error=response.message)
            raise HTTPException(status_code=404, detail="User not found")
        logger.info("✅ User deleted", user_id=user_id)
        return response
    except Exception as e:
        logger.error("🔥 Error while deleting user", user_id=user_id, error=str(e))
        raise HTTPException(
            status_code=500, detail="An error occurred while deleting the user"
        )
