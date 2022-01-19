# ecommerce-app

E-commerce app build with django on the back-end and react on the front-end

It allows for login, users, roles and permissions; products, orders and cart.

## Execute the following for first time

### Build container

$ docker-compose up

### Enter container

$ docker-compose exec admin_api sh

### Run migrations

$ python3 manage.py makemigrations

$ python3 manage.py migrate

### Load data from fixtures

$ python3 manage.py loaddata fixtures/filename.json
