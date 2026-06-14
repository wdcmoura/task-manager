"""
Testes Unitários — modelos e lógica isolada (sem I/O externo).
"""
from todo_project.models import User, Task
from todo_project import bcrypt


class TestUserModel:
    def test_user_repr(self, app):
        with app.app_context():
            user = User(username='alice', password='hashed')
            assert 'alice' in repr(user)

    def test_password_is_hashed(self, app):
        with app.app_context():
            raw = 'Password1!'
            hashed = bcrypt.generate_password_hash(raw).decode('utf-8')
            assert hashed != raw
            assert bcrypt.check_password_hash(hashed, raw)

    def test_wrong_password_fails(self, app):
        with app.app_context():
            hashed = bcrypt.generate_password_hash('Password1!').decode('utf-8')
            assert not bcrypt.check_password_hash(hashed, 'WrongPass!')

    def test_username_unique_constraint(self, db, app):
        with app.app_context():
            u1 = User(username='uniqueuser', password='hash1')
            u2 = User(username='uniqueuser', password='hash2')
            db.session.add(u1)
            db.session.commit()
            db.session.add(u2)
            import pytest
            with pytest.raises(Exception):
                db.session.commit()
            db.session.rollback()


class TestTaskModel:
    def test_task_repr(self, app):
        with app.app_context():
            task = Task(content='Buy milk', user_id=1)
            assert 'Buy milk' in repr(task)

    def test_task_date_auto_set(self, db, app):
        with app.app_context():
            user = User(username='dateowner', password='hash')
            db.session.add(user)
            db.session.commit()
            task = Task(content='Check date', user_id=user.id)
            db.session.add(task)
            db.session.commit()
            assert task.date_posted is not None

    def test_task_content_stored(self, db, app):
        with app.app_context():
            user = User(username='taskowner', password='hash')
            db.session.add(user)
            db.session.commit()
            task = Task(content='My task', user_id=user.id)
            db.session.add(task)
            db.session.commit()
            fetched = Task.query.filter_by(content='My task').first()
            assert fetched is not None
            assert fetched.user_id == user.id
