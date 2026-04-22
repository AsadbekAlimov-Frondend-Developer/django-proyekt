from flask import render_template, request, session, redirect, url_for, flash
from models import Product, Category

def init_routes(app):
    
    # Главная страница
    @app.route('/')
    def index():
        # Берем 4 последних добавленных товара для витрины главной страницы
        latest_products = Product.query.order_by(Product.id.desc()).limit(4).all()
        return render_template('index.html', products=latest_products)

    # Каталог товаров с возможностью фильтрации
    @app.route('/catalog')
    def catalog():
        # Получаем ID категории из URL параметров (если есть)
        category_id = request.args.get('category_id', type=int)
        categories = Category.query.all()
        
        if category_id:
            # Фильтруем товары по выбранной категории
            products = Product.query.filter_by(category_id=category_id).all()
            current_category = Category.query.get(category_id)
        else:
            # Если категория не выбрана, показываем все товары
            products = Product.query.all()
            current_category = None
            
        return render_template('catalog.html', products=products, categories=categories, current_category=current_category)

    # Корзина
    @app.route('/cart')
    def cart():
        # Получаем корзину из сессии. Если её нет, то пустой словарь `{} `
        cart_items = session.get('cart', {})
        products_in_cart = []
        total_price = 0
        
        # Перебираем товары в корзине (ID товара и количество)
        for product_id, quantity in cart_items.items():
            product = Product.query.get(int(product_id))
            if product:
                item_total = product.price * quantity
                total_price += item_total
                products_in_cart.append({
                    'product': product,
                    'quantity': quantity,
                    'total': item_total
                })
                
        return render_template('cart.html', cart_items=products_in_cart, total_price=total_price)

    # Добавление товара в корзину
    @app.route('/add_to_cart/<int:product_id>')
    def add_to_cart(product_id):
        # Корзина хранится в сессии в виде словаря: { 'product_id': quantity }
        if 'cart' not in session:
            session['cart'] = {}
            
        cart = session['cart']
        product_id_str = str(product_id)
        
        # Если товар уже есть, увеличиваем количество
        if product_id_str in cart:
            cart[product_id_str] += 1
        else:
            cart[product_id_str] = 1
            
        session.modified = True 
        flash('Товар успешно добавлен в корзину!')
        
        # Возвращаем пользователя на ту же страницу (или в каталог)
        return redirect(request.referrer or url_for('catalog'))

    # Очистка корзины
    @app.route('/clear_cart')
    def clear_cart():
        session.pop('cart', None)
        flash('Корзина очищена.')
        return redirect(url_for('cart'))
