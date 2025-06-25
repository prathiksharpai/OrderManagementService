from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app import crud, models, schemas, database

router = APIRouter()

# Dependency to get DB session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create Order
@router.post("/orders", response_model=schemas.OrderOut)
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    return crud.create_order(db, order)

# List Orders with pagination + price and status filtering
@router.get("/orders", response_model=list[schemas.OrderOut])
def list_orders(
    skip: int = 0,
    limit: int = 10,
    price_gt: float = Query(None, alias="min_price"),
    price_lt: float = Query(None, alias="max_price"),
    status: str = None,
    db: Session = Depends(get_db)
):
    return crud.list_orders(db, skip=skip, limit=limit, price_gt=price_gt, price_lt=price_lt, status=status)

# Get Order by ID
@router.get("/orders/{order_id}", response_model=schemas.OrderOut)
def get_order(order_id: int, db: Session = Depends(get_db)):
    order = crud.get_order_by_id(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

# Update Order Status
@router.patch("/orders/{order_id}/status")
def update_order_status(order_id: int, status: schemas.UpdateStatus, db: Session = Depends(get_db)):

    updated = crud.update_order_status(db, order_id, status.status)
    if not updated:
        raise HTTPException(status_code=404, detail="Order not found")
    return {"message": "Order status updated"}

@router.delete("/orders/{order_id}")
def delete_order(order_id: int, db: Session = Depends(database.get_db)):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    db.delete(order)
    db.commit()
    return {"message": "Order deleted"}
