"""Test configuration."""

import pytest


@pytest.fixture
def client():
    """FastAPI test client."""
    from fastapi.testclient import TestClient
    from app.main import app

    return TestClient(app)
