import contextlib
from collections.abc import AsyncIterator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from core.config import get_app_settings
from core.settings.base import BaseAppSettings

from domain.repository.user import IUserRepository
from infrastructure.repository.user import UserRepository

from domain.repository.saldo import ISaldoRepository
from infrastructure.repository.saldo import SaldoRepository

from domain.repository.topup import ITopupRepository
from infrastructure.repository.topup import TopupRepository

from domain.repository.transfer import ITransferRepository
from infrastructure.repository.transfer import TransferRepository

from domain.repository.withdraw import IWithdrawRepository
from infrastructure.repository.withdraw import WithdrawRepository

from domain.service.user import IUserService
from infrastructure.service.user import UserService

from domain.service.saldo import ISaldoService
from infrastructure.service.saldo import SaldoService

from domain.service.topup import ITopupService
from infrastructure.service.topup import TopupService

from domain.service.transfer import ITransferService
from infrastructure.service.transfer import TransferService

from domain.service.withdraw import IWithdrawService
from infrastructure.service.withdraw import WithdrawService

from domain.service.auth import IAuthService
from infrastructure.service.auth import AuthService

from core.security.jwt import JwtConfig
from core.security.hashpassword import Hashing


class Container:
    def __init__(self, settings: BaseAppSettings) -> None:
        self._settings = settings
        self._engine = create_async_engine(**settings.sqlalchemy_engine_props)
        self._session = async_sessionmaker(bind=self._engine, expire_on_commit=False)

    @property
    def session(self) -> async_sessionmaker:
        return self._session


    def get_jwt(self) -> JwtConfig:
        return JwtConfig(self._settings.jwt_secret_key, self._settings.jwt_token_expiration_minutes)

    async def user_repository(self) -> IUserRepository:
        session = self._session()
        return UserRepository(session)

    async def saldo_repository(self) -> ISaldoRepository:
        session = self._session

        return SaldoRepository(
            session
        )

    async def topup_repository(self) -> ITopupRepository:
        session = self._session

        return TopupRepository(
            session
        )

    async def transfer_repository(self) -> ITransferRepository:
        session = self._session

        return TransferRepository(
            session
        )

    async def withdraw_repository(self) -> IWithdrawRepository:
        session = self._session

        return WithdrawRepository(
            session
        )

    async def auth_service(self) -> IAuthService:
        user_repo = await self.user_repository()
        return AuthService(
            repository=user_repo,
            hashing=Hashing(),
            jwt_config=self.get_jwt()
        )

    async def user_service(self) -> IUserService:
        user_repo = await self.user_repository()

        return UserService(
            repository=user_repo,
            hashing=Hashing()
        )

    
    async def saldo_service(self) -> ISaldoService:
        user_repo = await self.user_repository()
        saldo_repo = await self.saldo_repository()

        return SaldoService(
            user_repository=user_repo,
            saldo_repository=saldo_repo
        )

    async def topup_service(self) -> ITopupService:
        user_repo = await self.user_repository()
        saldo_repo = await self.saldo_repository()
        topup_repo = await self.topup_repository()

        return TopupService(
            topup_repository=topup_repo,
            user_repository=user_repo,
            saldo_repository=saldo_repo
        )

    async def transfer_service(self) -> ITransferService:
        user_repo = await self.user_repository()
        saldo_repo = await self.saldo_repository()
        transfer_repo = await self.transfer_repository()

        return TransferService(
            transfer_repository==transfer_repo,
            user_repository=user_repo,
            saldo_repository=saldo_repo
        )

    async def withdraw_service(self) -> IWithdrawService:
        user_repo = await self.user_repository()
        saldo_repo = await self.saldo_repository()
        withdraw_repo = await self.withdraw_repository()

        return WithdrawService(
            withdraw_repository=withdraw_repo,
            user_repository=user_repo,
            saldo_repository=saldo_repo
        )







container = Container(settings=get_app_settings())