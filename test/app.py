from flask import Flask
from models import db
from routes import init_routes
from admin_setup import init_admin

def create_app():
    # Создаем экземпляр приложения Flask
    app = Flask(__name__)
    
    # Секретный ключ нужен для работы сессий (корзины). 
    # На реальном сервере он должен быть сложным и скрытым.
    app.config['SECRET_KEY'] = 'super-secret-key-for-diploma' 
    
    # Настройка базы данных. Мы используем SQLite - она хранит всё в одном файле.
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///store.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Данные для входа в Админ-панель
    app.config['ADMIN_USERNAME'] = 'admin'
    app.config['ADMIN_PASSWORD'] = 'admin777'

    # Инициализация базы данных
    db.init_app(app)
    
    # Инициализация админ-панели
    init_admin(app, db)
    
    # Инициализация маршрутов (страниц сайта)
    init_routes(app)

    # При первом запуске создаем таблицы в базе данных (если их нет)
    with app.app_context():
        db.create_all()

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, port=5000)
