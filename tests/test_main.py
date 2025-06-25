from fastapi.testclient import TestClient
from app.main import app
from app import models, database
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Test database URL
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:Prathiksha%4021@localhost/orderdb"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override dependency
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

models.Base.metadata.create_all(bind=engine)
app.dependency_overrides[database.get_db] = override_get_db

client = TestClient(app)

# Test: Create Order
def test_create_order():
    response = client.post("/orders", json={
        "customer_name": "Test User",
        "item": "Test Product",
        "price": 199.99
    })
    assert response.status_code == 200
    data = response.json()
    assert data["customer_name"] == "Test User"
    assert data["item"] == "Test Product"
    assert data["price"] == 199.99

# Test: List Orders
def test_list_orders():
    response = client.get("/orders")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

# Test: Update Order Status
def test_update_order_status():
    create_res = client.post("/orders", json={
        "customer_name": "Status User",
        "item": "Status Item",
        "price": 300.00
    })
    order_id = create_res.json()["id"]

    update_res = client.patch(f"/orders/{order_id}/status", json={"status": "Shipped"})
    assert update_res.status_code == 200
    assert update_res.json()["message"] == "Order status updated"

# Test: Price Filtering
def test_price_filtering():
    client.post("/orders", json={"customer_name": "Filter User", "item": "Filter Item", "price": 150})
    response = client.get("/orders?min_price=100&max_price=200")
    assert response.status_code == 200
    for order in response.json():
        assert 100 <= order["price"] <= 200

# Test: Search by Item Name
def test_search_orders():
    client.post("/orders", json={"customer_name": "Search User", "item": "SpecialItem", "price": 250})
    response = client.get("/orders?search=SpecialItem")
    assert response.status_code == 200
    found = any("SpecialItem" in order["item"] for order in response.json())
    assert found

# Test: Invalid Order ID for Status Update
def test_update_invalid_order_status():
    response = client.patch("/orders/999999/status", json={"status": "Delivered"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Order not found"

# Test: Delete Order
def test_delete_order():
    # Step 1: Create an order
    create_res = client.post("/orders", json={
        "customer_name": "Delete User",
        "item": "Delete Item",
        "price": 180
    })
    assert create_res.status_code == 200
    order_id = create_res.json()["id"]

    # Step 2: Delete the order
    delete_res = client.delete(f"/orders/{order_id}")
    assert delete_res.status_code == 200
    assert delete_res.json()["message"] == "Order deleted"

    # Step 3: Confirm deletion (optional)
    get_res = client.get(f"/orders/{order_id}")
    assert get_res.status_code == 404