# 🏗️ Retail Product API - Design Document

## 📋 Overview

RESTful API for retail inventory management, built with FastAPI and designed with a **Three-Tier Architecture** to ensure clean separation of concerns, maintainability, and scalability.

---

## 🎯 Project Goals

1. **Demonstrate production-ready API development** skills
2. **Implement proper architectural patterns** (three-tier separation)
3. **Showcase backend fundamentals** before advancing to LLM/AI engineering
4. **Build a deployable, working application** (not just local code)

---

## 🏛️ Architecture: Three-Tier Design

### **Why Three-Tier?**

Three-tier architecture separates concerns into distinct layers, making the codebase:

- ✅ **Easier to maintain** - Changes in one layer don't break others
- ✅ **Easier to test** - Each layer can be tested independently
- ✅ **Easier to scale** - Layers can be optimized or replaced independently

### **Layer Breakdown:**

```
┌─────────────────────────────────────────┐
│     Presentation Layer (main.py)        │  ← HTTP Routes, Validation
│  - FastAPI routes                       │
│  - Request/Response handling            │
│  - HTTP status codes                    │
└──────────────┬──────────────────────────┘
               │
               ↓
┌─────────────────────────────────────────┐
│  Business Logic (inventory_service.py)  │  ← Core Business Rules
│  - ID generation                        │
│  - Product modifications                │
│  - Inventory calculations               │
│  - Stock status updates                 │
└──────────────┬──────────────────────────┘
               │
               ↓
┌─────────────────────────────────────────┐
│   Data Access Layer (inventory_io.py)   │  ← Persistence
│  - JSON file read/write                 │
│  - Error handling for file operations   │
│  - Data format conversions              │
└─────────────────────────────────────────┘
```

---

## 📊 API Endpoints Design

### **RESTful Principles Applied:**

| Endpoint                | Method | Purpose                   | Status Code            | Rationale                                                         |
| ----------------------- | ------ | ------------------------- | ---------------------- | ----------------------------------------------------------------- |
| `/health`               | GET    | Health check endpoint     | 200 OK                 | Monitoring & diagnostics (status, version, uptime)                |
| `/products`             | GET    | List all products         | 200 OK                 | Standard collection retrieval                                     |
| `/products/{id}`        | GET    | Get single product        | 200 OK / 404 Not Found | Resource retrieval with error case                                |
| `/products`             | POST   | Create new product        | **201 Created**        | Semantically correct for resource creation                        |
| `/products/{id}`        | PATCH  | Partial update product    | 200 OK / 404 Not Found | Partial resource modification (changed from PUT to PATCH)         |
| `/products/{id}`        | DELETE | Delete product            | **204 No Content**     | Successful deletion returns no body                               |
| `/products/total_value` | GET    | Calculate inventory value | 200 OK                 | Analytics endpoint (placed before `{id}` to avoid route conflict) |

### **Route Ordering Strategy:**

```python
# ✅ CORRECT ORDER (specific routes first):
@app.get("/products/total_value")  # ← Specific route
@app.get("/products/{product_id}")  # ← Dynamic route

# ❌ WRONG ORDER (would break):
@app.get("/products/{product_id}")  # ← Would match "total_value" as an ID!
@app.get("/products/total_value")
```

---

## 🗂️ Data Model Design

### **Product Schema (Pydantic):**

```python
class Product(BaseModel):
    id: int          # Unique identifier (auto-generated)
    name: str        # Max 50 chars (prevents abuse)
    price: float     # Must be > 0 (business constraint)
    quantity: int    # Must be >= 0 (can be out of stock)
    in_stock: bool   # Calculated based on quantity
```

### **Validation Rules:**

| Field      | Constraint      | Rationale                                      |
| ---------- | --------------- | ---------------------------------------------- |
| `id`       | `> 0`           | IDs start at 1 (0 is invalid)                  |
| `name`     | `max_length=50` | Prevents excessively long names                |
| `price`    | `> 0`           | Products can't be free or negative price       |
| `quantity` | `>= 0`          | Zero is valid (out of stock)                   |
| `in_stock` | Auto-calculated | Updated in service layer when quantity changes |

