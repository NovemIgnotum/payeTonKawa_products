import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from app.main import app
from app.routes.products import get_db

client = TestClient(app)

class MockProduct:
    name = "TestProduct"
    price = 10.5
    stock_quantity = 5
    created_at = "2024-08-03T10:00:00+00:00"
    updated_at = "2024-08-03T10:00:00+00:00"
    id = 1

def override_get_db_create():
    db = MagicMock()
    db.query().filter().first.return_value = None
    db.add.return_value = None
    db.commit.return_value = None
    db.refresh.side_effect = lambda obj: setattr(obj, "id", 1)
    db.refresh.return_value = None
    yield db

def override_get_db_exists():
    db = MagicMock()
    db.query().filter().first.return_value = MockProduct()
    yield db

def override_get_db_get():
    db = MagicMock()
    db.query().filter().first.return_value = MockProduct()
    yield db

def override_get_db_list():
    db = MagicMock()
    db.query().all.return_value = [MockProduct(), MockProduct()]
    yield db

def override_get_db_update():
    db = MagicMock()
    db.query().filter().first.return_value = MockProduct()
    db.commit.return_value = None
    db.refresh.return_value = None
    yield db

def override_get_db_delete():
    db = MagicMock()
    db.query().filter().first.return_value = MockProduct()
    db.delete.return_value = None
    db.commit.return_value = None
    yield db

# Test POST /products (success)
def test_create_product_success():
    app.dependency_overrides[get_db] = override_get_db_create
    payload = {
        "name": "TestProduct",
        "price": 10.5,
        "stock_quantity": 5
    }
    response = client.post("/api/products", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["message"] == "Product created successfully."
    assert data["product"]["name"] == "TestProduct"

# Test POST /products (already exists)
def test_create_product_already_exists():
    app.dependency_overrides[get_db] = override_get_db_exists
    payload = {
        "name": "TestProduct",
        "price": 10.5,
        "stock_quantity": 5
    }
    response = client.post("/api/products", json=payload)
    assert response.status_code == 400
    data = response.json()
    assert data["message"] == "Product with this name already exists."

# Test GET /products/{product_id}
def test_get_product_success():
    app.dependency_overrides[get_db] = override_get_db_get
    response = client.get("/api/products/1")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Product retrieved successfully."
    assert data["product"]["id"] == 1

# Test GET /products/{product_id} not found
def test_get_product_not_found():
    def override():
        db = MagicMock()
        db.query().filter().first.return_value = None
        yield db
    app.dependency_overrides[get_db] = override
    response = client.get("/api/products/999")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Product not found"

# Test GET /products (list)
def test_get_products_list():
    app.dependency_overrides[get_db] = override_get_db_list
    response = client.get("/api/products")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "All products retrieved successfully."
    assert isinstance(data["product"], list)
    assert len(data["product"]) == 2

# Test PUT /products/{product_id}
def test_update_product_success():
    app.dependency_overrides[get_db] = override_get_db_update
    payload = {
        "price": 20.0,
        "stock_quantity": 10
    }
    response = client.put("/api/products/1", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Product updated successfully."
    assert data["product"]["id"] == 1

# Test PUT /products/{product_id} not found
def test_update_product_not_found():
    def override():
        db = MagicMock()
        db.query().filter().first.return_value = None
        yield db
    app.dependency_overrides[get_db] = override
    payload = {
        "price": 20.0,
        "stock_quantity": 10
    }
    response = client.put("/api/products/999", json=payload)
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Product not found"

# Test DELETE /products/{product_id}
def test_delete_product_success():
    app.dependency_overrides[get_db] = override_get_db_delete
    response = client.delete("/api/products/1")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Product deleted successfully."
    assert data["product"]["id"] == 1

# Test DELETE /products/{product_id} not found
def test_delete_product_not_found():
    def override():
        db = MagicMock()
        db.query().filter().first.return_value = None
        yield db
    app.dependency_overrides[get_db] = override
    response = client.delete("/api/products/999")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Product not found"


