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
| `/health`               | HEAD   | Health check (headers)    | 200 OK                 | UptimeRobot free-tier monitoring support                          |
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

### **Product Schema (SQLModel):**

```python
class ProductBase(SQLModel):
    name: str       # Min 1 char, max 50 chars, whitespace stripped & validated
    price: float    # Must be > 0 (business constraint)
    quantity: int   # Must be >= 0 (can be out of stock)
    in_stock: bool  # Flag for product availability
```

### **Validation Rules:**

| Field      | Constraint                        | Rationale                                           |
| ---------- | --------------------------------- | --------------------------------------------------- |
| `id`       | Auto-generated (primary key)      | Database handles ID generation via autoincrement     |
| `name`     | `min_length=1`, `max_length=50`   | Prevents empty and excessively long names            |
| `name`     | `@field_validator` (strip + check)| Rejects whitespace-only names like `"   "`           |
| `price`    | `gt=0`                            | Products can't be free or negative price             |
| `quantity` | `ge=0`                            | Zero is valid (out of stock)                         |
| `in_stock` | Optional on create                | Can be auto-determined or explicitly set             |

### **Schema Inheritance Pattern:**

```python
ProductBase    → Shared fields + validation (name, price, quantity, in_stock)
  ├── Product       → Database table model (adds id, table=True)
  ├── ProductCreate → POST schema (inherits base, excludes id)
  └── ProductUpdate → PATCH schema (all fields Optional for partial updates)
```

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

**Decision:** Create separate Pydantic model for PATCH requests.

```python
class ProductBase(SQLModel):     # Full model (shared fields)
    name: str
    price: float
    quantity: int
    in_stock: bool

class ProductUpdate(SQLModel):   # Partial model (all Optional)
    name: Optional[str]
    price: Optional[float]
    quantity: Optional[int]
    in_stock: Optional[bool]
```

**Rationale:**

- ✅ **API clarity** - PATCH only updates provided fields (clear contract)
- ✅ **Prevents accidental changes** - `exclude_unset=True` ensures only sent fields are modified
- ✅ **Future extensibility** - Easy to add more updatable fields later

---

### **3. Why Auto-Generate IDs in Database Layer?**

**Decision:** Server assigns IDs via PostgreSQL autoincrement, not client.

**Rationale:**

- ✅ **Data integrity** - Prevents ID collisions
- ✅ **Security** - Client can't forge IDs
- ✅ **Simplicity** - Database handles sequencing automatically

---

### **4. Why Calculate `in_stock` in Service Layer?**

**Decision:** Update `in_stock` when quantity changes, not in Pydantic model.

**Rationale:**

- ✅ **Separation of concerns** - Business logic stays in service layer
- ✅ **Three-tier compliance** - Data models should be "dumb" (no logic)
- ✅ **Explicit updates** - Clear when/where stock status changes

---

### **5. Why Structured JSON Logging?**

**Decision:** Use `python-json-logger` with `extra={}` fields instead of plain text f-strings.

**Before (v1.0.0):**
```
INFO: 2026-02-15 21:30:00 - __main__ - Product created successfully with ID: 5
```

**After (v1.2.0):**
```json
{"timestamp": "2026-02-15T21:30:00", "level": "INFO", "name": "__main__", "message": "Product created successfully", "product_id": 5}
```

**Rationale:**

- ✅ **Machine-parseable** - Log aggregators (Datadog, ELK) can index and search fields
- ✅ **Searchable** - `product_id`, `count`, `total_value` are discrete keys, not buried in strings
- ✅ **Consistent format** - Every log line follows the same JSON structure
- ✅ **Dual output** - Console (Render/Docker) + file (`logs/app.log`) for local debugging

---

## 🚀 Error Handling Strategy

### **Error Types:**

| Error Type               | HTTP Status               | Handling Location    | Example                          |
| ------------------------ | ------------------------- | -------------------- | -------------------------------- |
| **Validation Error**     | 422 Unprocessable Entity  | Pydantic (automatic) | Invalid price (<= 0), empty name |
| **Not Found**            | 404 Not Found             | Presentation Layer   | Product ID doesn't exist         |
| **File I/O Error**       | 500 Internal Server Error | Data Access Layer    | Can't read/write JSON            |
| **Business Logic Error** | 400 Bad Request           | Business Logic Layer | (Future: duplicate product name) |

### **Input Validation Defense:**