---

## 🔧 Implementation Phases

### **Phase 1: Core Structure** ✅

1. Set up FastAPI app with basic routes
2. Define Pydantic models for validation
3. Implement JSON-based persistence

### **Phase 2: Business Logic** ✅

1. ID auto-generation (sequential)
2. CRUD operations (Create, Read, Update, Delete)
3. Inventory value calculation
4. Stock status tracking

### **Phase 3: Production Features** ✅

1. Comprehensive error handling (404, 422, 500)
2. Logging infrastructure (console + file)
3. Proper HTTP status codes (201, 204, 404)
4. API documentation (auto-generated by FastAPI)

### **Phase 4: Deployment** ✅

1. Deploy to Render (cloud platform)
2. Test live endpoints
3. Update README with live URL

---

## 📝 Design Decisions & Rationale

### **1. Why JSON Storage for MVP?**

**Decision:** Use `products.json` file instead of a database.

**Rationale:**

- ✅ **Faster MVP development** - No database setup needed
- ✅ **Simpler deployment** - No external dependencies
- ✅ **Easy to inspect** - Human-readable data format
- ✅ **Sufficient for demo** - Shows CRUD logic without DB complexity

**Future:** Will migrate to PostgreSQL for production scalability.

---

### **2. Why Separate `ProductUpdate` Model?**

**Decision:** Create separate Pydantic model for PUT requests.

```python
class Product(BaseModel):        # Full model (all fields)
    id: int
    name: str
    price: float
    quantity: int
    in_stock: bool

class ProductUpdate(BaseModel):  # Partial model (only updatable fields)
    quantity: int
```

**Rationale:**

- ✅ **API clarity** - PUT only updates quantity (clear contract)
- ✅ **Prevents accidental changes** - Can't modify ID, name, or price via PUT
- ✅ **Future extensibility** - Easy to add more updatable fields later

---

### **3. Why Auto-Generate IDs in Service Layer?**

**Decision:** Server assigns IDs, not client.

**Rationale:**

- ✅ **Data integrity** - Prevents ID collisions
- ✅ **Security** - Client can't forge IDs
- ✅ **Simplicity** - Client doesn't need to track last ID

**Implementation:**

```python
def get_next_id(products: list) -> int:
    if not products:
        return 1
    return max(product.get("id", 0) for product in products) + 1
```

---

### **4. Why Calculate `in_stock` in Service Layer?**

**Decision:** Update `in_stock` when quantity changes, not in Pydantic model.

**Rationale:**

- ✅ **Separation of concerns** - Business logic stays in service layer
- ✅ **Three-tier compliance** - Data models should be "dumb" (no logic)
- ✅ **Explicit updates** - Clear when/where stock status changes

**Implementation:**

```python
def update_product_quantity(...):
    product["quantity"] = new_quantity
    product["in_stock"] = new_quantity > 0  # ← Calculated here
    save_products(inventory_data)
```

---

### **5. Why Logging at Multiple Layers?**

**Decision:** Add logging in service layer AND presentation layer.

**Rationale:**

- ✅ **Service layer logs business events** (product created, deleted)
- ✅ **Presentation layer logs HTTP events** (API calls, 404s)
- ✅ **Debugging** - Trace requests through all layers
- ✅ **Production monitoring** - Track API usage patterns

---

## 🚀 Error Handling Strategy

### **Error Types:**

| Error Type               | HTTP Status               | Handling Location    | Example                          |
| ------------------------ | ------------------------- | -------------------- | -------------------------------- |
| **Validation Error**     | 422 Unprocessable Entity  | Pydantic (automatic) | Invalid price (<= 0)             |
| **Not Found**            | 404 Not Found             | Presentation Layer   | Product ID doesn't exist         |
| **File I/O Error**       | 500 Internal Server Error | Data Access Layer    | Can't read/write JSON            |
| **Business Logic Error** | 400 Bad Request           | Business Logic Layer | (Future: duplicate product name) |

### **Error Handling Flow:**

