Для начала нужно установить все зависимости

pip install -r requirements.txt

У вас должен быть установлен redis 

Создаайте файл .env в который запишите данные согласно шаблону (.env.sample)

Сделайте миграцию -> python manage.py migrate

Загрузите данные с фикстуры -> python manage.py loaddata data1.json

ВАЖНО! Перед тем как создать superuser закомментируйте метод save в приложении users\models.py.

После выполните команду -> python manage.py createsuperuser

После разкомментируйте(верните обратно) метод save в приложении users\models.py.

#############

Для запуска сервиса используйте команду -> python manage.py runserver

Для запуска рассылок используется библиотека schedule. Она позволяет запускать функции по расписанию.

Для запуска рассылок используйте команду ->  python manage.py services

