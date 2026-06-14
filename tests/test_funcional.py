"""
Testes Funcionais — fluxos completos do ponto de vista do usuário.
Simula jornadas reais: cadastro → login → CRUD de tarefas → logout.
"""


class TestUserJourney:
    def test_full_registration_and_login_flow(self, client):
        # 1. Registra
        resp = client.post('/register', data={
            'username': 'journey',
            'password': 'Journey1!',
            'confirm_password': 'Journey1!',
        }, follow_redirects=True)
        assert b'Login' in resp.data

        # 2. Faz login
        resp = client.post('/login', data={
            'username': 'journey',
            'password': 'Journey1!',
        }, follow_redirects=True)
        assert b'Login Successfull' in resp.data

        # 3. Acessa lista de tarefas
        resp = client.get('/all_tasks')
        assert resp.status_code == 200

        # 4. Faz logout
        resp = client.get('/logout', follow_redirects=True)
        assert b'Login' in resp.data

        # 5. Confirma que não acessa área protegida após logout
        resp = client.get('/all_tasks', follow_redirects=False)
        assert resp.status_code == 302

    def test_full_task_crud_flow(self, logged_in_client):
        # 1. Cria tarefa
        resp = logged_in_client.post('/add_task', data={
            'task_name': 'Functional test task',
        }, follow_redirects=True)
        assert b'Task Created' in resp.data

        # 2. Verifica que aparece na lista
        resp = logged_in_client.get('/all_tasks')
        assert b'Functional test task' in resp.data

        # 3. Obtém o ID da tarefa criada
        from todo_project.models import Task
        from todo_project import app
        with app.app_context():
            task = Task.query.filter_by(content='Functional test task').first()
            task_id = task.id

        # 4. Edita a tarefa
        resp = logged_in_client.post(f'/all_tasks/{task_id}/update_task', data={
            'task_name': 'Updated functional task',
        }, follow_redirects=True)
        assert b'Task Updated' in resp.data

        # 5. Confirma a edição na lista
        resp = logged_in_client.get('/all_tasks')
        assert b'Updated functional task' in resp.data

        # 6. Deleta a tarefa
        resp = logged_in_client.get(f'/all_tasks/{task_id}/delete_task',
                                    follow_redirects=True)
        assert resp.status_code == 200

        # 7. Confirma remoção
        resp = logged_in_client.get('/all_tasks')
        assert b'Updated functional task' not in resp.data

    def test_unauthenticated_cannot_create_task(self, client):
        resp = client.post('/add_task', data={
            'task_name': 'Should not be created',
        }, follow_redirects=False)
        assert resp.status_code == 302
        assert '/login' in resp.headers['Location']

    def test_about_page_accessible_without_login(self, client):
        resp = client.get('/about')
        assert resp.status_code == 200

    def test_404_page(self, client):
        resp = client.get('/rota-inexistente')
        assert resp.status_code == 404
