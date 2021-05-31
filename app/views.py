from app import app, db
from app.models import User, Auto, Rents
from flask import render_template, request
from datetime import datetime
import os
from werkzeug.utils import secure_filename


UPLOAD_FOLDER = "./app/static/assets/images/auto"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    
    auto_list = Auto.query.all()  # Получаем все записи из таблицы Auto
    user_list = User.query.all()  # Получаем все записи из таблицы User
    # Полученные наборы передаем в контекст
    context = {
        'auto_list': auto_list,
        'user_list': user_list,
    }

    return render_template('index.html', **context)

@app.route('/rental_log')
def log():
    
    auto_list = Auto.query.all()  # Получаем все записи из таблицы Auto
    user_list = User.query.all()  # Получаем все записи из таблицы User
    # Полученные наборы передаем в контекст
    context = {
        'auto_list': auto_list,
        'user_list': user_list,
    }

    return render_template('rental_log.html', **context)


@app.route('/create_auto', methods=['POST', 'GET'])
def create_auto():

    context = None
    
    if request.method == 'POST':
        
        # Пришел запрос с методом POST (пользователь нажал на кнопку 'Добавить авто')
        # auto_id = request.form['id_auto'] 
        auto_name = request.form['name']
        # Получаем цену аренды авто - это значение поля input с атрибутом name="price"
        auto_price = request.form['price']
        
        if request.form['transmission'] == 'option1':
            transm = True
        else:
            transm = False
        # Добавляем авто в базу данных
        auto = Auto(name_auto=auto_name, price=auto_price, auto_description=request.form['description'], transm=transm)
        db.session.add(auto)
        db.session.flush()
        id = auto.id_auto

        # сохраняем изображения авто
        files = request.files.getlist('file')
        number = 1
        for file in files:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'auto' + str(id) + str(number) + '.jpg'))
            number += 1

        # сохраняем изменения в базе
        db.session.commit()

        # Заполняем словарь контекста
        context = {
            'method': 'POST',
            'title': auto_name,
            'price': auto_price,
        }
    
    elif request.method == 'GET':

        # Пришел запрос с методом GET - пользователь просто открыл в браузере страницу по адресу http://127.0.0.1:5000/create_product
        # В этом случае просто передаем в контекст имя метода
        context = {
            'method': 'GET',
        }

    return render_template('create_auto.html')

@app.route('/change_auto/<int:id_auto>', methods=['POST', 'GET'])
def change_auto(id_auto):

    context = None
    
    if request.method == 'POST':
        product = Auto.query.get(id_auto)
        # Пришел запрос с методом POST (пользователь нажал на кнопку 'Изменить')
        # auto_id = request.form['id_auto'] 
        auto_name = request.form['name']
        # Получаем цену аренды авто - это значение поля input с атрибутом name="price"
        auto_price = request.form['price']
        auto_description = request.form['description']

        if request.form['transmission'] == 'option1':
            transm = True
        else:
            transm = False
        
        product.name_auto = auto_name
        product.price = auto_price
        product.description = auto_description
        product.transm = transm
        # сохраняем изменения в базе
        db.session.commit()

        # сохраняем изображения авто
        files = request.files.getlist('file')
        number = 1
        for file in files:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'auto' + str(id_auto) + str(number) + '.jpg'))
            number += 1

        # Заполняем словарь контекста
        context = {
            'method': 'POST',
            'title': auto_name,
            'price': auto_price,
        }
    
    elif request.method == 'GET':
        product = Auto.query.get(id_auto)

        auto_name = product.name_auto
        auto_description = product.auto_description
        auto_price = product.price
        context = {
            'method': 'GET',
            'title': auto_name,
            'price': auto_price,
            'description': auto_description,
        }

    return render_template('change_auto.html', **context)


@app.route('/create_user', methods=['POST', 'GET'])
def create_user():

    context = None

    if request.method == 'POST':
        
        name = request.form['name']
        username = request.form['username']

        db.session.add(User(name=name, username=username))
        db.session.commit()

        context = {
            'method': 'POST',
            'name': name,
            'username': username,
        }
    
    elif request.method == 'GET':

        context = {
            'method': 'GET',
        }

    return render_template('create_user.html', **context)


@app.route('/auto_detail/<int:id_auto>', methods=['POST', 'GET'])
def product_detail(id_auto):
    
    product = Auto.query.get(id_auto)

    context = None

    if request.method == 'POST':
        if request.form.get("rent"):
            if not product.in_rent:
                product.in_rent = True
                rent = Rents(id_auto=id_auto, datetime_begin=datetime.now())
                db.session.add(rent)
            else:
                product.in_rent = False
                rent = Rents.query.filter_by(id_auto=id_auto, datetime_end=None).first()
                rent.datetime_end = datetime.now()
                rent.total_cost = product.price * ((rent.datetime_end -  rent.datetime_begin).total_seconds() // 60.0)
                product.n_rent += 1
                product.total_time += ((rent.datetime_end -  rent.datetime_begin).total_seconds() // 60.0)
                product.total_cost += rent.total_cost
        # сохраняем изменения в базе
    db.session.commit()

        #new_name_auto = request.form['new_name_auto']
        #new_price = request.form['new_price']
        #new_auto_description = request.form['new_auto_description']
        #new_img_url = request.form['auto_description']

        # if new_name_auto:
        #     Auto.name_auto = request.form['new_name_auto']
        
        # if new_price:
        #     Auto.price = request.form['new_price']
        
        # if new_img_url:
        #     product.Auto = request.form['new_auto_description']

        # db.session.commit()

    #age_seconds = (datetime.now() - Auto.created).seconds
    #age_seconds = 3600
    #age = divmod(age_seconds, 60)
    if product.in_rent:
        rent_act = 'Освободить'
        is_rent = 'Занят'
    else:
        rent_act = 'Арендовать'
        is_rent = 'Свободен'
    
    if product.transm:
        transm = 'Автоматическая'
    else:
        transm = 'Механика'
    
    
    rent_list = Rents.query.filter_by(id_auto = id_auto)
    context = {
        'id': product.id_auto,
        'title': product.name_auto,
        'price': product.price,
        'rent_act': rent_act,
        'auto_description': product.auto_description,
        'is_rent': is_rent,
        #'age': f'{age[0]} мин {age[1]} сек',
        'img1': 'auto' + str(product.id_auto) + '1.jpg',
        'img2': 'auto' + str(product.id_auto) + '2.jpg',
        'img3': 'auto' + str(product.id_auto) + '3.jpg',
        'img4': 'auto' + str(product.id_auto) + '4.jpg',
        'rent_list': rent_list,
        'transm': transm
    }

    return render_template('auto_detail.html', **context)


@app.route('/del_auto/<int:id_auto>', methods=['GET'])
def del_product(id_auto):
    
    product = Auto.query.get(id_auto)
    rents = Rents.query.filter_by(id_auto=id_auto).delete()
    context = {
        'title': product.name_auto,
        'price': product.price,
        'img_url': product.auto_description,
    }
    
    db.session.delete(product)
    db.session.commit()

    return render_template('del_auto.html', **context)
