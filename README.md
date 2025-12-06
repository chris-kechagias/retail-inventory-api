# 🛒 Retail Product Inventory API (FastAPI)

## 🏆 Project Status & Technology Badges

[![GitHub](https://img.shields.io/badge/GitHub-Repo-blue?style=flat-square&logo=github)](https://github.com/YOUR-GITHUB-USERNAME/retail-api)
[![Python](https://img.shields.io/badge/Python-3.11+-blue?style=flat-square&logo=python)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-05998b?style=flat-square&logo=fastapi)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](https://opensource.org/licenses/MIT)
[![Deployment](https://img.shields.io/badge/Deployed%20on-Render-006494?style=flat-square&logo=render)](https://YOUR-RENDER-URL)

---

## 🎯 Project Goal: Three-Tier Architecture MVP

This project is a Minimal Viable Product (MVP) of a Retail Product Inventory Management System.

It was built to demonstrate a production-ready **Three-Tier Architecture**

[Image of Three-Tier Architecture]
and foundational API engineering skills required for an **AI Engineer** role. The core objective was ensuring clear **separation of concerns** across the codebase:

- **Presentation Layer (`main.py`):** Handles routing, request/response validation, and delegates business logic.
- **Business Logic Layer (`inventory_service.py`):** Contains core business rules (e.g., ID generation, product modification, calculating inventory value).
- **Data Access Layer (`inventory_io.py`):** Manages read/write operations with the `products.json` file.
- **Data Modeling Layer (`models.py`):** Defines the Pydantic schemas for request/response validation and internal data structure.

---

## 🛠️ Tech Stack

| Component       | Technology   | Purpose                                                       |
| :-------------- | :----------- | :------------------------------------------------------------ |
| **Language**    | Python 3.11+ | Primary development language.                                 |
| **Framework**   | FastAPI      | High-performance, asynchronous RESTful API framework.         |
| **Validation**  | Pydantic     | **Crucial for API validation (`models.py`) and data typing.** |
| **Server**      | Uvicorn      | ASGI server for running the application.                      |
| **Persistence** | JSON File    | Simple local persistence for the MVP.                         |

---

## ✨ Features (CRUD Functionality)

The API provides full CRUD (Create, Read, Update, Delete) capability for product data, with professional HTTP status codes and error handling:

| Method   | Endpoint          | Description                                                                   | Status Codes     |
| :------- | :---------------- | :---------------------------------------------------------------------------- | :--------------- |
| `GET`    | `/products`       | Retrieves a list of all products.                                             | 200              |
| `GET`    | `/products/{id}`  | Retrieves a single product by ID.                                             | 200, **404**     |
| `GET`    | `/products/value` | **Calculates the total monetary value of all inventory (Price \* Quantity).** | 200              |
| `POST`   | `/products`       | Creates a new product and assigns a unique ID.                                | **201**          |
| `PUT`    | `/products/{id}`  | Updates the quantity of an existing product.                                  | 200, **404**     |
| `DELETE` | `/products/{id}`  | Deletes a product by ID.                                                      | **204**, **404** |

---

## 🚀 Getting Started (Local Setup)

### 1. Prerequisites

You must have **Python 3.11+** installed.

### 2. Setup and Installation

1.  Clone the repository:

    ```bash
    git clone [YOUR-REPO-URL]
    cd retail-api
    ```

2.  Create a virtual environment and activate it:

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4.  Run the application:
    ```bash
    fastapi dev main.py
    ```

### 3. API Documentation

Once running, access the interactive API documentation (Swagger UI) at:

**[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)**

---

## 📜 License

This project is licensed under the **MIT License**.

The MIT License allows you to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the software, provided the original copyright and permission notice is included in all copies or substantial portions of the Software.
