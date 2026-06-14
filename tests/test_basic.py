import sys
sys.path.append("todo_project")

from todo_project import app

def test_app_exists():
    assert app is not None

def test_about_page():
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200
