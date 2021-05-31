from app import db
from datetime import datetime


class User(db.Model):
    id_user = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), unique = True)
    name = db.Column(db.String(128))

class Rents(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_auto = db.Column(db.Integer)
    datetime_begin = db.Column(db.DateTime, default=datetime.now)  # Дата и время начала аренды
    datetime_end = db.Column(db.DateTime, default=None)  # Дата и время завершения аренды
    total_cost = db.Column(db.Integer)

class Auto(db.Model):
    id_auto = db.Column(db.Integer, primary_key=True)  # Идентификатор
    name_auto = db.Column(db.String(128))  # Автомобиль
    auto_description = db.Column(db.String(128))  # Описание автомобиля (картинка ?)
    transm = db.Column(db.Boolean, default=False)  # коробка передач
    price = db.Column(db.Integer)  # Стоимость аренды
    in_rent = db.Column(db.Boolean, default=False)  # Статус аренды
    datetime_begin = db.Column(db.DateTime, default=datetime.now)  # Дата и время начала аренды
    datetime_end = db.Column(db.DateTime, default=datetime.now)  # Дата и время завершения аренды
    total_cost = db.Column(db.Integer, default=0)  # Общая стоимость аренды
    n_rent = db.Column(db.Integer, default=0)  # Количество бронирований
    total_time = db.Column(db.Integer, default=0)  # Общее время аренды
    img_url = db.Column(db.String(128)) #путь к изображению
    