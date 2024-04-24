import pytest
import vt1

@pytest.fixture()
def app():
    app = vt1.app
    yield app

@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()