```
Client Request
     ↓
Pydantic Field Constraints ──→ 422 (empty name, negative price, wrong type)
     ↓
Custom @field_validator ──→ 422 (whitespace-only name like "   ")
     ↓
Endpoint Logic ──→ 404 (product not found)
     ↓
Success Response ──→ 200/201/204
```

---

## 📊 Data Flow Example (POST /products)

```
1. CLIENT SENDS:
   POST /products
   {
     "name": "  Laptop  ",
     "price": 999.99,
     "quantity": 10
   }

2. VALIDATION LAYER (models.py):
   - Pydantic checks: min_length=1 ✅, max_length=50 ✅, price gt=0 ✅
   - @field_validator strips whitespace: "  Laptop  " → "Laptop"
   - ProductCreate schema passes validation

3. PRESENTATION LAYER (main.py):
   - FastAPI receives validated data
   - Injects database session via SessionDep (Depends)
   - Calls Product.model_validate() to create table instance
   - Logs: {"message": "Creating new product", "name": "Laptop", "price": 999.99}

4. DATA LAYER (database.py → PostgreSQL):
   - session.add(db_product)
   - session.commit()
   - session.refresh(db_product) → gets DB-generated ID
   - Logs: {"message": "Product created successfully", "product_id": 5}

5. RESPONSE TO CLIENT:
   HTTP 201 Created
   {
     "id": 5,
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
- ✅ **HEAD method support** - Compatible with UptimeRobot free-tier monitoring

**Implementation:**

```python
class HealthResponse(SQLModel):
    """Structured health check response"""
    status: str = Field(default="ok", description="Health status indicator")
    uptime: float = Field(default=0.0, description="Service uptime in seconds")
    version: str

@app.head("/health")  # UptimeRobot compatibility
@app.get("/health", response_model=HealthResponse, tags=["System"])
def health_check():
    return HealthResponse(
        status="healthy",
        version="1.2.0",
        uptime=time.time() - START_TIME
    )
```

---

### **Testing Strategy**

**Decision:** Implement two-tier testing: integration tests (real DB) + isolated mock tests (SQLite override).

**Integration Test Coverage (6 tests — `test_api.py`):**

| Test Name                       | Purpose                       | Validates                         |
| ------------------------------- | ----------------------------- | --------------------------------- |
| `test_health`                   | Health endpoint functionality | Status, version, uptime fields    |
| `test_cloud_connection`         | Database connectivity         | Supabase connection works         |
| `test_create_product`           | Product creation              | POST endpoint, validation         |
| `test_read_single_product`      | Single product retrieval      | GET by ID works                   |
| `test_read_nonexistent_product` | Error handling                | 404 response for missing products |
| `test_create_product_invalid`   | Input validation              | 422 response for invalid data     |

**Isolated Mock Test Coverage (9 tests — `test_mock_api.py`):**

| Test Name                          | Purpose                              | Validates                               |
| ---------------------------------- | ------------------------------------ | --------------------------------------- |
| `test_create_product_isolated`     | Product creation without real DB     | Dependency override works               |
| `test_read_products_isolated`      | Product listing in isolation         | SQLite override returns correct data    |
| `test_product_not_found_isolated`  | 404 in isolated environment          | Error handling works without Supabase   |
| `test_create_product_empty_name`   | Empty name rejection                 | `min_length=1` catches `""`             |
| `test_create_product_negative_price`| Negative price rejection            | `gt=0` catches negative values          |
| `test_create_product_whitespace_name`| Whitespace-only name rejection     | `@field_validator` catches `"   "`      |

**Why two test tiers:**
- ✅ **Integration tests** prove the full stack works end-to-end with real Supabase
- ✅ **Mock tests** prove endpoint logic works in isolation, fast, offline, with zero data pollution
- ✅ **Together** they catch both connectivity issues AND logic bugs

**Key Testing Pattern — Dependency Override:**

```python
# Swap real Supabase for in-memory SQLite
test_engine = create_engine("sqlite://", poolclass=StaticPool)

def get_test_session():
    with Session(test_engine) as session:
        yield session

app.dependency_overrides[get_session] = get_test_session
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

## 🔒 Phase 7: Isolated Testing, Validation & Structured Logging ✅

**Decision:** Add dependency override testing, input validation hardening, and structured JSON logging.

### **Input Validation Hardening**

**Problem discovered by tests:** Empty and whitespace-only product names were accepted (returned 201 instead of 422).

