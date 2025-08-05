from typing import Annotated

from fastapi import Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from core.container import container
from core.security.httptoken import HTTPTokenHeader

from infrastructure.service.auth import AuthService
from infrastructure.service.user import UserService

from core.security.jwt import JwtConfig




token_security = HTTPTokenHeader(
    name="Authorization",
    scheme_name="JWT Token",
    description="Token Format: `Token xxxxxx.yyyyyyy.zzzzzz`",
    raise_error=True,
)
token_security_optional = HTTPTokenHeader(
    name="Authorization",
    scheme_name="JWT Token",
    description="Token Format: `Token xxxxxx.yyyyyyy.zzzzzz`",
    raise_error=False,
)


JWTToken = Annotated[str, Depends(token_security)]
DBSession = Annotated[AsyncSession, Depends(container.session)]


async def get_auth_service():
    return await container.auth_service()

async def get_user_service():
    return await container.user_service()


async def get_saldo_service():
    return await container.saldo_service()


async def get_topup_service():
    return await container.topup_service()



async def get_transfer_service():
    return await container.transfer_service()


async def get_withdraw_service():
    return await container.withdraw_service()



async def get_current_user(
    token: str = Depends(token_security),
    user_service = Depends(get_user_service),
):
    jwt_user = JwtConfig.verify_token(token)

    current_user = await user_service.find_by_id(id=jwt_user)

    return current_user