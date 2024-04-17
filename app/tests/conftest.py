import sys

import pytest

sys.path.append('app')

from app.app import create_app
from app.pesu import PESUAcademy


@pytest.fixture
def pesu_academy():
    yield PESUAcademy()


@pytest.fixture
def app():
    yield create_app()


@pytest.fixture
def client(app):
    return app.test_client()
