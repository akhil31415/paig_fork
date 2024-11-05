import pytest
from unittest.mock import patch, MagicMock

from botocore.exceptions import ClientError

from api.guardrails.providers.backend.bedrock import BedrockGuardrailProvider
from api.guardrails.providers import GuardrailConfig
from api.guardrails.providers.models import GuardrailConfigType


@pytest.fixture
def connection_details():
    return {
        'access_key': 'test-access-key',
        'secret_key': 'test-secret-key',
        'region': 'us-east-1'
    }

@pytest.fixture
def session_connection_details():
    return {
        'access_key': 'test-access-key',
        'secret_key': 'test-secret-key',
        'session_token': 'test-session-token',
        'region': 'us-east-1'
    }

@pytest.fixture
def iam_web_identity_details():
    return {
        'k8AwsRoleArn': 'arn:aws:iam::123456789012:role/test-role',
        'k8AwsWebIdentityToken': 'test-web-identity-token',
        'sessionName': 'test-session',
        'region': 'us-east-1'
    }

@pytest.fixture
def iam_role_details():
    return {
        'iam_role': 'arn:aws:iam::123456789012:role/test-role',
        'region': 'us-east-1'
    }


@pytest.fixture
def guardrail_configs():
    return [GuardrailConfig(
        status=1,
        guardrailProvider='AWS',
        guardrailProviderConnectionName='test_connection',
        configType=GuardrailConfigType.TOPIC_POLICY_CONFIG,
        configData="test_data")
    ]


# Test for verifying connection details
@patch('boto3.client')
def test_verify_connection_details_with_access_keys(mock_boto_client, connection_details):
    # Mock successful list_guardrails response
    mock_client = MagicMock()
    mock_client.list_guardrails.return_value = {
        'ResponseMetadata': {'HTTPStatusCode': 200}
    }
    mock_boto_client.return_value = mock_client

    provider = BedrockGuardrailProvider(connection_details)
    result, message = provider.verify_connection_details()

    assert result is True
    assert message == "Connection successful!"
    mock_client.list_guardrails.assert_called_once_with(MaxResults=1)

@patch('boto3.client')
def test_verify_connection_details_with_session_tokens(mock_boto_client, session_connection_details):
    # Mock successful list_guardrails response
    mock_client = MagicMock()
    mock_client.list_guardrails.return_value = {
        'ResponseMetadata': {'HTTPStatusCode': 200}
    }
    mock_boto_client.return_value = mock_client

    provider = BedrockGuardrailProvider(session_connection_details)
    result, message = provider.verify_connection_details()

    assert result is True
    assert message == "Connection successful!"
    mock_client.list_guardrails.assert_called_once_with(MaxResults=1)

@patch('boto3.client')
def test_verify_connection_details_with_assume_iam_role(mock_boto_client, iam_web_identity_details):
    # Mock successful list_guardrails response
    mock_client = MagicMock()
    mock_client.list_guardrails.return_value = {
        'ResponseMetadata': {'HTTPStatusCode': 200}
    }
    mock_boto_client.return_value = mock_client

    provider = BedrockGuardrailProvider(iam_web_identity_details)
    result, message = provider.verify_connection_details()

    assert result is True
    assert message == "Connection successful!"
    mock_client.list_guardrails.assert_called_once_with(MaxResults=1)

@patch('boto3.client')
def test_verify_connection_details_with_iam_role(mock_boto_client, iam_role_details):
    # Mock successful list_guardrails response
    mock_client = MagicMock()
    mock_client.list_guardrails.return_value = {
        'ResponseMetadata': {'HTTPStatusCode': 200}
    }
    mock_boto_client.return_value = mock_client

    provider = BedrockGuardrailProvider(iam_role_details)
    result, message = provider.verify_connection_details()

    assert result is True
    assert message == "Connection successful!"
    mock_client.list_guardrails.assert_called_once_with(MaxResults=1)

