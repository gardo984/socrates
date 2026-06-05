import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.database import Base
from app.core.security import create_access_token
from app.db.models import User


TEST_DATABASE_URL = "sqlite+pysqlite:///:memory:"
_test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

# Patch the module-level engine BEFORE any imports trigger the real one
import app.db.database as db_module
db_module.engine = _test_engine

# Re-create the SessionLocal with the test engine
db_module.SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=_test_engine
)

# Now import the app (engine already patched)
from app.main import app as _test_app


@pytest.fixture(scope="function")
def session():
    Base.metadata.create_all(bind=_test_engine)
    db = db_module.SessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=_test_engine)


@pytest.fixture(scope="function")
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            pass

    _test_app.dependency_overrides[db_module.get_db] = override_get_db
    with TestClient(_test_app) as test_client:
        yield test_client
    _test_app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def fake_user(session):
    user = User(
        name="Test User",
        email="test@example.com",
        hashed_password="$2b$12$LJ3m4ys3Lk0TSwHnbfOMiOx5xVex2J1vM1vC5z1x1x1x1x1x1x1x",
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@pytest.fixture(scope="function")
def auth_headers(fake_user):
    token = create_access_token(data={"sub": str(fake_user.id)})
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture(scope="function")
def auth_headers_for_user(session):
    def _make_headers(user: User):
        token = create_access_token(data={"sub": str(user.id)})
        return {"Authorization": f"Bearer {token}"}
    return _make_headers
