# Available Endpoints
| HTTP Methods | Endpoint                               | Description                  |
| ------------ | --------------------------------------- | ----------------------------- |
| GET, PUT, DELETE | /store/products/{id}/                  | Retrieve, update, or delete a specific product.               |
| GET, POST | /store/products/                        | Retrieve a list of all products or create a new product.      |
| GET, PUT, DELETE | /store/collections/{id}               | Retrieve, update, or delete a specific collection.           |
| GET, POST | /store/collections/                   | Retrieve a list of all collections or create a new collection. |
| GET, PUT, DELETE | /store/products/{id}/reviews/{review_id} | Retrieve, update, or delete a specific product review.   |
| GET, POST | /store/products/{id}/reviews/        | Retrieve a list of product reviews or add a new review.      |
| GET, POST | /store/carts/                         | Retrieve a list of user carts or create a new cart.         |
| GET, PUT, DELETE | /store/carts/{uuid}/items/{item_id}/  | Retrieve, update, or delete a specific item in a cart.     |
| GET, POST | /store/carts/{uuid}/items/            | Retrieve a list of items in a cart or add a new item.        |
| GET, PUT, DELETE | /store/users/{id}/                   | Retrieve, update, or delete a specific user.               |
| GET, POST | /auth/users/                         | Retrieve a list of all users or create a new user.          |
| POST | /auth/jwt/create/                     | Obtain a JWT access token for authentication.             |
| POST | /auth/jwt/refresh/                    | Refresh an existing JWT access token.                    |
| GET, PUT, DELETE | /store/customers/{id}/               | Retrieve, update, or delete a specific customer.           |
| GET, POST | /store/customers/                   | Retrieve a list of all customers or create a new customer.  |
| GET, PUT | /store/customers/me/                 | Retrieve, update the profile of the authenticated customer.       |
