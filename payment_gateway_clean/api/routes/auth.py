from fastapi import APIRouter, Depends, HTTPException
from typing import Union
from domain.dtos.request.auth import RegisterRequest, LoginRequest
from domain.dtos.response.api import ApiResponse, ErrorResponse
from domain.dtos.response.user import UserResponse
from infrastructure.service.auth import AuthService
from core.dependencies import get_auth_service, token_security, get_user_service
from core.security.jwt import JwtConfig
from core.container import container

router = APIRouter()

@router.post("/register", response_model=ApiResponse[UserResponse])
async def register_user(
    request: RegisterRequest, auth_service: AuthService = Depends(get_auth_service)
):
    """Register a new user."""
    try:
        user = await auth_service.register_user(request)

        if isinstance(user, ErrorResponse):
            raise HTTPException(status_code=400, detail="Failed to create user")

        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while registering the user")

@router.post("/login", response_model=ApiResponse[str])
async def login_user(
    request: LoginRequest, auth_service: AuthService = Depends(get_auth_service)
):
    try:
        user = await auth_service.login_user(request)

        if isinstance(user, ErrorResponse):
            raise HTTPException(status_code=404, detail="User not found or login failed")

        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred during login")


@router.get("/me", response_model=Union[ApiResponse[UserResponse], ErrorResponse])
async def me(
    token: str = Depends(token_security),
    user_service = Depends(get_user_service),
):
    try:
        jwt_user = container.get_jwt().verify_token(token=token)
        current_user = await user_service.find_by_id(id=jwt_user)

        if isinstance(current_user, ErrorResponse):
            raise HTTPException(status_code=404, detail="User not found")

        return current_user
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while fetching user information")
