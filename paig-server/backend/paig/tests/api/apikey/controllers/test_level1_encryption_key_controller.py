import pytest
from unittest.mock import AsyncMock, patch, Mock
from core.exceptions import NotFoundException
from api.apikey.controllers.paig_level1_encryption_key_controller import PaigLevel1EncryptionKeyController
from core.exceptions.error_messages_parser import get_error_message, ERROR_RESOURCE_NOT_FOUND
from api.apikey.services.paig_level1_encryption_key_service import PaigLevel1EncryptionKeyService
from api.apikey.database.db_operations.paig_level1_encryption_key_repository import PaigLevel1EncryptionKeyRepository
from api.encryption.factory.secure_encryptor_factory import SecureEncryptorFactory


@pytest.fixture
def controller(db_session, set_context_session):
    level1_encryption_key_repository = PaigLevel1EncryptionKeyRepository()
    secure_encryptor_factory = SecureEncryptorFactory()

    paig_level1_key_service =  PaigLevel1EncryptionKeyService(
        paig_level1_encryption_key_repository=level1_encryption_key_repository,
        secure_encryptor_factory=secure_encryptor_factory
    )
    controller_instance = PaigLevel1EncryptionKeyController()
    controller_instance._level1_encryption_key_service = paig_level1_key_service

    return controller_instance


@pytest.fixture
def level1_key_data():
    return {
        "id": 123,
        "paig_key_value": "encrypted_value",
        "key_status": "ACTIVE"
    }

@pytest.mark.asyncio
async def test_create_paig_level1_encryption_key(controller):
    from api.encryption.events.startup import create_encryption_master_key_if_not_exists
    await create_encryption_master_key_if_not_exists()

    result = await controller.create_paig_level1_encryption_key()
    assert result is not None

@pytest.mark.asyncio
async def test_get_paig_level1_encryption_key_by_id_success(controller):
    from api.encryption.events.startup import create_encryption_master_key_if_not_exists
    await create_encryption_master_key_if_not_exists()

    created_key = await controller.create_paig_level1_encryption_key()

    result = await controller.get_paig_level1_encryption_key_by_id(created_key.id)
    assert result.id == created_key.id

@pytest.mark.asyncio
async def test_get_paig_level1_encryption_key_by_id_not_found(controller):
    with pytest.raises(NotFoundException) as exc:
        await controller.get_paig_level1_encryption_key_by_id("missing-id")

    expected_message = get_error_message(
        ERROR_RESOURCE_NOT_FOUND, "Level 1 encryption key", "keyId", "missing-id"
    )
    assert expected_message in str(exc.value)