**Solution — layered defense:**

```python
name: str = Field(max_length=50, min_length=1, index=True)

@field_validator("name")
@classmethod
def name_must_not_be_empty(cls, value):
    if not value.strip():
        raise ValueError("Product name must not be empty.")
    return value.strip()
```

- `min_length=1` catches empty strings `""`
- `@field_validator` strips whitespace and rejects blank names like `"   "`
- `.strip()` also cleans valid names: `"  Laptop  "` → `"Laptop"`

**Key insight:** Tests caught a real bug that manual testing missed. This is exactly what automated testing is for.

### **Structured JSON Logging**

**Decision:** Replace `logging.Formatter` with `jsonlogger.JsonFormatter` and convert all f-string log calls to use `extra={}`.

**Why:**
- Log aggregators can index and search discrete fields
- `product_id`, `count`, `total_value` become queryable keys
- Consistent JSON structure across all log lines
- Compatible with Datadog, ELK stack, Render logs

### **Dependency Override Testing**

**Decision:** Use FastAPI's `app.dependency_overrides` with in-memory SQLite for isolated testing.

**Why:**
- Tests run offline (no Supabase dependency)
- No test data pollution in production database
- No phantom auto-increment IDs
- Fast execution (no network calls)
- Deterministic results

---

### **Phase 8: Router Refactor** (Planned)

- Refactor `main.py` into proper `app/` package structure
- Move product endpoints to `app/routers/products.py`
- Slim down `main.py` to app instance + lifespan + health only
- Update imports across test files

### **Phase 9: Advanced Features** (Planned)

- Add user authentication (JWT tokens)
- Implement search & filtering capabilities
- Rate limiting for API protection
- Caching layer (Redis)

### **Phase 10: CI/CD Pipeline** (Planned)

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
6. ✅ **Tests catching real bugs** - Empty name validation gap found by automated tests

### **Challenges Overcome:**

1. 🔧 **Route ordering** - Learned specific routes must come before dynamic routes
2. 🔧 **Status code selection** - 201 vs 200, 204 vs 200 (semantic correctness matters)
3. 🔧 **Layer separation** - Resisted putting business logic in routes (kept it in service layer)
4. 🔧 **Error handling** - Learned when to return `None` vs raise exceptions
5. 🔧 **Pydantic v1 vs v2** - Error types changed (`"value_error.any_str.min_length"` → `"string_too_short"`)
6. 🔧 **UptimeRobot HEAD requests** - Free tier only sends HEAD, requiring `@app.head()` decorator

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

### **v1.2.0 - Isolated Testing, Validation & Structured Logging**
*Focused on test isolation, input hardening, and production observability.*

| Skill Category              | Specific Skills                                                              |
| --------------------------- | ---------------------------------------------------------------------------- |
| **Advanced Testing**        | Dependency Override Pattern, SQLite In-Memory Testing, StaticPool            |
| **Input Validation**        | `@field_validator`, Whitespace Stripping, Layered Validation Defense         |
| **Structured Logging**      | `python-json-logger`, `extra={}` Pattern, Machine-Parseable Log Output      |
| **Pydantic v2 Proficiency** | `field_validator` Decorator, `"string_too_short"` Error Types               |
| **Monitoring Integration**  | UptimeRobot HEAD Support, External Health Check Configuration               |
| **Test Architecture**       | Two-Tier Testing Strategy (Integration + Isolated), Zero Data Pollution     |

---

## 📖 References & Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLModel Documentation](https://sqlmodel.tiangolo.com/)
- [PostgreSQL Official Documentation](https://www.postgresql.org/docs/)
- [Python JSON Logger](https://github.com/madzak/python-json-logger)
- [Python Logging Cookbook](https://docs.python.org/3/howto/logging.html)
- [Pydantic v2 Validators](https://docs.pydantic.dev/latest/concepts/validators/)
- [REST API Best Practices](https://restfulapi.net/)
- [Git Configuration (.gitignore) Guide](https://git-sc.com/docs/gitignore)
- [Dockerizing a FastAPI App](https://fastapi.tiangolo.com/deployment/docker/)
- [Heroku/Render Procfile Documentation](https://devcenter.heroku.com/articles/procfile)

---

**Document Version:** 1.2.0
**Last Updated:** February 15, 2026
**Status:** Isolated Testing, Validation & Structured Logging (v1.2.0) - Mock Tests, Input Hardening & JSON Logging Added
