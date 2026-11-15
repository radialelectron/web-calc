import os
import sys

ROOT = os.path.join(os.path.dirname(__file__), "..", "..", "..")
sys.path.insert(0, os.path.join(ROOT, "backend"))
sys.path.insert(0, os.path.join(ROOT, "consumers", "tip-calculator"))

import pytest  # noqa: E402
from database import Base, get_db  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402
from main import app  # noqa: E402
from sqlalchemy import create_engine  # noqa: E402
from sqlalchemy.orm import sessionmaker  # noqa: E402
from sqlalchemy.pool import StaticPool  # noqa: E402
from tip_calculator.webcalc_client import WebcalcClient  # noqa: E402

ENGINE = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
Session = sessionmaker(autocommit=False, autoflush=False, bind=ENGINE)


def _get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = _get_db


@pytest.fixture()
def webcalc():
    """WebcalcClient wired to the real Webcalc app (in-process, no mocks)."""
    Base.metadata.create_all(bind=ENGINE)
    with TestClient(app) as http:
        yield WebcalcClient(http)
    Base.metadata.drop_all(bind=ENGINE)
