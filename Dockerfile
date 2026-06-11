FROM python:3.10-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir \
    Flask==1.1.4 \
    Flask-Bcrypt==0.7.1 \
    Flask-Login==0.5.0 \
    Flask-SQLAlchemy==2.4.1 \
    Flask-WTF==0.14.3 \
    WTForms==2.2.1 \
    SQLAlchemy==1.3.24 \
    Werkzeug==1.0.1 \
    Jinja2==2.11.3 \
    MarkupSafe==2.0.1 \
    itsdangerous==1.1.0 \
    click==7.1.2

EXPOSE 5000

CMD ["python", "todo_project/run.py"]
