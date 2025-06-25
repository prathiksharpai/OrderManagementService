# 🧾 Order Management Service(FastAPI + MySQL)

This is a backend RESTful API for managing product orders, built with **FastAPI**, **MySQL**, and **SQLAlchemy**. It supports full CRUD operations, pagination, filtering, and unit testing.

---

## ⚙️ Tech Stack

| Layer        | Tool/Library         |
|--------------|----------------------|
| Framework    | FastAPI              |
| ORM          | SQLAlchemy           |
| Database     | MySQL                |
| Validation   | Pydantic             |
| Testing      | Pytest + TestClient  |

---

## 📦 Features

- ✅ Create, Read, Update, Delete (CRUD) for orders
- ✅ Price range and status filtering
- ✅ Pagination (`skip`, `limit`)
- ✅ Update order status
- ✅ Proper error handling
- ✅ Unit tests using test database
- ✅ Dockerized with `docker-compose`

---

## 🚀 Getting Started

### ⚙️ 1. Clone the Repository

git clone https://github.com/yourusername/order-management-api.git

cd order-management-api

###  2. Local Setup 

#### Install dependencies

python -m venv venv

source venv/bin/activate   

pip install -r requirements.txt

### Run MySQL locally (or use MySQL Workbench)

CREATE DATABASE orders_db;

### Run FastAPI

uvicorn app.main:app --reload

Visit http://localhost:8000/docs

---

## 🔗 API Endpoints

### 🔹 Create Order

POST /orders
Body:

{
  "customer_name": "Alice",
  
  "product": "Keyboard",
  
  "price": 199.99,
  
  "status": "Pending"
}

### 🔹 Get All Orders

GET /orders?skip=0&limit=5&min_price=100&max_price=500&status=Pending

### 🔹 Get Order by ID

GET /orders/{order_id}

### 🔹 Update Order Status

PATCH /orders/{order_id}/status

Body:

{
  "status": "Shipped"
}
### 🔹 Delete Order

DELETE /orders/{order_id}

### Running Unit Tests

Use a test DB or SQLite for tests.

pytest tests/test_main.py
