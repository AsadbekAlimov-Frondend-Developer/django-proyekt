from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from models import Category, Product

class ProductAdmin(ModelView):
    # Явно указываем, какие поля показывать при создании/редактировании товара
    form_columns = ['name', 'category', 'description', 'price', 'image_url']

def init_admin(app, db):
    # Создаем админ-панель. Доступ по ссылке: http://127.0.0.1:5000/admin
    admin = Admin(app, name='Управление магазином', template_mode='bootstrap4')
    
    # Добавляем разделы в админ-панель:
    admin.add_view(ModelView(Category, db.session, name="Категории"))
    admin.add_view(ProductAdmin(Product, db.session, name="Товары"))