```
Client Request
     ↓
Pydantic Validation ──→ 422 (Invalid Data)
     ↓
Service Layer Logic ──→ Returns None (Not Found)
     ↓
Presentation Layer ──→ Raises HTTPException 404
     ↓
FastAPI Exception Handler ──→ JSON Error Response
```

---

## 📊 Data Flow Example (POST /products)

```
1. CLIENT SENDS:
   POST /products
   {
     "id": 999,            ← Ignored (server generates ID)
     "name": "Laptop",
     "price": 999.99,
     "quantity": 10,
     "in_stock": true
   }

2. PRESENTATION LAYER (main.py):
   - FastAPI receives request
   - Pydantic validates data (price > 0, quantity >= 0)
   - Converts to Product model
   - Calls service layer

3. BUSINESS LOGIC LAYER (inventory_service.py):
   - Generates next available ID (e.g., 5)
   - Creates product dict with new ID
   - Appends to in-memory inventory
   - Calls data access layer

4. DATA ACCESS LAYER (inventory_io.py):
   - Writes entire inventory to products.json
   - Logs success/failure

5. RESPONSE TO CLIENT:
   HTTP 201 Created
   {
     "id": 5,              ← Server-generated ID
     "name": "Laptop",
     "price": 999.99,
     "quantity": 10,
     "in_stock": true
   }
```

---

## 🔮 Future Architectural Improvements

## 🔄 Phase 5: The Great Refactor (PostgreSQL Migration) ✅

**Decision:** Replace JSON file storage with a professional Relational Database Management System (RDBMS).

### **Why the change?**

- ❌ **JSON Limitations:** File locking issues, no concurrent writes, manual ID incrementing.
- ✅ **Postgres Benefits:** Atomic transactions, relational integrity, high-speed aggregations (SQL-side), and persistent storage that survives server restarts.

### **Architectural Evolution:**

```text
┌─────────────────────────────────────────┐
│      Presentation Layer (main.py)       │  ← No Change (FastAPI)
└──────────────┬──────────────────────────┘
               │
               ↓
┌─────────────────────────────────────────┐
│      Logic & ORM Layer (models.py)      │  ← REPLACED Service Layer
│  - SQLModel (Pydantic + SQLAlchemy)     │
│  - Automatic Validation                 │
└──────────────┬──────────────────────────┘
               │
               ↓
┌─────────────────────────────────────────┐
│     Data Layer (PostgreSQL / RDS)       │  ← REPLACED JSON File
│  - Structured Relational Tables         │
│  - Database-side math (func.sum)        │
└─────────────────────────────────────────┘
```
---

## 🛠️ Key Refactoring Decisions

### **1. Merging Service and Models**
- **Old Way:** `inventory_service.py` had to manually find the max ID and recalculate `in_stock`.
- **New Way:** Used **SQLModel inheritance**. The database now handles IDs via `primary_key=True`, and the API handles `in_stock` logic via schema validation.

### **2. Database-Side Aggregation**
- **Old Way:** Loading the entire JSON into Python memory just to sum the prices.
- **New Way:** Using `select(func.sum(Product.price * Product.quantity))`. The database does the heavy lifting, returning only the final number to the API.

### **3. Dependency Injection**
- **Decision:** Implemented `SessionDep` using FastAPI's `Depends`.
- **Rationale:** Ensures every request gets its own database connection and—more importantly—closes it when the request is done, preventing memory leaks.

---

## 🏗️ New Data Contract (SQLModel)

| Feature         | JSON Version (v0.x)      | Postgres Version (v1.0)             |
| :-------------- | :----------------------- | :---------------------------------- |
| **Storage**     | `products.json`          | **PostgreSQL 18**                   |
| **ID Gen**      | Manual `max()` in Python | **Database Serial / Autoincrement** |
| **Concurrency** | One user at a time       | **Multiprocessing Ready**           |
| **Deployment**  | Local Disk               | **Cloud-Ready (Render + Neon/RDS)** |

---

## 🏥 Phase 6: Health Monitoring & Testing Infrastructure ✅

**Decision:** Add production-ready monitoring and comprehensive test coverage.

