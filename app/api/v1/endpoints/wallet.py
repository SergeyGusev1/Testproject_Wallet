from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_session
from app.services.wallet import WalletService
from app.schemas.wallet import OperationRequest, WalletResponse, ErrorResponse
from app.crud import wallet_crud


router = APIRouter(prefix='/api/v1/wallets', tags=['wallets'])


@router.get(
    '/{wallet_uuid}',
    response_model=WalletResponse,
    responses={404: {'model': ErrorResponse}}
)
async def get_wallet(
    wallet_uuid: UUID,
    session: AsyncSession = Depends(get_session)
):
    """Получить баланс кошелька"""
    try:
        wallet = await wallet_crud.get_wallet(session,  wallet_uuid)
        return wallet
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.post(
    '/{wallet_uuid}/operation',
    response_model=WalletResponse,
    responses={
        404: {'model': ErrorResponse},
        400: {'model': ErrorResponse}
    }
)
async def operate_wallet(
    wallet_uuid: UUID,
    operation: OperationRequest,
    session: AsyncSession = Depends(get_session)
):
    """Пополнить или снять средства с кошелька"""
    service = WalletService(session)

    try:
        wallet = await service.update_balance(
            wallet_uuid,
            operation.operation_type,
            operation.amount
        )
        return wallet
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
