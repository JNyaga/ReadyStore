<!-- START doctoc generated TOC please keep comment here to allow auto update -->

<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

**Table of Contents**

- [READY STORE](#ready-store)
  - [Installation/Usage locally](#installationusage-locally)
    - [Requirements:](#requirements)
    - [Install redis](#install-redis)
    - [Install `pyenv` to manage python in OS:](#install-pyenv-to-manage-python-in-os)
      - [Install `pipenv` to manage project environment:](#install-pipenv-to-manage-project-environment)
    - [USAGE:](#usage)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

# READY STORE

- This is a django api created to aid in creation of`ecomas` application by exposing endpoints which make it easier to access needed services without building entire backend for ecomas.

Ready store API can be accessed at [ReadyStore](https://readystore.onrender.com/) `[ReadyStore](https://readystore.onrender.com/)`

Or deployed locally 👇

## Installation/Usage locally

#### Requirements:

- python3.9
- docker installed -(for redis)
- mysql installed(with default ports`3306` open)
- For`windows` its preffered to use`wsl` to run project but it will do with just the normal service

### Install redis

Best option is to run redis on docker

```python
docker run -d --name redis-stack-server -p 6379:6379 redis/redis-stack-server:latest
```

### Install `pyenv` to manage python in OS:

- **Linux(**recommended**)-**>[How to install &#39;pyenv&#39; Python version manager on Ubuntu 20.04 (hashnode.dev)](https://brain2life.hashnode.dev/how-to-install-pyenv-python-version-manager-on-ubuntu-2004)
- **Windows->**[pyenv-windows](https://github.com/pyenv-win/pyenv-win)

> After installing as per instruction in above

Run 👇 in `powershell` or `terminal` to install python 3.9 to system:

```bash
 pyenv install 3.9
```

#### Install `pipenv` to manage project environment:

```bash
pip install pipenv
```

**Then** clone the project above

```bash
git clone https://github.com/JNyaga/ReadyStore.git
```

In the `storefront/settings/dev.py` file input the values of your `mysql database` or any database you may choose(read django docs for other databases). Add the `DATABASE` setting and do as follows

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '[YOUR_DATABASE_NAME]',#choose the name you wish for you database(any)
        'HOST': 'localhost',
        'USER': '[YOUR_USERNAME]',
        'PASSWORD': '[YOUR_PASWWORD]'
    }
}

```

- Open the folder and run the following commands:

```bash



#To install the required modules
pipenv install -r requirements.txt

#Activate the environment
pipenv shell

#Run the migrations
pipenv run python manage.py makemigrations
pipenv run python manage.py migrate

#Populate database
pipenv run python manage.py seed_db

#Create admin user:
pipenv run python manage.py createsuperuser #follow the steps that follows

```

### USAGE:

Access the api at `https://readystore.onrender.com`

For `local` to run the API service you run

```bash
pipenv run python manage.py runserver
```

The API has the following endpoints

| Method | Endpoint                                       | Auth\|No auth\|Admin | Function                                                                                                                               |
| ------ | ---------------------------------------------- | -------------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| POST   | `/auth/users/`                               | no auth              | registers a new user and returns the     registered user                                                                               |
| GET    | `/auth/users/me`                             | Auth                 | returns a specific user details                                                                                                        |
| POST   | `/auth/jwt/create/`                          | no auth              | Takes a set of user credentials and returns an access and refresh JSON web token pair to prove the authentication of those credentials |
| GET    | `/store/customers/`                          | admin && auth        | Returns a list of all customers                                                                                                        |
| POST   | `/store/customers/`                          | admin && auth        | Allows  admin to add a customer                                                                                                        |
| GET    | `/store/customers/<pk>/`                     | admin && auth        | Retrieves details of customer with `id==pk`                                                                                          |
| PUT    | `/store/customers/<pk>/`                     | admin && auth        | Allows edit details of customer with `id==pk`                                                                                        |
| DELETE | `/store/customers/<pk>/`                     | admin && auth        | Deletes  details of customer with `id==pk`                                                                                           |
| GET    | `/store/customers/me/`                       | auth                 | Returns details for a specific customer                                                                                                |
| PUT    | `/store/customers/me/`                       | auth                 | Allow editing details of specific customer and returns edited details                                                                  |
| DELETE | `/store/customers/me/`                       | auth                 | Allows customer to delete their details                                                                                                |
| GET    | `/store/products/`                           | no auth              | returns a list of available products                                                                                                   |
| GET    | `/store/products/<pk>/`                      | no auth              | returns details of a specific  product with `id==pk`                                                                                 |
| PUT    | `/store/products/<pk>/`                      | admin && auth        | Edit details of a product with `id==pk`                                                                                              |
| DELETE | `/store/products/<pk>/`                      | auth && admin        | Deletes product with `id==pk`                                                                                                        |
| GET    | `/store/products/<product_pk>/images/`       | no auth              | Returns a list of images for a specifik product with `id== product_pk`                                                               |
| POST   | `/store/products/<product_pk>/images/`       | auth && admin        | adds images of specific product with `id==product_pk`                                                                                |
| GET    | `/store/products/<product_pk>/images/<pk>/`  | no auth              | return details of image with `id==pk` for product with `id==product_pk`                                                            |
| PUT    | `/store/products/<product_pk>/images/<pk>/`  | auth && admin        | Takes an image to replace image with `id==pk` for product with `id==product_pk` and returns the new image details                  |
| DELETE | `/store/products/<product_pk>/images/<pk>/`  | auth && admin        | Deletes image with `id==pk` for product with `id==product_pk` and returns the new image details                                    |
| GET    | `/store/products/<product_pk>/reviews/`      | no auth              | returns all reviews of product with `id==product_pk`                                                                                 |
| POST   | `/store/products/<product_pk>/reviews/`      | auth                 | Takes object of review for  product with `id==product_pk`                                                                            |
| GET    | `/store/products/<product_pk>/reviews/<pk>/` | no auth              | returns details of review with `id==pk` for product with `id==product_pk`                                                          |
| PUT    | `/store/products/<product_pk>/reviews/<pk>/` | auth                 | Allow editing of details of review with `id==pk` for product with `id==product_pk`                                                 |
| DELETE | `/store/products/<product_pk>/reviews/<pk>/` | auth                 | Deletes review with `id==pk` for product with `id==product_pk`                                                                     |
| GET    | `/store/collections/`                        | no auth              | returns a list of all collections                                                                                                      |
| POST   | `/store/collections/`                        | admin && auth        | Takes a title of collection and returns the collection added.                                                                          |
| GET    | `/store/collections/<pk>/`                   | no auth              | returns the details of collection with `id== pk`                                                                                     |
| PUT    | `/store/collections/<pk>/`                   | admin && auth        | Edit the title details of collection with `id== pk`                                                                                  |
| DELETE | `/store/collections/<pk>/`                   | admin && auth        | Delete the title details of collection with `id== pk`                                                                                |
| POST   | `/store/carts/`                              | no auth              | Creates an empty cart object and returns its `id`                                                                                    |
| GET    | `/store/carts/<cart_pk>/`                    | no auth              | Retrieves details of cart with `id==cart_pk`                                                                                         |
| DELETE | `/store/carts/<cart_pk>/`                    | no auth              | Deletes  cart with `id==cart_pk`                                                                                                     |
| GET    | `/store/carts/<cart_pk>/items/`              | no auth              | Lists items in cart with `id==cart_pk`                                                                                               |
| POST   | `/store/carts/<cart_pk>/items/`              | no auth              | Adds items to  cart with `id==cart_pk`                                                                                               |
| GET    | `/store/carts/<cart_pk>/items/<pk>/`         | no auth              | Gets details of item with `id== pk` in cart with `id==cart_pk`                                                                     |
| PATCH  | `/store/carts/<cart_pk>/items/<pk>/`         | no auth              | Update the quantity detail of item with `id== pk` in cart with `id==cart_pk`                                                       |
| DELETE | `/store/carts/<cart_pk>/items/<pk>/`         | no auth              | Delete item with `id== pk` in cart with `id==cart_pk`                                                                              |
| GET    | `/store/orders/`                             | auth\| admin         | Returns order list of a specific customer or all order if customer is admin                                                            |
| POST   | `/store/orders/`                             | auth                 | Takes in a `cart_id` and returns an order created from the cart,  Deletes the cart                                                   |
| GET    | `/store/orders/<pk>/`                        | auth\| admin         | returns details of particular order with `id==pk`                                                                                    |
| PATCH  | `/store/orders/<pk>/`                        | auth && admin        | Edit details of order with `id==pk`(payment details)                                                                                 |
| DELETE | `/store/orders/<pk>/`                        | auth && admin        | Deletes order with `id==pk`                                                                                                          |
