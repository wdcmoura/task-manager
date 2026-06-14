"""
Testes de Integração — rotas + banco de dados em memória.
Verifica que as camadas (route → model → db) funcionam juntas.
"""


class TestAuthRoutes:
    def test_register_page_loads(self, client):
        response = client.get('/register')
        assert response.status_code == 200
        assert b'Register' in response.data

    def test_login_page_loads(self, client):
        response = client.get('/login')
        assert response.status_code == 200
        assert b'Login' in response.data

    def test_register_creates_user(self, client, db):
        response = client.post('/register', data={
            'username': 'newuser',
            'password': 'Password1!',
            'confirm_password': 'Password1!',
        }, follow_redirects=True)
        assert response.status_code == 200
        from todo_project.models import User
        user = User.query.filter_by(username='newuser').first()
        assert user is not None

    def test_register_redirects_to_login(self, client):
        response = client.post('/register', data={
            'username': 'redirect',
            'password': 'Password1!',
            'confirm_password': 'Password1!',
        })
        assert response.status_code == 302
        assert '/login' in response.headers['Location']

    def test_register_duplicate_username(self, client, registered_user):
        response = client.post('/register', data={
            'username': registered_user['username'],
            'password': 'Password1!',
            'confirm_password': 'Password1!',
        }, follow_redirects=True)
        assert response.status_code == 200
        assert b'Register' in response.data  # permanece na página de registro

    def test_login_valid_credentials(self, client, registered_user):
        response = client.post('/login', data={
            'username': registered_user['username'],
            'password': registered_user['password'],
        }, follow_redirects=True)
        assert response.status_code == 200
        assert b'Login Successfull' in response.data

    def test_login_invalid_password(self, client, registered_user):
        response = client.post('/login', data={
            'username': registered_user['username'],
            'password': 'WrongPassword!',
        }, follow_redirects=True)
        assert b'Login Unsuccessful' in response.data

    def test_login_nonexistent_user(self, client):
        response = client.post('/login', data={
            'username': 'ghost',
            'password': 'Password1!',
        }, follow_redirects=True)
        assert b'Login Unsuccessful' in response.data


class TestProtectedRoutes:
    def test_all_tasks_requires_login(self, client):
        response = client.get('/all_tasks', follow_redirects=False)
        assert response.status_code == 302
        assert '/login' in response.headers['Location']

    def test_add_task_requires_login(self, client):
        response = client.get('/add_task', follow_redirects=False)
        assert response.status_code == 302

    def test_logout_redirects(self, logged_in_client):
        response = logged_in_client.get('/logout', follow_redirects=False)
        assert response.status_code == 302
        assert '/login' in response.headers['Location']


class TestTaskRoutes:
    def test_add_task_saves_to_db(self, logged_in_client, db):
        response = logged_in_client.post('/add_task', data={
            'task_name': 'Integration task',
        }, follow_redirects=True)
        assert response.status_code == 200
        from todo_project.models import Task
        task = Task.query.filter_by(content='Integration task').first()
        assert task is not None

    def test_all_tasks_shows_user_tasks(self, logged_in_client):
        logged_in_client.post('/add_task', data={'task_name': 'Visible task'})
        response = logged_in_client.get('/all_tasks')
        assert response.status_code == 200
        assert b'Visible task' in response.data
