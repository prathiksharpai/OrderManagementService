def test_create_order():
    from app.schemas import OrderCreate
    order = OrderCreate(customer_name="Test", item="Item", price=20.5)
    assert order.customer_name == "Test"
