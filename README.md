# E-Commerce Backend (Django + DRF)

A modular, extensible backend service for an e‑commerce platform built with Django and Django REST Framework. It provides user management and catalog (categories/products) functionality with a clean architecture and environment-specific settings.

---

## Key Features
- Modular app structure (`apps/users`, `apps/catalog`)
- Token/JWT-ready authentication architecture (custom user model)
- Category & product models with serializer + view layers
- DRF pagination & permissions abstractions
- Environment-specific settings (`development`, `staging`, `production`, `testing`)
- Seed script for bootstrap data (`seed_category_product_db`)
- Dockerized deployment workflow
- Pytest test suite scaffold

---

## Tech Stack
- Python 3.10+
- Django (core framework)
- Django REST Framework
- PostgreSQL (recommended) / SQLite (dev fallback)
- Pytest
- Docker / Docker Compose (optional)
- ASGI-ready (`core/asgi.py`)

---
## Settings Strategy
- `core/settings/__init__.py`: Selects appropriate setting based on ENVIRONMENT var in `.env` file
- `core/settings/base.py`: Shared defaults
- `core/settings/development.py`: Local DX flags
- `core/settings/testing.py`: Lightweight for CI
- `core/settings/staging.py` / `production.py`: Hardened
---

## Installation (Local)
1. Clone:
   ```
   git clone git@github.com:joekariuki3/ecommerce_backend.git
   cd ecommerce_backend
   ```
2. Create env:
   ```
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. Install deps:
   ```
   pip install -r requirements.txt
   ```
4. Environment variables (example `.env`):
   - see `.env.example`
   ```
   cp .env.example .env
   ```
   - Edit `.env` as needed.
5. Migrate:
   ```
   python manage.py migrate
   ```
6. (Optional) Seed catalog:
   ```
   python manage.py seed_users_db
   python manage.py seed_category_product_db
   ```
7. Run:
   ```
   python manage.py runserver
   ```

---

## Docker Usage
```
docker build -t ecommerce-backend .
docker run -p 8000:8000 --env-file .env ecommerce-backend
```

---

## Management Commands
- `seed_users_db`: Inserts sample users.
- `seed_category_product_db`: Inserts sample categories/products.

---

## API Overview (Illustrative)
Adjust to match actual router registrations.

| Area    | Endpoint (example)                            | Method | Purpose |
|---------|-----------------------------------------------|--------|---------|
| Auth    | `/api/users/register/`                        | POST | Create user |
| Auth    | `/api/auth/login/`                            | POST | Obtain token/session |
| Auth    | `/api/auth/logout/`                           | POST | Invalidate token/session |
| Auth    | `/api/auth/refresh/`                          | POST | Refresh token |
| Auth    | `/api/auth/verify/`                           | POST | Verify token |
| Users   | `/api/users/me/`                              | GET | Current profile |
| Catalog | `/api/catalog/categories/`                    | GET/POST | List/create categories |
| Catalog | `/api/catalog/categories/{id}/`               | GET/PATCH/DELETE | Category detail |
| Catalog | `/api/catalog/products/`                      | GET/POST | List/create products |
| Catalog | `/api/catalog/products/{id}/`                 | GET/PATCH/DELETE | Product detail |
| Catalog | `/api/catalog/products/?category={id}`        | GET | Filter products by category |
| Catalog | `/api/catalog/products/?search={term}`        | GET | Search products by name/description |
| Catalog | `/api/catalog/products/?page={n}`             | GET | Paginated product list |
| Catalog | `/api/catalog/products/?limit={n}&offset={m}` | GET | Offset-based pagination |
| Catalog | `/api/catalog/products/?ordering=price`       | GET | Order by price/name |
---

## Testing
```
pytest -q
```
Pytest auto-discovers under `apps/*/tests/`. Fixtures in `conftest.py`.

---

## Data Model (High-Level)
- Users: Custom user model it extends AbstractUser
- Categories: Simple model with name, description
- Products: Linked to Category (FK).
---

## Migrations
Generate when models change:
```
python manage.py makemigrations
python manage.py migrate
```

---

## Seeding / Sample Data
- Use only in non-production environments.
- Command: `python manage.py seed_users_db`
- Command: `python manage.py seed_category_product_db`  

---

# upcoming features:
- Orders & Cart service (`apps/orders`)
- Inventory & stock reservations
- Payment provider abstraction
- Search (Postgres full-text / OpenSearch)
- Caching (Redis) for catalog endpoints
- Rate limiting (DRF throttles / nginx)

---

## Contributing
1. Create feature branch: `git checkout -b feature/my_feature`
2. Keep commits atomic (Consider Conventional Commits):
   - `feat(catalog): add product discount field`
3. Run tests & lint before push
4. Open PR to `develop` branch
5. Provide description + screenshots (if relevant)

---

## Deployment Checklist
- `DEBUG=false`
- Secure allowed hosts
- Run `collectstatic` if static assets added
- Apply migrations
- Seed only where needed
- Add WSGI/ASGI server (gunicorn/uvicorn) behind reverse proxy

---

## Documentation
Extra references in `docs/ref_doc.md` and `docs/wiki_doc.md`. Keep architecture notes there.

---