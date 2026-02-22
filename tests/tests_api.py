import pytest
import uuid
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text

from app.main import app
from app.core.db import Base, get_session


TEST_DB_URL = 'sqlite+aiosqlite:///./test.db'
test_engine = create_async_engine(TEST_DB_URL)
TestingLocalSession = sessionmaker(test_engine, class_=AsyncSession)


async def override_get_session():
    async with TestingLocalSession() as session:
        yield session

app.dependency_overrides[get_session] = override_get_session


@pytest.fixture(autouse=True)
async def setup_db():
    """Создание таблиц перед тестами"""
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def client():
    """Клиент для тестов"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url='http://test') as ac:
        yield ac


@pytest.fixture
async def test_wallet():
    """Создание тестового кошелька через прямой SQL"""
    async with TestingLocalSession() as session:
        wallet_uuid_raw = uuid.uuid4()
        wallet_uuid_with_hyphens = str(wallet_uuid_raw)
        wallet_uuid_no_hyphens = wallet_uuid_raw.hex

        await session.execute(
            text(
                'INSERT INTO wallets(uuid, balance) VALUES (:uuid, :balance)'),
            {'uuid': wallet_uuid_no_hyphens, 'balance': 1000}
        )
        await session.commit()

        return {
            'uuid_with_hyphens': wallet_uuid_with_hyphens,
            'uuid_no_hyphens': wallet_uuid_no_hyphens,
            'balance': 1000
        }


@pytest.mark.asyncio
async def test_get_wallet_success(client, test_wallet):
    """Тест 1. Успешное получение кошелька"""
    response = await client.get(
        f'/api/v1/wallets/{test_wallet["uuid_with_hyphens"]}')
    assert response.status_code == 200
    data = response.json()
    assert data['uuid'].replace('-', '') == test_wallet['uuid_no_hyphens']
    assert data['balance'] == test_wallet['balance']


@pytest.mark.asyncio
async def test_deposit(client, test_wallet):
    """Тест 2. Пополнение кошелька"""
    response = await client.post(
        f'/api/v1/wallets/{test_wallet["uuid_no_hyphens"]}/operation',
        json={'operation_type': 'DEPOSIT', 'amount': 1000}
    )
    assert response.status_code == 200
    assert response.json()['balance'] == 2000


@pytest.mark.asyncio
async def test_withdraw_success(client, test_wallet):
    """Тест 3. Успешное снятие"""
    response = await client.post(
        f'/api/v1/wallets/{test_wallet["uuid_no_hyphens"]}/operation',
        json={'operation_type': 'WITHDRAW', 'amount': 500}
    )
    assert response.status_code == 200
    assert response.json()['balance'] == 500


@pytest.mark.asyncio
async def test_withdraw_fail(client, test_wallet):
    """Тест 4. Снятие больше чем есть"""
    response = await client.post(
        f'/api/v1/wallets/{test_wallet["uuid_no_hyphens"]}/operation',
        json={'operation_type': 'WITHDRAW', 'amount': 1500}
    )
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_get_wallet_fail(client):
    """Тест 5. Несуществующий кошелёк"""
    random_uuid = uuid.uuid4().hex
    response = await client.get(f'/api/v1/wallets/{random_uuid}')
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_post_wallet_fail(client):
    """Тест 6. Несуществующий кошелёк при изменении"""
    random_uuid = uuid.uuid4().hex
    response = await client.post(
        f'/api/v1/wallets/{random_uuid}/operation',
        json={'operation_type': 'DEPOSIT', 'amount': 100}
    )
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_invalid_amount(client, test_wallet):
    """Тест 7. Отрицательная сумма"""
    response = await client.post(
        f'/api/v1/wallets/{test_wallet["uuid_no_hyphens"]}/operation',
        json={'operation_type': 'DEPOSIT', 'amount': -100}
    )
    assert response.status_code == 422