### **Health Check Endpoint**

**Rationale:**
- ✅ **Production requirement** - Cloud platforms (Render, AWS, etc.) need health checks to determine if the service is running
- ✅ **Uptime tracking** - Provides visibility into service availability
- ✅ **Version reporting** - Allows monitoring systems to detect deployments
- ✅ **Standardization** - Industry best practice for REST APIs

**Implementation:**

```python
class HealthResponse(SQLModel):
    """Structured health check response"""
    status: str = Field(default="ok", description="Health status indicator")
    uptime: float = Field(default=0.0, description="Service uptime in seconds")
    version: str

@app.get("/health", response_model=HealthResponse, tags=["System"])
def health_check():
    return HealthResponse(
        status="healthy",
        version="1.1.0",
        uptime=time.time() - START_TIME
    )
```

**Benefits:**
- Load balancers can verify service health before routing traffic
- Monitoring tools (Datadog, New Relic) can track availability
- Version tracking helps correlate bugs with deployments
- Uptime metric useful for SLA reporting

---

### **Testing Strategy**

**Decision:** Implement pytest-based test suite with FastAPI TestClient.

**Test Coverage (6 tests):**

| Test Name                       | Purpose                       | Validates                         |
| ------------------------------- | ----------------------------- | --------------------------------- |
| `test_health`                   | Health endpoint functionality | Status, version, uptime fields    |
| `test_cloud_connection`         | Database connectivity         | Supabase connection works         |
| `test_create_product`           | Product creation              | POST endpoint, validation         |
| `test_read_single_product`      | Single product retrieval      | GET by ID works                   |
| `test_read_nonexistent_product` | Error handling                | 404 response for missing products |
| `test_create_product_invalid`   | Input validation              | 422 response for invalid data     |

**Why TestClient over manual testing:**
- ✅ **Automated** - Runs in seconds, no manual clicking
- ✅ **Repeatable** - Same tests, same results every time
- ✅ **CI/CD ready** - Can integrate with GitHub Actions
- ✅ **Regression prevention** - Catches bugs when refactoring

**Key Testing Patterns:**

```python
from fastapi.testclient import TestClient

# 1. Test endpoint response structure
def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "version" in data  # Ensure expected fields exist

# 2. Test database integration
def test_cloud_connection():
    response = client.get("/products/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)  # Verify list response

# 3. Test error cases
def test_read_nonexistent_product():
    response = client.get("/products/999999")
    assert response.status_code == 404  # Verify proper error handling
```

---

## 🗄️ Database Migration: Render → Supabase

**Decision:** Migrate from Render's PostgreSQL to Supabase's managed PostgreSQL.

### **Why the change?**

- ❌ **Render limitation** - Render's free tier PostgreSQL became obsolete/deprecated
- ✅ **Supabase advantages:**
  - Modern PostgreSQL management interface
  - Built-in API generation (REST & GraphQL)
  - Real-time subscriptions capability
  - Better free tier for development

### **Migration Impact:**

**Code changes required:** ✅ **ZERO**
- SQLModel abstracts the database layer
- Only the `DATABASE_URL` environment variable changed
- Same PostgreSQL protocol (psycopg2 driver)

**Connection String Format:**

```bash
# Old (Render)
DATABASE_URL=postgresql://user:password@hostname.render.com/database

# New (Supabase)
DATABASE_URL=postgresql://user:password@db.supabase.co:5432/postgres
```

**Benefits:**
- Same ACID compliance and relational integrity
- Better developer experience with Supabase dashboard
- Free tier more suitable for portfolio projects
- Potential for future feature expansion (real-time, storage)

---

### **Phase 7: Advanced Features** (Planned)

- Add user authentication (JWT tokens)
- Implement search & filtering capabilities
- Rate limiting for API protection
- Caching layer (Redis)

### **Phase 8: CI/CD Pipeline** (Planned)

- GitHub Actions workflow for automated testing
- Automated deployment on merge to main
- Test coverage reporting
- Linting and code quality checks (ruff, black)

---

## 📚 Key Learnings

### **What Worked Well:**

