# 🛒 Retail Product Inventory API

## Technology Badges

[![GitHub](https://img.shields.io/badge/GitHub-Repo-blue?style=flat-square&logo=github)](https://github.com/chris-kechagias/retail-api)
[![Python](https://img.shields.io/badge/Python-3.11+-blue?style=flat-square&logo=python)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-05998b?style=flat-square&logo=fastapi)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](https://opensource.org/licenses/MIT)
[![Deployment](https://img.shields.io/badge/Deployed%20on-Render-006494?style=flat-square&logo=render)](https://retail-api-MYAPP.onrender.com)

> **Note:** After deployment, replace `MYAPP` in the badge above with your actual Render app name.

## 🏆 Project Status

[![Last commit](https://img.shields.io/github/last-commit/chris-kechagias/retail-inventory-api?style=flat-square)](https://github.com/chris-kechagias/retail-inventory-api.git)
[![Top Language](https://img.shields.io/github/languages/top/chris-kechagias/retail-inventory-api?style=flat-square)](https://github.com/chris-kechagias/retail-inventory-api.git)
[![Repo size](https://img.shields.io/github/repo-size/chris-kechagias/retail-inventory-api?label=Repo%20Size&style=flat-square)](https://github.com/chris-kechagias/retail-inventory-api.git)
[![Deployment Status](https://img.shields.io/badge/Deployed%20on-Render-006494?style=flat-square&logo=render)](https://YOUR-RENDER-URL)

---

## 🎯 Project Goal: Three-Tier Architecture MVP

This project is a **Minimal Viable Product (MVP)** of a Retail Product Inventory Management System, built to demonstrate production-ready **Three-Tier Architecture** and foundational API engineering skills required for an **AI Engineer** role.

The core objective was ensuring clear **separation of concerns** across the codebase:

- **Presentation Layer (`main.py`):** Handles HTTP routing, request/response validation, and delegates to business logic.
- **Business Logic Layer (`inventory_service.py`):** Contains core business rules (ID generation, product modifications, inventory calculations).
- **Data Access Layer (`inventory_io.py`):** Manages all read/write operations with the `products.json` file.
- **Data Modeling Layer (`models.py`):** Defines Pydantic schemas for request/response validation and type safety.

---

## 💡 Why I Built This

This project demonstrates:

- **RESTful API design** with proper HTTP semantics (201 for creation, 204 for deletion, 404 for not found)
- **Three-tier architecture** with clear separation of concerns
- **Production-ready code** with comprehensive logging, error handling, and data validation
- **Pydantic for data validation** - critical skill for AI/ML data pipelines
- **FastAPI framework** - chosen for its async capabilities, automatic OpenAPI documentation, and performance

Built as part of my career transition from retail management to AI Engineering, this project showcases foundational backend skills before advancing to LLM engineering, RAG systems, and production ML deployments.

**Background:** 15 years in retail operations management + B.Eng. in Automation & Control Engineering (2010) + AI thesis on neural network computer vision. Now building the technical portfolio to break into AI Engineering.

---

## 🛠️ Tech Stack

| Component       | Technology     | Purpose                                                       |
| :-------------- | :------------- | :------------------------------------------------------------ |
| **Language**    | Python 3.11+   | Primary development language.                                 |
| **Framework**   | FastAPI        | High-performance, asynchronous RESTful API framework.         |
| **Validation**  | Pydantic       | Request/response validation, type safety, auto-documentation. |
| **Server**      | Uvicorn        | ASGI server for running the application.                      |
| **Persistence** | JSON File      | Simple local persistence for the MVP (future: PostgreSQL).    |
| **Logging**     | Python logging | Structured logging to console and file for debugging.         |

---

## ✨ Features (Full CRUD)

The API provides complete CRUD (Create, Read, Update, Delete) capability for product data, with professional HTTP status codes and comprehensive error handling:

| Method   | Endpoint                | Description                                          | Status Codes     |
| :------- | :---------------------- | :--------------------------------------------------- | :--------------- |
| `GET`    | `/products`             | Retrieves a list of all products.                    | 200              |
| `GET`    | `/products/{id}`        | Retrieves a single product by ID.                    | 200, **404**     |
| `GET`    | `/products/total_value` | Calculates total monetary value (Price × Quantity).  | 200              |
| `POST`   | `/products`             | Creates a new product with auto-generated unique ID. | **201**          |
| `PUT`    | `/products/{id}`        | Updates the quantity of an existing product.         | 200, **404**     |
| `DELETE` | `/products/{id}`        | Deletes a product by ID.                             | **204**, **404** |

---

## 🚀 Getting Started (Local Setup)

### 1. Prerequisites

- **Python 3.11+** installed
- **Git** for cloning the repository

### 2. Installation

1. Clone the repository:

```bash
   git clone https://github.com/chris-kechagias/retail-inventory-api.git
   cd retail-inventory-api
```

2. Create and activate a virtual environment:

```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
   pip install -r requirements.txt
```

### 3. Running the API

Start the development server:

```bash
fastapi dev main.py
```

The API will be available at: **http://127.0.0.1:8000**

### 4. Interactive API Documentation

FastAPI automatically generates interactive documentation:

- **Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc:** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 📝 Example Usage

### Create a Product

```bash
curl -X POST "http://127.0.0.1:8000/products" \
  -H "Content-Type: application/json" \
  -d '{
    "id": 1,
    "name": "Laptop",
    "price": 999.99,
    "quantity": 10,
    "in_stock": true
  }'
```

### Get All Products

```bash
curl "http://127.0.0.1:8000/products"
```

### Get Single Product

```bash
curl "http://127.0.0.1:8000/products/1"
```

### Update Product Quantity

```bash
curl -X PUT "http://127.0.0.1:8000/products/1" \
  -H "Content-Type: application/json" \
  -d '{"quantity": 5}'
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
retail-api/
├── main.py                 # Presentation Layer (FastAPI routes)
├── models.py               # Pydantic data models & validation
├── inventory_service.py    # Business Logic Layer
├── inventory_io.py         # Data Access Layer (JSON I/O)
├── logger_config.py        # Logging configuration
├── requirements.txt        # Python dependencies
├── README.md               # This file
├── DESIGN.md               # Architecture & design decisions
├── .gitignore              # Git ignore rules
├── data/
│   └── products.json       # JSON data store
└── logs/
    └── app.log             # Application logs
```

---

## 🔮 Future Enhancements

- [ ] Replace JSON storage with PostgreSQL database
- [ ] Add user authentication & authorization (JWT)
- [ ] Implement pagination for product listings
- [ ] Add search & filter functionality
- [ ] Deploy with Docker containerization
- [ ] Add CI/CD pipeline (GitHub Actions)
- [ ] Implement rate limiting
- [ ] Add comprehensive unit & integration tests

---

## 📜 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## 👤 Author

**Chris Kechagias**  
Transitioning from Automation Engineer with Retail Management Experience to AI Engineering  
📍 Thessaloniki, Greece  
🔗 [GitHub](https://github.com/chris-kechagias) | [LinkedIn](https://www.linkedin.com/in/chkechagias)

---

## 🙏 Acknowledgments

Built as part of a self-directed AI Engineering roadmap (Nov 2025 - Sep 2026). This project represents Week 2 of Phase 0 (Foundations), demonstrating backend API development skills before advancing to LLM engineering and RAG systems.

Special thanks to the FastAPI and Pydantic communities for excellent documentation.
