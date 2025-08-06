from fastapi import APIRouter
from api.routes import auth, health_checker, saldo, topup, transfer, withdraw

router = APIRouter()

router.include_router(
    router=health_checker.router, tags=["Health"], prefix="/health-check"
)

router.include_router(router=auth.router, tags=[
                      "Authentication"], prefix="/auth")

router.include_router(router=saldo.router, tags=["Saldo"], prefix="/saldo")

router.include_router(router=topup.router, tags=["Topup"], prefix="/topup")

router.include_router(router=transfer.router, tags=[
                      "Transfer"], prefix="/transfer")

router.include_router(router=withdraw.router, tags=[
                      "Withdraw"], prefix="/withdraw")
