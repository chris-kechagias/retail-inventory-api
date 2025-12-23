# 🛒 Retail Product Inventory API

## Technology Badges

[![GitHub](https://img.shields.io/badge/GitHub-Repo-blue?style=flat-square&logo=github)](https://github.com/chris-kechagias/retail-inventory-api)
[![Python](https://img.shields.io/badge/Python-3.11+-blue?style=flat-square&logo=python)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-18-336791?style=flat-square&logo=postgresql)](https://www.postgresql.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-05998b?style=flat-square&logo=fastapi)](https://fastapi.tiangolo.com/)
[![SQLModel](https://img.shields.io/badge/SQLModel-0.0.22-00b0ff?style=flat-square&logo=pydantic)](https://sqlmodel.tiangolo.com/)
[![Dockerfile](https://img.shields.io/badge/container-Dockerfile-2496ED?style=flat-square&logo=docker)](https://docs.docker.com/engine/reference/builder/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](https://opensource.org/licenses/MIT)

---

## 🎯 Project Goal

A **production-ready REST API** for retail inventory management, demonstrating modern Python backend architecture with PostgreSQL persistence.

**Architecture:**

- **Presentation Layer (`main.py`):** FastAPI routes, HTTP request/response handling, dependency injection.
- **Data Layer (`database.py`):** PostgreSQL connection, session management, SQLModel engine.
- **Schema Layer (`models.py`):** SQLModel classes serving dual purpose - Pydantic validation AND SQLAlchemy ORM.

---

## 💡 Why I Built This

This project demonstrates:

- **RESTful API design** with proper HTTP semantics (201 for creation, 204 for deletion, 404 for not found)
- **PostgreSQL integration** with SQLModel ORM for type-safe database operations
- **Production-ready patterns** including dependency injection, environment variables, and structured logging
- **SQLModel** - combining Pydantic validation + SQLAlchemy ORM in a single class
- **Database-side aggregation** - using SQL `func.sum()` for performant calculations

Built as part of my career transition from retail management to AI Engineering. This v2.0 upgrade from JSON to PostgreSQL demonstrates database integration skills essential for production ML systems.

**Background:** 15 years in retail operations + B.Eng. in Automation & Control Engineering (2010) + AI thesis on neural network computer vision.

---

## 🛠️ Tech Stack

| Component     | Technology                          | Purpose                                        |
| :------------ | :---------------------------------- | :--------------------------------------------- |
| **Language**  | Python 3.11+                        | Primary development language.                  |
| **Framework** | FastAPI                             | High-performance async REST API framework.     |
| **ORM**       | SQLModel                            | Combines Pydantic validation + SQLAlchemy ORM. |
| **Database**  | PostgreSQL 18                       | Production-grade relational database.          |
| **Server**    | Uvicorn                             | ASGI server for running the application.       |
| **Logging**   | Python logging (`logger_config.py`) | Structured logging to console and file.        |

---

## ✨ Features (Full CRUD)

| Method   | Endpoint                | Description                                 | Status Codes |
| :------- | :---------------------- | :------------------------------------------ | :----------- |
| `GET`    | `/products`             | List all products with pagination.          | 200          |
| `GET`    | `/products/{id}`        | Retrieve a single product by ID.            | 200, 404     |
| `GET`    | `/products/total_value` | Calculate total inventory value (SQL-side). | 200          |
| `POST`   | `/products`             | Create a new product (ID auto-generated).   | 201          |
| `PATCH`  | `/products/{id}`        | Partial update of product fields.           | 200, 404     |
| `DELETE` | `/products/{id}`        | Delete a product by ID.                     | 204, 404     |

---

## 🚀 Getting Started

### 1. Prerequisites

- **Python 3.11+**
- **PostgreSQL 18** installed and running
- **Git**

### 2. Installation

```bash
git clone https://github.com/chris-kechagias/retail-inventory-api.git
cd retail-inventory-api
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Database Setup

1. Create a PostgreSQL database:

```sql
CREATE DATABASE retail_inventory;
```

2. Create a `.env` file in the project root:

```
DATABASE_URL=postgresql+psycopg2://postgres:YOUR_PASSWORD@localhost/retail_inventory
```

### 4. Run the API

```bash
fastapi dev main.py
```

API available at: **[http://127.0.0.1:8000](https://retail-inventory-api-chris.onrender.com)**

### 5. Interactive Documentation

- **Swagger UI:** [http://127.0.0.1:8000/docs](https://retail-inventory-api-chris.onrender.com/docs)
- **ReDoc:** [http://127.0.0.1:8000/redoc
](https://retail-inventory-api-chris.onrender.com/redoc)
---

## 📝 Example Usage

### Create a Product

```bash
curl -X POST "http://127.0.0.1:8000/products" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Laptop",
    "price": 999.99,
    "quantity": 10
  }'
```

### Get All Products (with pagination)

```bash
curl "http://127.0.0.1:8000/products?offset=0&limit=10"
```

### Get Single Product

```bash
curl "http://127.0.0.1:8000/products/1"
```

### Update Product (Partial)

```bash
curl -X PATCH "http://127.0.0.1:8000/products/1" \
  -H "Content-Type: application/json" \
  -d '{"quantity": 5, "in_stock": false}'
```

### Calculate Total Inventory Value

```bash
curl "http://127.0.0.1:8000/products/total_value"
```

### Delete a Product

```bash
curl -X DELETE "http://127.0.0.1:8000/products/1"
```

---

## 🏗️ Project Structure

```
retail-inventory-api/
├── main.py                   # Presentation Layer (FastAPI routes)
├── models.py                 # SQLModel schemas & database table
├── database.py               # PostgreSQL engine & session dependency
├── logger_config.py          # Logging configuration
├── requirements.txt          # Python dependencies
├── .env                      # Environment variables (not in git)
├── LICENSE                   # MIT License
├── README.md                 # This file
├── DESIGN.md                 # Architecture & migration documentation
├── .gitignore                # Git ignore rules
├── Dockerfile                # Container build instructions
├── Procfile                  # Startup command for Render
└── logs/
    └── app.log               # Application logs
```

---

## 🔮 Future Enhancements

- [x] Replace JSON storage with PostgreSQL database ✅
- [x] Implement pagination for product listings ✅
- [ ] Add user authentication & authorization (JWT)
- [ ] Add search & filter functionality
- [ ] Deploy updated version to Render
- [ ] Add CI/CD pipeline (GitHub Actions)
- [ ] Implement rate limiting
- [ ] Add comprehensive unit & integration tests

---

## 📜 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## 👤 Author

**Chris Kechagias**  
Automation Engineer transitioning to AI Engineering  
📍 Thessaloniki, Greece  
🔗 [GitHub](https://github.com/chris-kechagias) | [LinkedIn](https://www.linkedin.com/in/chkechagias)

---

## 🙏 Acknowledgments

Built as part of a self-directed AI Engineering roadmap (Nov 2025 - Sep 2026). This v2.0 release represents Phase 0 completion - demonstrating PostgreSQL integration before advancing to LLM engineering and RAG systems in Phase 1.

Special thanks to FastAPI, SQLModel, and PostgreSQL communities for excellent documentation.
