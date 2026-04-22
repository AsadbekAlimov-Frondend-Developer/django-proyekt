from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Модель (таблица) Категорий
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    
    # Метод, который определяет, как объект будет отображаться в виде текста (например в админке)
    def __str__(self):
        return self.name

# Модель (таблица) Товаров
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(300), nullable=True) # Ссылка на изображение
    
    # Связь с категорией (Один ко многим: в одной категории может быть много товаров)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    category = db.relationship('Category', backref='products')

    def __str__(self):
        return self.name
