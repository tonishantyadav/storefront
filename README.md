
# Storefront

Storefront is a robust and scalable **REST API** project built using **Django** and **Django Rest Framework (DRF)**. It provides a comprehensive solution for managing store data, allowing developers to easily create, retrieve, update, and delete store-related information.

## Install and Run Locally

Setup virtual environment
```bash
Windows: python -m venv storefront-env
Unix/Mac: python3 -m venv storefront-env
```

Activate virtual environment
```bash
Windows: storefront-env\Scripts\activate.bat
Unix/Mac: source storefront-env/bin/activate
```
Clone the project and go to project directory
```bash
  git clone https://github.com/tonishantyadav/Storefront.git
  cd storefront
```

Install dependencies
```bash
  pip install -r requirements.txt
```

Start the server
```bash
  python manage.py runserver
```

Acess the API
```bash
Access the APIs at http://localhost:8000/store/
For Example-
# listing all the products
http://localhost:8000/store/products/ 
```



## Currently Available Endpoints

#### Get products and product

```
  GET /store/products
  GET /store/products/{id}
```

#### Get collections and collection

```
  GET /store/collections/
  GET /store/collections/{id}
```

#### Get product reviews and review

```
  GET /store/products/{id}/reviews
  GET /store/products/{id}/reviews/{review_id}
```

#### Get cart items and item

```
  GET /store/cart/{uuid}/items
  GET /store/cart/{uuid}/items/{item_id}
```

#### Get users and user

```
  GET /auth/users/
  GET /store/users/{id}
```

#### Get user login JWT acess token
```
  Acess token- GET /auth/jwt/create 
  Refresh token- GET /auth/jwt/refresh
```

#### Get customers and customer

```
  GET /store/customers/
  GET /store/customers/{id}
```

#### Get login customer profile

```
  GET /store/customers/me
```


## Contact
Contact
For any questions or feedback, please contact me at inishantyadav24@gmail.com.

I hope you find Storefront useful for your store management needs! Happy coding!
