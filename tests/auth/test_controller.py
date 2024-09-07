from src.auth import User

from tests.test_setup import client, session
from tests.constants import full_register_payload, full_login_payload


def test_validation_failing_if_email_missing_register(client, session):
    full_register_payload_copy = full_register_payload.copy()
    del full_register_payload_copy["email"]

    api_response = client.post("/api/v1/auth/register", json=full_register_payload_copy)
    status_code = api_response.status_code
    assert status_code == 422


def test_validation_failing_if_name_missing_register(client, session):
    full_register_payload_copy = full_register_payload.copy()
    del full_register_payload_copy["name"]

    api_response = client.post("/api/v1/auth/register", json=full_register_payload_copy)
    status_code = api_response.status_code
    assert status_code == 422


def test_validation_failing_if_password_missing_register(client, session):
    full_register_payload_copy = full_register_payload.copy()
    del full_register_payload_copy["password"]

    api_response = client.post("/api/v1/auth/register", json=full_register_payload_copy)
    status_code = api_response.status_code
    assert status_code == 422


def test_validation_failing_if_confirm_password_missing_register(client, session):
    full_register_payload_copy = full_register_payload.copy()
    del full_register_payload_copy["confirm_password"]

    api_response = client.post("/api/v1/auth/register", json=full_register_payload_copy)
    status_code = api_response.status_code
    assert status_code == 422


def test_validation_failing_if_password_not_equal_to_confirm_password_in_register(client, session):
    full_register_payload_copy = full_register_payload.copy()
    full_register_payload_copy["confirm_password"] = "test@123"

    api_response = client.post("/api/v1/auth/register", json=full_register_payload_copy)
    status_code = api_response.status_code
    assert status_code == 400


def test_validation_failing_if_name_lt_2_and_gt_50_in_register(client, session):
    full_register_payload_copy = full_register_payload.copy()
    full_register_payload_copy["name"] = "t"

    api_response = client.post("/api/v1/auth/register", json=full_register_payload_copy)
    status_code = api_response.status_code
    assert status_code == 400

    full_register_payload_copy[
        "name"] = "tsfdfsgsdgfsgdfgsfdtsfdfsgsdgfsgdfgsfdtsfdfsgsdgfsgdfgsfdtsfdfsgsdgfsgdfgsfdtsfdfsgsdgfsgdfgsfdtsfdfsgsdgfsgdfgsfdtsfdfsgsdgfsgdfgsfd"

    api_response = client.post("/api/v1/auth/register", json=full_register_payload_copy)
    status_code = api_response.status_code
    assert status_code == 400


def test_validation_failing_if_password_lt_6_and_gt_20_in_register(client, session):
    full_register_payload_copy = full_register_payload.copy()
    full_register_payload_copy["password"] = "dummy"
    full_register_payload_copy["confirm_password"] = "dummy"

    api_response = client.post("/api/v1/auth/register", json=full_register_payload_copy)
    status_code = api_response.status_code
    assert status_code == 400

    full_register_payload_copy[
        "password"] = "tsfdfsgsdgfsgdfgsfdtsfdfsgsdgfsgdfgsfdtsfdfsgsdgfsgdfgsfdtsfdfsgsdgfsgdfgsfdtsfdfsgsdgfsgdfgsfdtsfdfsgsdgfsgdfgsfdtsfdfsgsdgfsgdfgsfd"

    api_response = client.post("/api/v1/auth/register", json=full_register_payload_copy)
    status_code = api_response.status_code
    assert status_code == 400


def test_validation_failing_if_confirm_password_lt_6_and_gt_20_in_register(client, session):
    full_register_payload_copy = full_register_payload.copy()
    full_register_payload_copy["confirm_password"] = "dummy"
    full_register_payload_copy["password"] = "dummy"

    api_response = client.post("/api/v1/auth/register", json=full_register_payload_copy)
    status_code = api_response.status_code
    assert status_code == 400

    full_register_payload_copy[
        "password"] = "tsfdfsgsdgfsgdfgsfdtsfdfsgsdgfsgdfgsfdtsfdfsgsdgfsgdfgsfdtsfdfsgsdgfsgdfgsfdtsfdfsgsdgfsgdfgsfdtsfdfsgsdgfsgdfgsfdtsfdfsgsdgfsgdfgsfd"

    api_response = client.post("/api/v1/auth/register", json=full_register_payload_copy)
    status_code = api_response.status_code
    assert status_code == 400


def test_validation_failing_if_email_not_in_proper_format_in_register(client, session):
    full_register_payload_copy = full_register_payload.copy()
    full_register_payload_copy["email"] = "test123"

    api_response = client.post("/api/v1/auth/register", json=full_register_payload_copy)
    status_code = api_response.status_code
    assert status_code == 400


def test_validation_failing_if_user_with_same_email_already_exists_in_register(client, session):
    api_response = client.post("/api/v1/auth/register", json=full_register_payload)
    full_register_payload_copy = full_register_payload.copy()
    full_register_payload_copy["email"] = api_response.json()["data"]["email"]

    api_response = client.post("/api/v1/auth/register", json=full_register_payload_copy)
    status_code = api_response.status_code
    assert status_code == 400
    assert api_response.json()["message"] == "Email already exist."


def test_registering_a_user(client, session):
    api_response = client.post("/api/v1/auth/register", json=full_register_payload)

    status_code = api_response.status_code
    assert status_code == 201

    json_response = api_response.json()
    assert len(json_response["data"]['token']) == 145
    assert session.query(User).count() == 1


def test_validation_failing_if_password_lt_6_and_gt_20_in_login(client, session):
    full_login_payload_copy = full_login_payload.copy()
    full_login_payload_copy["password"] = "dummy"

    api_response = client.post("/api/v1/auth/login", json=full_login_payload_copy)
    status_code = api_response.status_code
    assert status_code == 400

    full_login_payload_copy[
        "password"] = "tsfdfsgsdgfsgdfgsfdtsfdfsgsdgfsgdfgsfdtsfdfsgsdgfsgdfgsfdtsfdfsgsdgfsgdfgsfdtsfdfsgsdgfsgdfgsfdtsfdfsgsdgfsgdfgsfdtsfdfsgsdgfsgdfgsfd"

    api_response = client.post("/api/v1/auth/login", json=full_login_payload_copy)
    status_code = api_response.status_code
    assert status_code == 400


def test_validation_failing_if_email_not_in_proper_format_in_login(client, session):
    full_login_payload_copy = full_login_payload.copy()
    full_login_payload_copy["email"] = "test@123"

    api_response = client.post("/api/v1/auth/login", json=full_login_payload_copy)
    status_code = api_response.status_code
    assert status_code == 400


def test_logging_in_a_user(client, session):
    client.post("/api/v1/auth/register", json=full_register_payload)

    login_payload = {
        "email": "a@dummy.com",
        "password": "dummy@123"
    }

    api_response = client.post("/api/v1/auth/login", json=login_payload)

    status_code = api_response.status_code
    assert status_code == 200

    json_response = api_response.json()
    assert json_response["data"]['name'] == 'dhaval 1'
    assert len(json_response["data"]['token']) == 145
