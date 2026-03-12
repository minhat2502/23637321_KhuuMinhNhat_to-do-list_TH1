import pytest


def test_create_todo_success(auth_client):
    resp = auth_client.post("/api/v1/todos", json={"title": "Mua sữa"})
    assert resp.status_code == 201
    data = resp.json()
    assert data["title"] == "Mua sữa"
    assert data["is_done"] is False


def test_create_todo_with_tags_and_due_date(auth_client):
    resp = auth_client.post("/api/v1/todos", json={
        "title": "Học FastAPI",
        "due_date": "2026-03-20",
        "tags": ["học tập", "công việc"],
    })
    assert resp.status_code == 201
    data = resp.json()
    assert data["due_date"] == "2026-03-20"
    assert len(data["tags"]) == 2


def test_create_todo_title_too_short(auth_client):
    resp = auth_client.post("/api/v1/todos", json={"title": "ab"})
    assert resp.status_code == 422


def test_create_todo_title_empty(auth_client):
    resp = auth_client.post("/api/v1/todos", json={"title": ""})
    assert resp.status_code == 422


def test_create_todo_no_auth(client):
    resp = client.post("/api/v1/todos", json={"title": "No auth todo"})
    assert resp.status_code == 401


def test_list_todos(auth_client):
    auth_client.post("/api/v1/todos", json={"title": "Todo số 1"})
    auth_client.post("/api/v1/todos", json={"title": "Todo số 2"})
    resp = auth_client.get("/api/v1/todos")
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2


def test_list_todos_filter_is_done(auth_client):
    auth_client.post("/api/v1/todos", json={"title": "Chưa xong", "is_done": False})
    auth_client.post("/api/v1/todos", json={"title": "Đã xong rồi", "is_done": True})
    resp = auth_client.get("/api/v1/todos?is_done=false")
    assert resp.json()["total"] == 1


def test_get_todo_success(auth_client):
    create_resp = auth_client.post("/api/v1/todos", json={"title": "Chi tiết todo"})
    todo_id = create_resp.json()["id"]
    resp = auth_client.get(f"/api/v1/todos/{todo_id}")
    assert resp.status_code == 200
    assert resp.json()["id"] == todo_id


def test_get_todo_not_found(auth_client):
    resp = auth_client.get("/api/v1/todos/99999")
    assert resp.status_code == 404


def test_update_todo(auth_client):
    create_resp = auth_client.post("/api/v1/todos", json={"title": "Cần cập nhật"})
    todo_id = create_resp.json()["id"]
    resp = auth_client.put(f"/api/v1/todos/{todo_id}", json={"title": "Đã cập nhật", "is_done": True})
    assert resp.status_code == 200
    assert resp.json()["title"] == "Đã cập nhật"
    assert resp.json()["is_done"] is True


def test_patch_todo(auth_client):
    create_resp = auth_client.post("/api/v1/todos", json={"title": "Patch test todo"})
    todo_id = create_resp.json()["id"]
    resp = auth_client.patch(f"/api/v1/todos/{todo_id}", json={"is_done": True})
    assert resp.status_code == 200
    assert resp.json()["is_done"] is True


def test_complete_todo(auth_client):
    create_resp = auth_client.post("/api/v1/todos", json={"title": "Cần hoàn thành"})
    todo_id = create_resp.json()["id"]
    resp = auth_client.post(f"/api/v1/todos/{todo_id}/complete")
    assert resp.status_code == 200
    assert resp.json()["is_done"] is True


def test_delete_todo(auth_client):
    create_resp = auth_client.post("/api/v1/todos", json={"title": "Cần xóa đi"})
    todo_id = create_resp.json()["id"]
    resp = auth_client.delete(f"/api/v1/todos/{todo_id}")
    assert resp.status_code == 204
    # Sau khi soft-delete, GET by id phải trả 404
    assert auth_client.get(f"/api/v1/todos/{todo_id}").status_code == 404


def test_delete_todo_not_found(auth_client):
    resp = auth_client.delete("/api/v1/todos/99999")
    assert resp.status_code == 404


def test_soft_delete_hidden_from_list(auth_client):
    auth_client.post("/api/v1/todos", json={"title": "Todo sống"})
    del_resp = auth_client.post("/api/v1/todos", json={"title": "Todo bị xóa mềm"})
    todo_id = del_resp.json()["id"]
    auth_client.delete(f"/api/v1/todos/{todo_id}")
    list_resp = auth_client.get("/api/v1/todos")
    titles = [t["title"] for t in list_resp.json()["items"]]
    assert "Todo bị xóa mềm" not in titles
    assert list_resp.json()["total"] == 1


def test_get_deleted_todos(auth_client):
    del_resp = auth_client.post("/api/v1/todos", json={"title": "Sẽ vào thùng rác"})
    todo_id = del_resp.json()["id"]
    auth_client.delete(f"/api/v1/todos/{todo_id}")
    resp = auth_client.get("/api/v1/todos/deleted")
    assert resp.status_code == 200
    assert any(t["id"] == todo_id for t in resp.json())


def test_restore_todo(auth_client):
    del_resp = auth_client.post("/api/v1/todos", json={"title": "Cần khôi phục"})
    todo_id = del_resp.json()["id"]
    auth_client.delete(f"/api/v1/todos/{todo_id}")
    restore_resp = auth_client.post(f"/api/v1/todos/{todo_id}/restore")
    assert restore_resp.status_code == 200
    assert restore_resp.json()["id"] == todo_id
    # Sau khi restore, todo xuất hiện lại trong danh sách
    assert auth_client.get(f"/api/v1/todos/{todo_id}").status_code == 200


def test_restore_todo_not_found(auth_client):
    resp = auth_client.post("/api/v1/todos/99999/restore")
    assert resp.status_code == 404


def test_user_cannot_access_other_user_todo(client):
    # User A tạo todo
    client.post("/api/v1/auth/register", json={"email": "a@test.com", "password": "pass1234"})
    resp_a = client.post("/api/v1/auth/login", data={"username": "a@test.com", "password": "pass1234"})
    token_a = resp_a.json()["access_token"]
    create_resp = client.post(
        "/api/v1/todos", json={"title": "Todo của A"},
        headers={"Authorization": f"Bearer {token_a}"},
    )
    todo_id = create_resp.json()["id"]

    # User B đăng nhập và cố xem todo của A
    client.post("/api/v1/auth/register", json={"email": "b@test.com", "password": "pass1234"})
    resp_b = client.post("/api/v1/auth/login", data={"username": "b@test.com", "password": "pass1234"})
    token_b = resp_b.json()["access_token"]
    resp = client.get(f"/api/v1/todos/{todo_id}", headers={"Authorization": f"Bearer {token_b}"})
    assert resp.status_code == 404
