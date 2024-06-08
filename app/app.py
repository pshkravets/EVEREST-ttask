from flask import render_template, request, redirect, flash, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, logout_user, current_user
from flask_jsonrpc import JSONRPC

from models import Gods, db, City, Order, Address, User, Country
from make_celery import flask_app, login_manager
from forms import AddressForm

from tasks import order_status_changing

jsonrpc = JSONRPC(flask_app, '/api', enable_web_browsable_api=True)


@jsonrpc.method('App.order_rpc')
def order_rpc(login: str, password: str, order_id: int) -> dict:
    order_json = {}
    user = User.query.filter_by(login=login).first()
    if check_password_hash(user.password, password):
        order = Order.query.get(order_id)
        if not order:
            return {'error': 'Order with this id does`t exists'}
        order_json['id'] = order.id
        order_json['amount'] = order.amount
        order_json['status'] = order.status
        order_json['product'] = Gods.query.get(order.good_id).name

        address = Address.query.get(order.address_id)
        city = City.query.get(address.city_id)
        country = Country.query.get(city.country_id)
        order_json['address'] = f'{country.name}, {city.name}, {address.address}'
    else:
        order_json['error'] = 'Your login or password is invalid'
    return order_json


@flask_app.route('/')
def home():
    goods = Gods.query.all()
    return render_template('home.html', goods=goods, current_user=current_user)


@flask_app.route('/create/', methods=['GET', 'POST'])
def create_product():
    if request.method == 'GET':
        return render_template('creating.html')

    if request.method == 'POST':
        photo_path = request.files["photo"].filename
        request.files['photo'].save(f'static/media/{photo_path}')
        price = request.form['price']
        color = request.form['color']
        weight = request.form['weight']
        product_name = request.form['product_name']
        new = Gods(name=product_name, weight=weight, color=color, price=price, photo=photo_path)
        db.session.add(new)
        db.session.commit()
        return redirect('/')


@flask_app.route('/edit/<int:pk>', methods=['GET', 'POST'])
def edit_product(pk):
    if request.method == "GET":
        product = Gods.query.get(pk)
        return render_template('edit.html', product=product)
    if request.method == 'POST':
        thing = Gods.query.get(pk)
        price = request.form['price']
        color = request.form['color']
        weight = request.form['weight']
        product_name = request.form['product_name']

        thing.name = product_name
        thing.weight = weight
        thing.color = color
        thing.price = price
        if request.files['photo']:
            photo_path = request.files["photo"].filename
            request.files['photo'].save(f'static/media/{photo_path}')
            thing.photo = photo_path
        db.session.commit()
        return redirect('/')


@flask_app.route('/delete/<int:pk>')
def product_deleting(pk):
    thing = Gods.query.get(pk)
    db.session.delete(thing)
    db.session.commit()
    return redirect('/')


@flask_app.route('/order/<int:pk>', methods=['GET', 'POST'])
def product_order(pk):
    if request.method == 'GET':
        form = AddressForm()
        form.city.query = City.query.filter(None).all()
        return render_template('order.html', form=form, id=pk)

    if request.method == 'POST':
        country = request.form['country']
        city = request.form['city']
        address = request.form['address']
        amount = request.form['amount']

        address_add = Address(city_id=city, address=address)
        db.session.add(address_add)
        db.session.commit()

        address_id = Address.query.filter_by(address=address).first().id
        order = Order(address_id=address_id, good_id=pk, amount=amount, status='Delivering')
        db.session.add(order)
        db.session.commit()
        order_status_changing.delay(order.id)

        return redirect('/')


@flask_app.route('/get-cities')
def get_cities():
    country_id = request.args.get('country', type=int)
    cities = City.query.filter_by(country_id=country_id).all()
    return render_template('city_options.html', cities=cities)


@flask_app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'GET':
        return render_template('login.html')

    elif request.method == 'POST':
        login = request.form['login']
        password = request.form['password']
        user = User.query.filter_by(login=login).first()
        if check_password_hash(user.password, password):
            login_user(user)
            return redirect('/')
        else:
            flash('Логін або пароль невірні')
            return redirect('/login')


@flask_app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        login = request.form.get('login')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        if login and password1 and password2:
            if password1 == password2:
                pass_hash = generate_password_hash(password2)
                user = User(login=login, password=pass_hash)
                db.session.add(user)
                db.session.commit()
                return redirect('/login')
            flash('Паролі не збігаються')
        else:
            flash('Заповніть всі поля')
            return render_template('register.html')


@flask_app.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect('/')


@flask_app.route('/api/v1/order/<int:order_id>', methods=['GET'])
def orderAPI(order_id):
    order_json = {}
    order = Order.query.get(order_id)
    order_json['id'] = order.id
    order_json['amount'] = order.amount
    order_json['status'] = order.status
    order_json['product'] = Gods.query.get(order.good_id).name

    address = Address.query.get(order.address_id)
    city = City.query.get(address.city_id)
    country = Country.query.get(city.country_id)
    order_json['address'] = f'{country.name}, {city.name}, {address.address}'
    return jsonify(order_json)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


if __name__ == '__main__':
    flask_app.run(debug=True, host='0.0.0.0')


