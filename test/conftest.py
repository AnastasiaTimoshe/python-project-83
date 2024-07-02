import pytest
from page_analyzer.app import index


@pytest.fixture()
def app():
    app = index()
    app.config.update({
        "TESTING": True,
    })
    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()
