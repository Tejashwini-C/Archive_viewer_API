import pytest
from utils.request import request_call
from payload.json_payload import Payload
from utils.logger import log_request_response
from utils.excel import get_test_data

call_method = request_call()

# ------------------ DYNAMIC SHEET READS ------------------

headers_conn, data_conn = get_test_data("metadata_test_connection")
headers_create_tables, data_create_tables = get_test_data("metadata_Create_tables")
headers_super_user, data_super_user = get_test_data("Super_user")
headers_add_storage, data_add_storage = get_test_data("add_storage")
headers_fetch_storage, data_fetch_storage = get_test_data("fetch_storage")
headers_convert_server, data_convert_server = get_test_data("convert_server")
headers_query_server, data_query_server = get_test_data("query_server")

# ------------------ BASIC TESTS ------------------

class Testarchive:
    auth_token = None

    def test_health_check(self):
        response = call_method.test_get_method("v1/health-check")
        assert response.status_code == 200
        log_request_response(response)

    def test_meta_data(self):
        response = call_method.test_get_method("v1/metadata-status")
        assert response.status_code == 200
        log_request_response(response)

    def test_metadata_info(self):
        response = call_method.test_get_method("v1/metadata-info")
        assert response.status_code == 200
        log_request_response(response)

    def test_superuser_status(self):
        response = call_method.test_get_method("v1/superuser-status")
        assert response.status_code == 404
        log_request_response(response)

    def test_app_preferences(self):
        response = call_method.test_get_method("v1/app-preferences")
        assert response.status_code == 404
        log_request_response(response)

    def test_onboarding(self):
        response = call_method.test_get_method("v1/onboarding")
        assert response.status_code == 404
        log_request_response(response)

# ------------------ PARAMETERIZED TESTS ------------------

@pytest.mark.parametrize(",".join(headers_conn), data_conn, ids=[f"{row[0]}" for row in data_conn])
def test_add_metadata_test_connection(testcasename, action, connectionType, NNE_enabled, LoginType, status,
                                      databaseType, host, port, username, psswrd, databaseName, excepeted_statuscode):
    params = Payload.meta_data_params(action, connectionType, NNE_enabled, LoginType, status)
    body = Payload.meta_data_body(databaseType, host, port, username, psswrd, databaseName)
    metadata_response = call_method.test_post_method("v1/meta-data", params=params, json=body)
    log_request_response(metadata_response, request_body=body, params=params)
    assert metadata_response.status_code == excepeted_statuscode


@pytest.mark.parametrize(",".join(headers_create_tables), data_create_tables, ids=[f"{row[0]}" for row in data_create_tables])
def test_add_metadata_create_tables(testcasename, action, connectionType, NNE_enabled, LoginType, status,
                                    databaseType, host, port, username, psswrd, databaseName, excepeted_statuscode):
    params = Payload.meta_data_params(action, connectionType, NNE_enabled, LoginType, status)
    body = Payload.meta_data_body(databaseType, host, port, username, psswrd, databaseName)
    response = call_method.test_post_method("v1/meta-data", params=params, json=body)
    log_request_response(response, request_body=body, params=params)
    assert response.status_code == excepeted_statuscode


@pytest.mark.parametrize(",".join(headers_super_user), data_super_user, ids=[f"{row[0]}" for row in data_super_user])
def test_onboarding_authentication(testcasename, loginType, name, username, psswrd, email, excepeted_statuscode):
    body = Payload.Super_user_payload(loginType, name, username, psswrd, email)
    response = call_method.test_post_method("/v1/onboarding-authentication", json=body)
    log_request_response(response, request_body=body)
    assert response.status_code == excepeted_statuscode

    if response.status_code == 200:
        token = response.json().get("detail", {}).get("data", {}).get("access_token")
        if token:
            # Store token in a file
            with open("utils/Auth.txt", "w", encoding="utf-8") as f:
                f.write(f"Bearer {token}")

@pytest.mark.parametrize(",".join(headers_add_storage), data_add_storage, ids=[f"{row[0]}" for row in data_add_storage])
def test_add_storage(testcasename, storageType, name, locationType, mountPath, path, UNC_path, storageProtocol, saveFlag, excepeted_statuscode):
    params = Payload.add_storage_params(storageType)
    body = Payload.add_storage_body(name, locationType, mountPath, path, UNC_path, storageProtocol, saveFlag)
    response = call_method.test_post_method("/v1/manage-storage", params=params, json=body)
    log_request_response(response, request_body=body, params=params)
    assert response.status_code == excepeted_statuscode



@pytest.mark.parametrize(",".join(headers_fetch_storage), data_fetch_storage, ids=[f"{row[0]}" for row in data_fetch_storage])
def test_fetch_storage(testcasename, storageId, excepeted_statuscode):
    params = Payload.fetch_storage_params(storageId)
    response = call_method.test_get_method("/v1/manage-storage", params=params)
    log_request_response(response, params=params)
    assert response.status_code == excepeted_statuscode

@pytest.mark.parametrize(",".join(headers_convert_server), data_convert_server, ids=[f"{row[0]}" for row in data_convert_server])
def test_convert_server(testcasename, platformType, optimServerName, optimDirectory, psthomePath, defaultQualifier, storageId, excepeted_statuscode):
    params = Payload.convert_server_params(platformType)
    body = Payload.convert_server_body(optimServerName, optimDirectory, psthomePath, defaultQualifier, storageId)
    response = call_method.test_post_method("/v1/convert-server", params=params, json=body)
    log_request_response(response, request_body=body, params=params)
    assert response.status_code == excepeted_statuscode

@pytest.mark.parametrize(",".join(headers_query_server), data_query_server, ids=[f"{row[0]}" for row in data_query_server])
def test_query_server(testcasename, catalogType, skip, ssl, queryServerName, databaseName, host, port, username, psswrd, excepeted_statuscode):
    params = Payload.query_server_params(catalogType, skip, ssl)
    body = Payload.query_server_body(queryServerName, databaseName, host, port, username, psswrd)
    response = call_method.test_post_method("/v1/query-server", params=params, json=body)
    log_request_response(response, request_body=body, params=params)
    assert response.status_code == excepeted_statuscode


