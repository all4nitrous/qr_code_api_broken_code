import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_login_for_access_token():
    form_data = {
        "username": "admin",
        "password": "secret",
    }
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/token", data=form_data)
    assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.json()}"
    assert "access_token" in response.json(), "Missing 'access_token' in response"
    assert response.json()["token_type"] == "bearer"

@pytest.mark.asyncio
async def test_create_qr_code_unauthorized():
    qr_request = {
        "url": "https://example.com",
        "fill_color": "red",
        "back_color": "white",
        "size": 10,
    }
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/qr_codes/", json=qr_request)
    assert response.status_code == 401, f"Expected 401, got {response.status_code}: {response.json()}"

@pytest.mark.asyncio
async def test_create_and_delete_qr_code():
    form_data = {
        "username": "admin",
        "password": "secret",
    }
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Login and get the access token
        token_response = await ac.post("/token", data=form_data)
        assert token_response.status_code == 200, f"Expected 200, got {token_response.status_code}: {token_response.json()}"
        access_token = token_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {access_token}"}

        # Create a QR code
        qr_request = {
            "url": "https://example.com",
            "fill_color": "red",
            "back_color": "white",
            "size": 10,
        }
        create_response = await ac.post("/qr_codes/", json=qr_request, headers=headers)
        assert create_response.status_code in [201, 409], f"Expected 201 or 409, got {create_response.status_code}: {create_response.json()}"

        # If the QR code was created, delete it
        if create_response.status_code == 201:
            assert "qr_code_url" in create_response.json(), "Missing 'qr_code_url' in create response"
            qr_code_url = create_response.json()["qr_code_url"]
            qr_filename = qr_code_url.split('/')[-1]
            delete_response = await ac.delete(f"/qr_codes/{qr_filename}", headers=headers)
            assert delete_response.status_code == 204, f"Expected 204, got {delete_response.status_code}: {delete_response.json()}"
