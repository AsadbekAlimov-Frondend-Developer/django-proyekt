from flask import request, Response, current_app
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from models import Category, Product
from werkzeug.exceptions import HTTPException

# Класс для защиты админки паролем (Basic Auth)
class SecureViewMixin:
    def is_accessible(self):
        auth = request.authorization
        if auth and auth.username == current_app.config['ADMIN_USERNAME'] and \
           auth.password == current_app.config['ADMIN_PASSWORD']:
            return True
        return False

    def _handle_view(self, name, **kwargs):
        if not self.is_accessible():
            return Response(
                'Нужна авторизация', 401,
                {'WWW-Authenticate': 'Basic realm="Login Required"'}
            )

class SecureModelView(SecureViewMixin, ModelView):
    pass

class SecureAdminIndexView(SecureViewMixin, AdminIndexView):
    pass

class ProductAdmin(SecureModelView):
    # Явно указываем, какие поля показывать при создании/редактировании товара
    form_columns = ['name', 'category', 'description', 'price', 'image_url']

class CategoryAdmin(SecureModelView):
    pass

def init_admin(app, db):
    # Создаем админ-панель. Доступ по ссылке: http://127.0.0.1:5000/admin
    admin = Admin(
        app, 
        name='Управление магазином', 
        template_mode='bootstrap4',
        index_view=SecureAdminIndexView(name='Главная', url='/admin')
    )
    
    # Добавляем разделы в админ-панель:
    admin.add_view(CategoryAdmin(Category, db.session, name="Категории"))
    admin.add_view(ProductAdmin(Product, db.session, name="Товары"))
