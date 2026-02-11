# 🛒 Retail Product Inventory API

REST API for retail inventory management built while learning modern Python backend development. FastAPI + PostgreSQL + Docker deployment.

---

## Tech Stack

![Python](https://img.shields.io/badge/Python-3.11%2B-blue?style=flat-square&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115%2B-009688?style=flat-square&logo=fastapi)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-336791?style=flat-square&logo=postgresql)
![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED?style=flat-square&logo=docker)
![SQLModel](https://img.shields.io/badge/SQLModel-ORM-red?style=flat-square)

## Status

![Deployment](https://img.shields.io/website?url=https%3A%2F%2Fretail-inventory-api-chris.onrender.com&label=Live%20API&style=flat-square)
![Last Commit](https://img.shields.io/github/last-commit/chris-kechagias/retail-inventory-api?style=flat-square)
![Commits](https://img.shields.io/github/commit-activity/m/chris-kechagias/retail-inventory-api?style=flat-square&label=Activity)
![License](https://img.shields.io/github/license/chris-kechagias/retail-inventory-api?style=flat-square)

---

## Table of Contents

- [🛒 Retail Product Inventory API](#-retail-product-inventory-api)
  - [Tech Stack](#tech-stack)
  - [Status](#status)
  - [Table of Contents](#table-of-contents)
  - [About](#about)
  - [Features](#features)
  - [Demo](#demo)
  - [Installation](#installation)
    - [Prerequisites](#prerequisites)
    - [Clone the Repository](#clone-the-repository)
    - [Option 1: Local Setup (Virtual Environment)](#option-1-local-setup-virtual-environment)
    - [Option 2: Full Docker Setup](#option-2-full-docker-setup)
  - [Usage](#usage)
    - [Testing the API](#testing-the-api)
  - [API Endpoints](#api-endpoints)
  - [Testing](#testing)
    - [Running Tests](#running-tests)
    - [Test Suite](#test-suite)
  - [Configuration](#configuration)
    - [Environment Variables](#environment-variables)
    - [Docker Compose Configuration](#docker-compose-configuration)
  - [Project Structure](#project-structure)
    - [Architecture Overview](#architecture-overview)
  - [Tech Stack Details](#tech-stack-details)
  - [License](#license)
  - [Acknowledgements](#acknowledgements)
  - [Author](#author)

---

## About

A REST API for managing retail product inventory, built as part of my AI Engineering career transition roadmap.

**Learning objectives:**
- Master modern Python backend patterns
- Practice database-backed architecture (PostgreSQL vs JSON files)
- Learn Docker containerization for deployment
- Build portfolio demonstrating backend engineering skills

**Context:**
This project represents Phase 0 completion (Nov-Dec 2025) in a structured 10-month career transition from retail operations management to AI Engineering. Built with 15 years of retail inventory management experience, applying real-world operational knowledge to technical implementation.

**🔗 Live API:** https://retail-inventory-api-chris.onrender.com

**📚 Interactive Docs:** https://retail-inventory-api-chris.onrender.com/docs

---

## Features

-  Complete CRUD operations for product inventory
-  PostgreSQL database with SQLModel ORM (Supabase)
-  Docker containerization with Docker Compose
-  Comprehensive logging infrastructure
-  Pydantic validation on all endpoints
-  Deployed on Render with live documentation
-  SQL-based total inventory value calculation
-  Pagination support for product listings
-  Health check endpoint with uptime tracking
-  Comprehensive test suite with pytest

---

## Demo

**Interactive API Documentation:**

Visit the live Swagger UI to test all endpoints directly in your browser:
👉 **https://retail-inventory-api-chris.onrender.com/docs**

**Example API Response:**

```json
{
  "id": 1,
  "name": "Laptop",
  "price": 999.99,
  "quantity": 10,
  "in_stock": true
}
```

---

## Installation

### Prerequisites

- Python 3.11+
- Docker & Docker Compose
- Git
- PostgreSQL 15 (if running without Docker)

### Clone the Repository

```bash
git clone https://github.com/chris-kechagias/retail-inventory-api.git
cd retail-inventory-api
```

### Option 1: Local Setup (Virtual Environment)

**1. Create and activate virtual environment:**

```bash
# Create virtual environment
python3 -m venv venv

# Activate (macOS/Linux)
source venv/bin/activate

# Activate (Windows)
.\venv\Scripts\activate
```

**2. Install dependencies:**

```bash
pip install -r requirements.txt
pip install "fastapi[standard]"
```

**3. Start PostgreSQL database (Docker):**

```bash
docker-compose up -d db
```

**4. Configure environment variables:**

Create `.env` file in project root:

```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/retail_inventory_db
```

**5. Run the application:**

```bash
fastapi dev main.py --port 8000
```

**Access points:**
- API Root: http://127.0.0.1:8000
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

---

### Option 2: Full Docker Setup

Run the entire stack (App + Database) in Docker:

```bash
docker-compose up --build
```

The API will be available at http://localhost:8000

---

## Usage

### Testing the API

**1. Create a product:**

```bash
curl -X POST "http://127.0.0.1:8000/products" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Laptop",
    "price": 999.99,
    "quantity": 10
  }'
```

**2. Get all products (with pagination):**

```bash
curl "http://127.0.0.1:8000/products?offset=0&limit=10"
```

**3. Get single product:**

```bash
curl "http://127.0.0.1:8000/products/1"
```

**4. Update product:**

```bash
curl -X PATCH "http://127.0.0.1:8000/products/1" \
  -H "Content-Type: application/json" \
  -d '{"quantity": 5, "in_stock": false}'
```

**5. Calculate total inventory value:**

```bash
curl "http://127.0.0.1:8000/products/total_value"
```

**6. Delete product:**

```bash
curl -X DELETE "http://127.0.0.1:8000/products/1"
```

---

## API Endpoints

| Method | Endpoint                | Description                                   | Status Codes |
| ------ | ----------------------- | --------------------------------------------- | ------------ |
| GET    | `/`                     | API info and documentation links              | 200          |
| GET    | `/health`               | Health check with status, version, and uptime | 200          |
| GET    | `/products`             | List all products with pagination             | 200          |
| GET    | `/products/{id}`        | Get single product by ID                      | 200, 404     |
| GET    | `/products/total_value` | Calculate total inventory value (SQL)         | 200          |
| POST   | `/products`             | Create new product                            | 201          |
| PATCH  | `/products/{id}`        | Partial update of product                     | 200, 404     |
| DELETE | `/products/{id}`        | Delete product by ID                          | 204, 404     |

**All endpoints documented interactively at `/docs`**

---

## Testing

The project includes a comprehensive test suite using **pytest** and FastAPI's **TestClient**.

### Running Tests

**1. Install test dependencies:**

```bash
pip install pytest pytest-cov
```

**2. Run all tests:**

```bash
pytest tests/
```

**3. Run tests with coverage:**

```bash
pytest tests/ --cov=. --cov-report=term-missing
```

### Test Suite

The test suite (`tests/test_api.py`) includes:

| Test                            | Purpose                                                       |
| ------------------------------- | ------------------------------------------------------------- |
| `test_health`                   | Validates health endpoint returns status, version, and uptime |
| `test_cloud_connection`         | Verifies database connection via GET /products                |
| `test_create_product`           | Tests product creation with POST /products                    |
| `test_read_single_product`      | Tests retrieving a specific product by ID                     |
| `test_read_nonexistent_product` | Validates 404 response for invalid product IDs                |
| `test_create_product_invalid`   | Tests validation errors (422) for invalid data                |

**Coverage:**
- Health check endpoint
- Database connectivity
- CRUD operations
- Error handling (404, 422)
- Data validation

---

## Configuration

### Environment Variables

The application requires a `.env` file with database connection details:

```env
DATABASE_URL=postgresql://user:password@host:port/database_name
```

**Example for local development:**

```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/retail_inventory_db
```

**Example for Supabase (production):**

```env
DATABASE_URL=postgresql://user:password@db.supabase.co:5432/postgres
```

**Example for Render deployment:**

```env
DATABASE_URL=postgresql://user:password@hostname.render.com/database
```

### Docker Compose Configuration

Database settings are defined in `docker-compose.yml`:

```yaml
environment:
  POSTGRES_USER: postgres
  POSTGRES_PASSWORD: password
  POSTGRES_DB: retail_inventory_db
ports:
  - "5432:5432"
```

---

## Project Structure

```
retail-inventory-api/
├── main.py                   # FastAPI routes and application entry
├── models.py                 # SQLModel schemas and database tables
├── database.py               # PostgreSQL engine and session management
├── logger_config.py          # Logging configuration
├── requirements.txt          # Python dependencies
├── .env                      # Environment variables (not in repo)
├── .env.example              # Template for environment setup
├── docker-compose.yml        # Container orchestration
├── Dockerfile                # Application container definition
├── Procfile                  # Render deployment startup command
├── LICENSE                   # MIT License
├── README.md                 # This file
├── DESIGN.md                 # Architecture and migration notes
├── tests/
│   ├── __init__.py          # Test package initialization
│   └── test_api.py          # API endpoint test suite
└── logs/
    └── app.log               # Application logs
```

### Architecture Overview

**Presentation Layer (`main.py`):**
FastAPI routes, HTTP request/response handling, dependency injection

**Data Layer (`database.py`):**
PostgreSQL connection, session management, SQLModel engine

**Schema Layer (`models.py`):**
SQLModel classes serving dual purpose - Pydantic validation AND SQLAlchemy ORM

---

## Tech Stack Details

| Component        | Technology               | Purpose                                       |
| ---------------- | ------------------------ | --------------------------------------------- |
| Language         | Python 3.11+             | Primary development language                  |
| Framework        | FastAPI                  | High-performance async REST API               |
| ORM              | SQLModel                 | Combines Pydantic validation + SQLAlchemy ORM |
| Database         | PostgreSQL 15 (Supabase) | Production-grade relational database          |
| Server           | Uvicorn                  | ASGI server for FastAPI                       |
| Containerization | Docker + Docker Compose  | Consistent deployment environments            |
| Deployment       | Render                   | Cloud hosting platform                        |
| Database Hosting | Supabase                 | Managed PostgreSQL database                   |
| Testing          | pytest + TestClient      | Automated API testing                         |
| Logging          | Python logging           | Structured logging to console and file        |

**Why These Choices:**

- **FastAPI:** Modern async framework, automatic API documentation, excellent performance
- **SQLModel:** Type-safe database interactions, combines validation and ORM in one tool
- **PostgreSQL:** Industry-standard relational database, ACID compliance, scalability
- **Docker:** Ensures consistent environments from development to production

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Acknowledgements

**Mentorship:**
Special thanks to [qquorum](https://github.com/qquorum), Senior Software Developer for:
- Code review and Docker improvements
- Direct contributions to project architecture

**Project Context:**
Built during Phase 0 (Nov-Dec 2025) of my AI Engineering career transition roadmap. This project demonstrates backend development fundamentals before advancing to LLM engineering, RAG systems, and AI agent development in Phase 1 (Jan-Mar 2026).

**Career Background:**
Transitioning from 15 years of retail operations management (H&M, Adidas, Luigi Footwear) to AI Engineering, building on B.Eng. in Automation & Control Engineering (2010) and neural network computer vision thesis background.

---

## Author

**Chris Kechagias**
Learning AI Engineering | Thessaloniki, Greece

🔗 [GitHub](https://github.com/chris-kechagias) | [LinkedIn](https://www.linkedin.com/in/chris-kechagias)

*Career-changing from retail operations to AI engineering. Building technical skills to combine domain expertise with AI/ML development.*

---

**⭐ If you find this project helpful, consider giving it a star!**
