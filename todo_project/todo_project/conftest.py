import pytest
import os
import sys

# Garante que o pacote todo_project seja encontrado
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

os.environ['SECRET_KEY'] = 'test-secret-key'
os.environ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

from todo_project import app as flask_app, db as _db


@pytest.fixture(scope='session')
def app():
    flask_app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'WTF_CSRF_ENABLED': False,
        'SECRET_KEY': 'test-secret-key',
    })
    with flask_app.app_context():
        _db.create_all()
        yield flask_app
        _db.drop_all()


@pytest.fixture(scope='function')
def db(app):
    with app.app_context():
        yield _db
        _db.session.rollback()


@pytest.fixture(scope='function')
def client(app):
    return app.test_client()


@pytest.fixture(scope='function')
def registered_user(client, db):
    """Cria e retorna um usuário registrado."""
    client.post('/register', data={
        'username': 'testuser',
        'password': 'Password1!',
        'confirm_password': 'Password1!',
    }, follow_redirects=True)
    return {'username': 'testuser', 'password': 'Password1!'}


@pytest.fixture(scope='function')
def logged_in_client(client, registered_user):
    """Retorna um client já autenticado."""
    client.post('/login', data={
        'username': registered_user['username'],
        'password': registered_user['password'],
    }, follow_redirects=True)
    return client
