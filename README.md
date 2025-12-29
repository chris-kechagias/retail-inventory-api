# 🛒 Retail Product Inventory API

## Technology Badges

[![GitHub](https://img.shields.io/badge/GitHub-Repo-blue?style=flat-square&logo=github)](https://github.com/chris-kechagias/retail-inventory-api)
[![Python](https://img.shields.io/badge/Python-3.11+-blue?style=flat-square&logo=python)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-336791?style=flat-square&logo=postgresql)](https://www.postgresql.org/)
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

## 🚀 Getting Started

Follow these steps to get the project running on your local machine.

### 1. Prerequisites

- **Docker & Docker Compose** (for running the database)
- **Python 3.11+**
- **Git**

### 2. Installation

Clone the repository and navigate to the project folder:

```bash
git clone https://github.com/chris-kechagias/retail-inventory-api.git
cd retail-inventory-api
```

### 3. Environment Setup (Virtual Environment)

It is highly recommended (and often required on newer systems) to use a Python virtual environment to manage dependencies.

```bash
# 1. Create a virtual environment named 'venv'
python3 -m venv venv

# 2. Activate the virtual environment
source venv/bin/activate  # macOS/Linux
# .\venv\Scripts\activate  # Windows

# 3. Install dependencies
pip install -r requirements.txt
pip install "fastapi[standard]"
```

### 4. Database Setup (Docker)

Start the PostgreSQL database using Docker Compose. This containerizes the database so you don't need to install PostgreSQL directly on your system.

```bash
# Start the database in the background
docker-compose up -d db
```

_Note: The database runs on port `5432`._

### 5. Configuration

Create a `.env` file in the project root to tell the application how to connect to the local database:

**`.env` content:**

```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/retail_inventory_db
```

### 6. Run the API

Start the FastAPI development server. The application is configured to run on port **8000**.

```bash
# Ensure your virtual environment is activated
fastapi dev main.py --port 8000
```

- **API Root:** [http://127.0.0.1:8000](http://127.0.0.1:8000)
- **Interactive Docs (Swagger UI):** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc:** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 🐳 Running Fully in Docker

Alternatively, you can run the entire stack (App + Database) purely in Docker without local Python installation:

<!--  -->
<!--  -->

<!--  -->
<!--  -->
<!--  -->
<!--  -->
<!--  -->

```bash
docker-compose up --build
```

The API will be available at [http://localhost:8000](http://localhost:8000).

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

## 📝 Example Usage (Port 8000)

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

## 🛠️ Tech Stack

| Component     | Technology                          | Purpose                                        |
| :------------ | :---------------------------------- | :--------------------------------------------- |
| **Language**  | Python 3.11+                        | Primary development language.                  |
| **Framework** | FastAPI                             | High-performance async REST API framework.     |
| **ORM**       | SQLModel                            | Combines Pydantic validation + SQLAlchemy ORM. |
| **Database**  | PostgreSQL 15                       | Production-grade relational database.          |
| **Server**    | Uvicorn                             | ASGI server for running the application.       |
| **Logging**   | Python logging (`logger_config.py`) | Structured logging to console and file.        |

---

## 🏗️ Project Structure

```
retail-inventory-api/
├── main.py                   # Presentation Layer (FastAPI routes)
├── models.py                 # SQLModel schemas & database table
├── database.py               # PostgreSQL engine & session dependency
├── logger_config.py          # Logging configuration
├── requirements.txt          # Python dependencies
├── .env                      # Environment variables (local config)
├── docker-compose.yml        # Container orchestration (DB + App)
├── Dockerfile                # App container definition
├── LICENSE                   # MIT License
├── README.md                 # This file
├── DESIGN.md                 # Architecture & migration documentation
├── Procfile                  # Startup command for Render
└── logs/
    └── app.log               # Application logs
```

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
