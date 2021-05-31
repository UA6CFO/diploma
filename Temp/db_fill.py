from app import db
from app.models import User


# создаем экземпляр класса User
new_user = User(name="Иван")

# добавляем изменения в базу данных (при этом база не сохраняется)
db.session.add(new_user)

# сохраняем изменения в базе
db.session.commit()