1. ✅ **Planning before coding** - Mapping CLI functions to API endpoints saved time
2. ✅ **Incremental development** - Built layer by layer, tested each piece
3. ✅ **Using AI assistants** - Gemini/ChatGPT/Claude for architecture validation
4. ✅ **Type hints everywhere** - Caught bugs early, improved IDE autocomplete
5. ✅ **Comprehensive logging** - Made debugging significantly easier

### **Challenges Overcome:**

1. 🔧 **Route ordering** - Learned specific routes must come before dynamic routes
2. 🔧 **Status code selection** - 201 vs 200, 204 vs 200 (semantic correctness matters)
3. 🔧 **Layer separation** - Resisted putting business logic in routes (kept it in service layer)
4. 🔧 **Error handling** - Learned when to return `None` vs raise exceptions

---

## 🎓 Skills Demonstrated (The Evolution)

### **v1.0.0 - The Professional Upgrade (Database-Driven)**
*Focused on scalability, relational data, and modern Python patterns.*

| Skill Category            | Specific Skills                                                   |
| ------------------------- | ----------------------------------------------------------------- |
| **Backend Development**   | FastAPI, RESTful API design, HTTP semantics                       |
| **Software Architecture** | Three-tier architecture, separation of concerns                   |
| **Database Engineering**  | **PostgreSQL 18**, Relational Schema Design, SQL Aggregations     |
| **ORM & Persistence**     | **SQLModel**, SQLAlchemy Engine, Session & Transaction management |
| **Modern Async Patterns** | **Lifespan Context Managers** (replacing deprecated events)       |
| **Dependency Injection**  | FastAPI `Depends` with **Annotated** type hints                   |
| **Security & Config**     | Environment Secret Management (**`.env`**, `python-dotenv`)       |
| **Data Integrity**        | Database-level Primary Keys, Indexing, and Auto-increment         |
| **Advanced Querying**     | Database-side math (`func.sum`), Offset/Limit Pagination          |
| **Data Validation**       | Pydantic models, Field constraints, type safety                   |
| **Error Handling**        | Try-except blocks, HTTPException, proper status codes             |
| **Logging**               | Python logging module, structured logs, multiple handlers         |
| **Code Quality**          | Type hints, docstrings, meaningful variable names                 |
| **Version Control**       | Git, meaningful commits, clean repo structure                     |
| **Documentation**         | README, design docs, inline comments                              |
| **Dev Environment**       | pgAdmin 4 for Database Administration & Data Visualization        |

### **v1.1.0 - Production Monitoring & Quality Assurance**
*Focused on testing, health monitoring, and production readiness.*

| Skill Category           | Specific Skills                                                     |
| ------------------------ | ------------------------------------------------------------------- |
| **Testing & QA**         | **pytest**, FastAPI TestClient, Integration Testing, Test Coverage  |
| **Health Monitoring**    | Health Check Endpoints, Uptime Tracking, Version Reporting          |
| **Cloud Infrastructure** | **Supabase** PostgreSQL, Database Migration, Multi-cloud Deployment |
| **Error Handling**       | 404 Testing, 422 Validation Testing, Status Code Verification       |
| **API Design Maturity**  | System Tags, Response Models, Structured Health Responses           |
| **Development Workflow** | Test-Driven Practices, Automated Testing, Regression Prevention     |

---

## 📖 References & Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLModel Documentation](https://sqlmodel.tiangolo.com/)
- [PostgreSQL Official Documentation](https://www.postgresql.org/docs/)
- [Python Logging Cookbook](https://docs.python.org/3/howto/logging.html)
- [REST API Best Practices](https://restfulapi.net/)
- [Git Configuration (.gitignore) Guide](https://git-sc.com/docs/gitignore)
- [Dockerizing a FastAPI App](https://fastapi.tiangolo.com/deployment/docker/)
- [Heroku/Render Procfile Documentation](https://devcenter.heroku.com/articles/procfile)

---

**Document Version:** 1.1.0
**Last Updated:** February 11, 2026
**Status:** Production Monitoring & Testing (v1.1.0) - Health Checks & Test Suite Added