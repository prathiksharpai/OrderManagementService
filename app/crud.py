from sqlalchemy.orm import Session
from . import models, schemas

# Create a new order
def create_order(db: Session, order: schemas.OrderCreate):
    db_order = models.Order(**order.dict())
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

# Get order by ID
def get_order_by_id(db: Session, order_id: int):
    return db.query(models.Order).filter(models.Order.id == order_id).first()

# List orders with pagination and optional price/status filtering
def list_orders(
    db: Session,
    skip: int = 0,
    limit: int = 10,
    price_gt: float = None,
    price_lt: float = None,
    status: str = None
):
    query = db.query(models.Order)

    if price_gt is not None:
        query = query.filter(models.Order.price > price_gt)
    if price_lt is not None:
        query = query.filter(models.Order.price < price_lt)
    if status is not None:
        query = query.filter(models.Order.status == status)

    return query.offset(skip).limit(limit).all()

# Update order status
def update_order_status(db: Session, order_id: int, new_status: str):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if order:
        order.status = new_status
        db.commit()
        db.refresh(order)
    return order
