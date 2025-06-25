from pydantic import BaseModel, Field
from typing import Optional,Literal

# Input schema for creating an order
class OrderCreate(BaseModel):
    customer_name: str = Field(..., max_length=100)
    item: str = Field(..., max_length=100)
    price: float

# Output schema for returning an order
class OrderOut(BaseModel):
    id: int
    customer_name: str
    item: str
    price: float
    status: str

    class Config:
        orm_mode = True

# Input schema for updating status
class UpdateStatus(BaseModel):
    status: Literal["Pending", "Shipped", "Delivered", "Cancelled"]