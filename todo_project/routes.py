from flask import render_template
from todo_project import app

@app.route("/")
def home():
    return "OK - Flask rodando"
