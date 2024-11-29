from fastapi import APIRouter, Depends
from core.dependencies import token_security



router = APIRouter()


@router.get("")
async def health_check(token: str =Depends(token_security)) -> dict:
    print("Hello {}".format(token))
    return {"message": "hello health check"}