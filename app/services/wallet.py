from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.wallet import Wallet
from app.schemas.wallet import OperationType
from app.crud import wallet_crud


class WalletService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def update_balance(
        self,
        wallet_uuid: UUID,
        operation_type: OperationType,
        amount: int
    ) -> Wallet:
        """Обновление баланса с защитой от race conditions"""

        wallet = await wallet_crud.get_wallet_for_update(self.session,
                                                         wallet_uuid)
        if operation_type == OperationType.DEPOSIT:
            new_balance = wallet.balance + amount
        else:
            new_balance = wallet.balance - amount
            if new_balance < 0:
                raise ValueError(
                    f'Недостаточно срудств. Доступно {wallet.balance}'
                )
        return await wallet_crud.update_wallet_balance(
            self.session,
            wallet,
            new_balance
        )