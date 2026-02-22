from pydantic import BaseModel, Field, UUID4, ConfigDict
from enum import Enum


class OperationType(str, Enum):
    DEPOSIT = 'DEPOSIT'
    WITHDRAW = 'WITHDRAW'


class OperationRequest(BaseModel):
    operation_type: OperationType
    amount: int = Field(..., gt=0, description='Сумма в рублях')


class WalletResponse(BaseModel):
    uuid: UUID4
    balance: int

    model_config = ConfigDict(from_attributes=True)


class ErrorResponse(BaseModel):
    detail: str
