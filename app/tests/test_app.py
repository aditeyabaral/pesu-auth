import json
import os
from envyaml import EnvYAML

config = EnvYAML("app/tests/config.yaml", strict=False)

def test_convert_readme_to_html_should_convert_readme_to_html_on_start():
    assert "README.html" in os.listdir()


def test_temporary_readme_file_should_not_exist_after_conversion():
    assert "README_tmp.md" not in os.listdir()


def test_index_should_return_readme_as_html(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.text == open("README.html").read()
    assert "Error occurred while retrieving home page" not in response.text


def test_authenticate_should_return_error_when_json_is_not_provided(client):
    response = client.post("/authenticate")
    assert response.status_code == 400
    assert response.content_type == "text/html; charset=utf-8"
    response_json = json.loads(response.data)
    assert response_json["status"] is False
    assert response_json["message"] == "No JSON provided, or Content-Type is not application/json."


def test_authenticate_should_return_error_when_json_is_empty(client):
    response = client.post("/authenticate", headers={"Content-Type": "application/json"}, json={})
    assert response.status_code == 400
    assert response.content_type == "text/html; charset=utf-8"
    response_json = json.loads(response.data)
    assert response_json["status"] is False
    assert response_json["message"] == "No JSON provided, or Content-Type is not application/json."


def test_authenticate_should_return_error_when_password_is_not_provided(client):
    response = client.post(
        "/authenticate",
        headers={"Content-Type": "application/json"},
        json={"username": config["username"]}
    )
    assert response.status_code == 400
    assert response.content_type == "text/html; charset=utf-8"
    response_json = json.loads(response.data)
    assert response_json["status"] is False
    assert response_json["message"] == "Username or password not provided."


def test_authenticate_should_return_error_when_username_is_not_provided(client):
    response = client.post(
        "/authenticate",
        headers={"Content-Type": "application/json"},
        json={"password": config["password"]}
    )
    assert response.status_code == 400
    assert response.content_type == "text/html; charset=utf-8"
    response_json = json.loads(response.data)
    assert response_json["status"] is False
    assert response_json["message"] == "Username or password not provided."


def test_authenticate_should_login_when_valid_username_and_password_is_provided(client):
    response = client.post(
        "/authenticate",
        headers={"Content-Type": "application/json"},
        json={"username": config["username"], "password": config["password"]}
    )
    assert response.status_code == 200
    response_json = json.loads(response.data)
    assert response_json["status"] is True
    assert "timestamp" in response_json
    assert response_json["message"] == "Login successful."
    assert "profile" not in response_json
    assert "know_your_class_and_section" not in response_json

def test_authenticate_should_not_login_when_invalid_username_and_password_is_provided(client):
    response = client.post(
        "/authenticate",
        headers={"Content-Type": "application/json"},
        json={"username": "invalid_username", "password": "invalid_password"}
    )
    assert response.status_code == 200
    response_json = json.loads(response.data)
    assert response_json["status"] is False
    assert "timestamp" in response_json
    assert "profile" not in response_json
    assert response_json["message"] == "Invalid username or password, or the user does not exist."

def test_authenticate_should_return_profile_and_valid_fields_when_profile_is_true(client):
    campus_expansion_map = {"RR": "Ring Road", "EC": "Electronic City"}
    response = client.post(
        "/authenticate",
        headers={"Content-Type": "application/json"},
        json={"username": config["username"], "password": config["password"], "profile": True}
    )
    assert response.status_code == 200
    response_json = json.loads(response.data)
    assert response_json["status"] is True
    assert "timestamp" in response_json
    assert "profile" in response_json
    assert "know_your_class_and_section" in response_json
    assert response_json["message"] == "Login successful."

    assert "name" in response_json["profile"]
    assert response_json["profile"]["name"] == config["name"]
    assert "prn" in response_json["profile"]
    assert response_json["profile"]["prn"] == config["prn"]
    assert "srn" in response_json["profile"]
    assert response_json["profile"]["srn"] == config["srn"]
    assert "program" in response_json["profile"]
    assert response_json["profile"]["program"] == config["program"]
    assert "branch_short_code" in response_json["profile"]
    assert response_json["profile"]["branch_short_code"] == config["branch_short_code"]
    assert "branch" in response_json["profile"]
    assert response_json["profile"]["branch"] == config["branch"]
    assert "semester" in response_json["profile"]
    assert response_json["profile"]["semester"] == config["semester"]
    assert "section" in response_json["profile"]
    assert response_json["profile"]["section"] == config["section"]
    assert "email" in response_json["profile"]
    assert response_json["profile"]["email"] == config["email"]
    assert "phone" in response_json["profile"]
    assert response_json["profile"]["phone"] == config["phone"]
    assert "campus_code" in response_json["profile"]
    assert int(response_json["profile"]["campus_code"]) == int(config["campus_code"])
    assert "campus" in response_json["profile"]
    assert response_json["profile"]["campus"] == config["campus"]

    assert "prn" in response_json["know_your_class_and_section"]
    assert response_json["know_your_class_and_section"]["prn"] == config["prn"]
    assert "srn" in response_json["know_your_class_and_section"]
    assert response_json["know_your_class_and_section"]["srn"] == config["srn"]
    assert "name" in response_json["know_your_class_and_section"]
    assert response_json["know_your_class_and_section"]["name"] == config["name"]
    assert "class" in response_json["know_your_class_and_section"]
    assert response_json["know_your_class_and_section"]["class"] == config["semester"]
    assert "section" in response_json["know_your_class_and_section"]
    assert response_json["know_your_class_and_section"]["section"] == config["section"]
    assert "cycle" in response_json["know_your_class_and_section"]
    assert response_json["know_your_class_and_section"]["cycle"] == config["cycle"]
    assert "department" in response_json["know_your_class_and_section"]
    assert response_json["know_your_class_and_section"]["department"] == f"{config['branch_short_code']} ({config['campus']} Campus)"
    assert "branch" in response_json["know_your_class_and_section"]
    assert response_json["know_your_class_and_section"]["branch"] == config["branch_short_code"]
    assert "institute_name" in response_json["know_your_class_and_section"]
    assert response_json["know_your_class_and_section"]["institute_name"] == f"PES University ({campus_expansion_map[config['campus']]})"





