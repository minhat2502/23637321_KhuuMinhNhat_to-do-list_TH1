def test_register_success(client):
    resp = client.post("/api/v1/auth/register", json={"email": "user@test.com", "password": "pass1234"})
    assert resp.status_code == 201
    data = resp.json()
    assert data["email"] == "user@test.com"
    assert data["is_active"] is True


def test_register_duplicate_email(client):
    payload = {"email": "dup@test.com", "password": "pass1234"}
    client.post("/api/v1/auth/register", json=payload)
    resp = client.post("/api/v1/auth/register", json=payload)
    assert resp.status_code == 400


def test_login_success(client):
    client.post("/api/v1/auth/register", json={"email": "login@test.com", "password": "pass1234"})
    resp = client.post("/api/v1/auth/login", data={"username": "login@test.com", "password": "pass1234"})
    assert resp.status_code == 200
    assert "access_token" in resp.json()


def test_login_wrong_password(client):
    client.post("/api/v1/auth/register", json={"email": "fail@test.com", "password": "pass1234"})
    resp = client.post("/api/v1/auth/login", data={"username": "fail@test.com", "password": "wrongpass"})
    assert resp.status_code == 401


def test_get_me(auth_client):
    resp = auth_client.get("/api/v1/auth/me")
    assert resp.status_code == 200
    assert resp.json()["email"] == "test@test.com"


def test_get_me_no_token(client):
    resp = client.get("/api/v1/auth/me")
    assert resp.status_code == 401
