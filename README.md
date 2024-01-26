# Employee

### Зависимости
1. Django==5.0.1 - основной фреймворк
2. django-mptt==0.16.0 - хранение деревьев в базе
3. django-seed==0.3.1 - заполнение тестовых данных
4. Pillow==10.2.0 - обработка изображений
5. environs==10.3.0 - чтение переменных окружения

### Установка
1. Установите зависимости проекта ```pip install -r requirements.txt```
2. Запустите postgres базу данных в контейнере ```docker-compose -f docker-compose-dev.yml up -d```
3. Создайте файл ```.env``` рядом с ```.env.sample``` и заполните по аналогии с примером
    ```
   # Приложение
   # опциональные переменные
   DJANGO_DEBUG=
   DJANGO_ALLOWED_HOSTS=
   DJANGO_SECRET=
   
   # База данных
   # обязательные переменные
   DB_HOST=localhost
   DB_PORT=5432
   DB_NAME=db
   DB_USER=admin
   DB_PASSWORD=password
   # опциональные переменные
   DB_ENGINE=django.db.backends.postgresql

    ```
4. Выполните миграции ```python employee_directory/manage.py migrate```
5. Заполните базу тестовыми данными ```python employee_directory/manage.py fill_employees```
   - --tree_id - ключ, отвечающий за то, в какое дерево создавать сотрудников (если не передано - создает новое)
   - --count - количество сотрудников (по умолчанию - 50_000)
   - --max_lvl - максимальный уровень иерархии (по умолчанию 5)
6. Запустите сервер ```python employee_directory/manage.py runserver```