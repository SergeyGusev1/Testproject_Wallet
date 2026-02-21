from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.wallet import Wallet


async def get_wallet(db: AsyncSession, wallet_uuid: UUID) -> Wallet:
    """Получить кошелёк по UUID"""
    result = await db.execute(
        select(Wallet).where(Wallet.uuid == wallet_uuid)
    )
    wallet = result.scalar_one_or_none()

    if not wallet:
        raise ValueError(f'Кошелёк {wallet_uuid} не найден')
    return wallet


async def get_wallet_for_update(db: AsyncSession, wallet_uuid: UUID) -> Wallet:
    """Получить кошелёк с блокировкой строки"""
    result = await db.execute(
        select(Wallet)
        .where(Wallet.uuid == wallet_uuid)
        .with_for_update()
    )
    wallet = result.scalar_one_or_none()\

    if not wallet:
        raise ValueError(f'Кошелёк {wallet_uuid} не найден')
    return wallet


async def update_wallet_balance(
    db: AsyncSession,
    wallet: Wallet,
    new_balance: int
) -> Wallet:
    """Обновить баланс кошелька"""
    wallet.balance = new_balance
    await db.commit()
    await db.refresh(wallet)
    return wallet
