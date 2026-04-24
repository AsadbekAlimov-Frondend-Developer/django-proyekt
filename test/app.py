fr om flask import Flask
fro m models import db
fro m routes import init_routes
fro m admin_setup import init_admin

def crea te_app():
    # Создаем экземпляр приложения Flask
    app = F lask(__name__)
    
    # Секретный ключ нужен для работы сессий (корзины). 
    # На реальном сервере он должен быть сложным и скрытым.
    app.conf ig['SECRET_KEY'] = 'super-secret-key-for-diploma' 
    
    # Настройка базы данных. Мы используем SQLite - она хранит всё в одном файле.
    app.conf ig['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///store.db'
    app.conf ig['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

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
