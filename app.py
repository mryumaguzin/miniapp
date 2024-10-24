from flask import Flask
from models import db
from routes import app

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Создание базы данных
    app.run(debug=True)
