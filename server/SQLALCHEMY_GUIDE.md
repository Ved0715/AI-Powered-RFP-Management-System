# SQLAlchemy Setup - Quick Reference

## Installation Commands

```bash
# Activate virtual environment
source venv/bin/activate

# Install SQLAlchemy and related packages
pip install sqlalchemy asyncpg alembic python-dotenv greenlet

# Update requirements.txt
pip freeze > requirements.txt
```

## Key Files Created

1. **`models/base.py`** - SQLAlchemy configuration

   - Async engine
   - Session factory
   - Database enums (Role, RFPStatus, ProposalStatus)
   - FastAPI dependency `get_db()`

2. **`models/__init__.py`** - Package exports

3. **`.env`** - Environment variables (DATABASE_URL)

4. **`test_db_connection.py`** - Database connection test

## Usage in FastAPI Routes

```python
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from models import get_db

router = APIRouter()

@router.get("/test")
async def test_route(db: AsyncSession = Depends(get_db)):
    result = await db.execute("SELECT 1")
    return {"result": result.scalar()}
```

## Database Connection Details

- **Host**: localhost
- **Port**: 5432
- **Database**: rfp_db
- **User**: rfp_user
- **Password**: rfp_password
- **Connection String**: `postgresql+asyncpg://rfp_user:rfp_password@localhost:5432/rfp_db`

## Test Connection

```bash
python test_db_connection.py
```

## Next Steps

1. Create model files:

   - `models/user.py`
   - `models/rfp.py`
   - `models/proposal.py`

2. Initialize Alembic for migrations:

   ```bash
   alembic init alembic
   ```

3. Create initial migration:

   ```bash
   alembic revision --autogenerate -m "Initial schema"
   ```

4. Run migrations:
   ```bash
   alembic upgrade head
   ```