def test_verify_connection_details_invalid():
    connection_details = {'invalid_key': 'fake_value'}
    provider = BedrockGuardrailProvider(connection_details)
    result, message = provider.verify_connection_details()
    assert result is False
    assert message == "Connection details are incomplete. Please review your settings."

# New tests incorporating friendly message changes
@patch('boto3.client')
def test_verify_connection_details_success(mock_boto_client, connection_details):
    # Mocking a successful Bedrock client and response
    mock_client = MagicMock()
    mock_client.list_guardrails.return_value = {
        'ResponseMetadata': {'HTTPStatusCode': 200}
    }
    mock_boto_client.return_value = mock_client

    provider = BedrockGuardrailProvider(connection_details)
    result, message = provider.verify_connection_details()

    assert result is True
    assert message == "Connection successful!"
    mock_client.list_guardrails.assert_called_once_with(MaxResults=1)

@patch('boto3.client')
def test_verify_connection_details_failed_verification(mock_boto_client, connection_details):
    # Mocking a Bedrock client with a failed list_guardrails response
    mock_client = MagicMock()
    mock_client.list_guardrails.return_value = {
        'ResponseMetadata': {'HTTPStatusCode': 500}
    }
    mock_boto_client.return_value = mock_client

    provider = BedrockGuardrailProvider(connection_details)
    result, message = provider.verify_connection_details()

    assert result is False
    assert message == "We encountered an issue while verifying your settings. Please try again."

@patch('boto3.client')
def test_verify_connection_details_exception(mock_boto_client, connection_details):
    # Mocking an exception during client initialization
    mock_boto_client.side_effect = Exception("Connection failed")

    provider = BedrockGuardrailProvider(connection_details)
    result, message = provider.verify_connection_details()

    assert result is False
    assert message == "Unable to verify connection. Please check your details and try again."


# Mock boto3 client creation
@patch('boto3.client')
def test_create_bedrock_client_with_access_keys(mock_boto3_client, connection_details):
    provider = BedrockGuardrailProvider(connection_details)
    provider.create_bedrock_client()
    mock_boto3_client.assert_called_once_with(
        'bedrock',
        aws_access_key_id='test-access-key',
        aws_secret_access_key='test-secret-key',
        region_name='us-east-1'
    )


@patch('boto3.client')
def test_create_bedrock_client_with_session_tokens(mock_boto3_client, session_connection_details):
    provider = BedrockGuardrailProvider(session_connection_details)
    provider.create_bedrock_client()
    mock_boto3_client.assert_called_once_with(
        'bedrock',
        aws_access_key_id='test-access-key',
        aws_secret_access_key='test-secret-key',
        aws_session_token='test-session-token',
        region_name='us-east-1'
    )


@patch('boto3.client')
def test_create_bedrock_client_with_iam_web_identity(mock_boto3_client, iam_web_identity_details):
    mock_boto3_client.return_value = MagicMock()
    mock_boto3_client.return_value.assume_role_with_web_identity = MagicMock(
        return_value = {
            'Credentials': {
                'AccessKeyId': 'fake_temp_access_key',
                'SecretAccessKey': 'fake_temp_secret_key',
                'SessionToken': 'fake_temp_session_token'
            }
        }
    )

    provider = BedrockGuardrailProvider(iam_web_identity_details)
    provider.create_bedrock_client()

    # mock_sts_boto3.assert_called_once_with('sts')
    mock_boto3_client.assert_called_with(
        'bedrock',
        aws_access_key_id='fake_temp_access_key',
        aws_secret_access_key='fake_temp_secret_key',
        aws_session_token='fake_temp_session_token',
        region_name='us-east-1'
    )


@patch('boto3.client')
def test_create_bedrock_client_with_iam_role(mock_boto3_client, iam_role_details):
    provider = BedrockGuardrailProvider(iam_role_details)
    provider.create_bedrock_client()
    mock_boto3_client.assert_called_once_with(
        'bedrock',
        region_name='us-east-1'
    )


