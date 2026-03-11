# Retail Inventory API

![Python](https://img.shields.io/badge/Python-3.11%2B-blue?style=flat-square&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115%2B-009688?style=flat-square&logo=fastapi)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-336791?style=flat-square&logo=postgresql)
![Supabase](https://img.shields.io/badge/Supabase-Cloud%20DB-3ECF8E?style=flat-square&logo=supabase)
![SQLModel](https://img.shields.io/badge/SQLModel-ORM-red?style=flat-square)
![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED?style=flat-square&logo=docker)

---

## About

A REST API for managing retail product inventory and variants. Built with FastAPI, SQLModel, and PostgreSQL, with structured JSON logging, centralised exception handling, and Docker support.

---

## Installation

### Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/)
- Docker & Docker Compose

### Clone

```bash
git clone https://github.com/chris-kechagias/retail-inventory-api.git
cd retail-inventory-api
```

### Environment variables

Copy `.env.example` to `.env` and fill in the values:

```bash
cp .env.example .env
```

```env
# Local Docker
DB_USERNAME=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=retail_inventory_db

# Supabase (Cloud) — Transaction pooler
# DB_USERNAME=postgres.<your-project-ref>
# DB_PASSWORD=your_supabase_password
# DB_HOST=aws-1-<region>.pooler.supabase.com
# DB_PORT=6543
# DB_NAME=postgres
```

### Option 1: Local (uv)

Install uv if you don't have it:

```bash
pip install uv
```

Install dependencies and start the database:

```bash
uv sync
docker compose up -d db
```

Run the development server:

```bash
task dev
# or manually:
uv run uvicorn main:app --reload
```

### Option 2: Full Docker

```bash
task build
# or manually:
docker compose up --build
```

The API will be available at http://localhost:8000.

---

## Acknowledgements

Special thanks to [qquorum](https://github.com/qquorum), Senior Software Developer, for code reviews, architectural guidance, and mentorship throughout this project.

---

## Author

**Chris Kechagias**
[GitHub](https://github.com/chris-kechagias) | [LinkedIn](https://www.linkedin.com/in/chris-kechagias)

*Transitioning from retail operations to AI engineering.*

**⭐ If you find this project helpful, consider giving it a star!** 