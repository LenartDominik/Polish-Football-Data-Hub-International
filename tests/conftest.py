import sys
import os
from pathlib import Path

# Dodaj główny katalog projektu do sys.path, aby testy widziały moduł 'app'
# To pozwala na importowanie np. 'from app.backend.main import app'
project_root = str(Path(__file__).parent.parent)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import pytest
import os

# Force SQLite for tests if NOT explicitly set to something else
# This ensures tests don't accidentally wipe a real Supabase DB
if "DATABASE_URL" not in os.environ:
    os.environ["DATABASE_URL"] = "sqlite:///:memory:"

from app.backend.database import engine, Base
from app.backend.main import app
from fastapi.testclient import TestClient

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """Create all tables for testing - runs once per test session"""
    # For SQLite in-memory, the engine and connection must persist
    # Line 40 in main.py also calls this, but doing it here ensures
    # it happens before any test client is created.
    Base.metadata.create_all(bind=engine)
    yield

@pytest.fixture
def client():
    """Get a TestClient for testing API endpoints"""
    with TestClient(app) as c:
        yield c