# Mock guardrail action
@patch.object(BedrockGuardrailProvider, 'create_bedrock_client')
@patch.object(BedrockGuardrailProvider, '_perform_guardrail_action')
def test_create_guardrail(mock_perform_guardrail_action, mock_create_bedrock_client, connection_details,
                          guardrail_configs):
    provider = BedrockGuardrailProvider(connection_details)
    provider.create_guardrail(guardrail_configs, name='test_guardrail', kmsKeyId='test_key', tags=['test_tag'])

    mock_create_bedrock_client.assert_called_once()
    mock_perform_guardrail_action.assert_called_once()


# Test updating guardrail
@patch.object(BedrockGuardrailProvider, '_perform_guardrail_action')
@patch.object(BedrockGuardrailProvider, 'create_bedrock_client')
def test_update_guardrail(mock_create_bedrock_client, mock_perform_guardrail_action, connection_details,
                          guardrail_configs):
    provider = BedrockGuardrailProvider(connection_details)
    created_guardrail_details = {'response': {'guardrailId': 'test_id'}}
    provider.update_guardrail(created_guardrail_details, guardrail_configs)

    mock_create_bedrock_client.assert_called_once()
    mock_perform_guardrail_action.assert_called_once()


# Test deleting guardrail
@patch.object(BedrockGuardrailProvider, '_perform_guardrail_action')
@patch.object(BedrockGuardrailProvider, 'create_bedrock_client')
def test_delete_guardrail(mock_create_bedrock_client, mock_perform_guardrail_action, connection_details):
    provider = BedrockGuardrailProvider(connection_details)
    created_guardrail_details = {'response': {'guardrailId': 'test_id'}}
    provider.delete_guardrail(created_guardrail_details)

    mock_create_bedrock_client.assert_called_once()
    mock_perform_guardrail_action.assert_called_once()


# Test payload construction
def test_get_create_bedrock_guardrail_payload(connection_details, guardrail_configs):
    provider = BedrockGuardrailProvider(connection_details)
    payload = provider.get_create_bedrock_guardrail_payload(guardrail_configs, name='test_guardrail')

    assert payload['name'] == 'test_guardrail'
    assert payload['description'] == ''
    assert payload[GuardrailConfigType.BLOCKED_INPUTS_MESSAGING] == 'Sorry, the model cannot answer this question.'
    assert payload[GuardrailConfigType.BLOCKED_OUTPUTS_MESSAGING] == 'Sorry, the model cannot answer this question.'


# Test performing guardrail action and handling exceptions
@patch('boto3.client')
def test_perform_guardrail_action_success(mock_boto3_client, connection_details):
    mock_client = MagicMock()
    mock_client.create_guardrail.return_value = {'guardrailId': '123', 'guardrailArn': 'arn:aws:bedrock::123', 'version': 'DRAFT'}
    provider = BedrockGuardrailProvider(connection_details)

    success, result = provider._perform_guardrail_action(mock_client.create_guardrail, {'name': 'test_guardrail'})
    assert success == True
    assert result == {'guardrailId': '123', 'guardrailArn': 'arn:aws:bedrock::123', 'version': 'DRAFT'}


# Test exception handling
@patch('boto3.client')
def test_handle_bedrock_exceptions(mock_boto3_client, connection_details):
    mock_client = MagicMock()
    mock_client.exceptions.ResourceNotFoundException = ClientError
    provider = BedrockGuardrailProvider(connection_details)

    exception = ClientError({"Error": {"Code": "ResourceNotFoundException"}}, "create_guardrail")
    result = provider.handle_bedrock_exceptions(exception, mock_client)

    assert result['message'] == "Resource not found. Please verify that the resource you are trying to access exists."
    assert result['details']['errorType'] == 'ClientError'