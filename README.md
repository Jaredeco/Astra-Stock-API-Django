# Django Rest Framework Bond Service API

This is a Django Rest Framework API for managing bonds and investments. It allows authenticated users to perform CRUD operations on bonds and investments, as well as analyze their portfolio. Users can register and obtain a token for authentication, which is required for all API endpoints.

## API Structure

In this RESTful API, endpoints (URLs) define the structure of the API and how end users access data from our application using the HTTP methods - GET, POST, PUT, DELETE. Endpoints are logically organized around different resources.

### Bonds

- `GET /api/v1/bonds/`: List all bonds.
- `POST /api/v1/bond/`: Create a new bond.
- `GET /api/v1/bond/<isin>/`: Retrieve a specific bond.
- `PUT /api/v1/bond/<isin>/`: Update a specific bond.
- `DELETE /api/v1/bond/<isin>/`: Delete a specific bond.

### Investments

- `GET /api/v1/investments/`: List all investments.
- `POST /api/v1/investment/`: Create a new investment.
- `GET /api/v1/investment/<pk>/`: Retrieve a specific investment.
- `PUT /api/v1/investment/<pk>/`: Update a specific investment.
- `DELETE /api/v1/investment/<pk>/`: Delete a specific investment.

### Portfolio Analysis

- `GET /api/v1/portfolio/<username>/`: Analyze the user's portfolio.

### User Portfolio

- `GET /api/v1/portfolio/bonds/<username>/`: List all bonds in the user's portfolio.
- `GET /api/v1/portfolio/investments/<username>/`: List all investments in the user's portfolio.

### Authentication and User Management

- `POST /api/v1/authenticate/`: Authenticate the user or register a new user.
- `GET /api/v1/users/`: List all users. (Admin-only endpoint)

Users can authenticate using the `/api/v1/authenticate/` endpoint, which registers the user if no account exists or authenticates if the user already exists. Once authenticated, users can obtain a token for authentication, which is required for all API endpoints.

## Requirements
- Python 3.6 or higher
- Django 3.1 or higher
- Django REST Framework

## Installation
1. Clone the repository:

```
git clone <repository_url>
cd bond_service_api
```

2. Create a virtual environment and activate it:

```
python -m venv env
source env/bin/activate  # On Windows, use `env\Scripts\activate`
```

3. Install the required dependencies:

```
pip install -r requirements.txt
```

## Usage

### Running the API

To start the Django development server:

```
python manage.py runserver
```

The API will be accessible at `http://localhost:8000/`.

### Running the Tests

To run the tests for views, use the following command:

```
python manage.py test base.tests.views_tests
```

To run the tests for models, use the following command:

```
python manage.py test base.tests.models_tests
```

The tests ensure the functionality and correctness of the models and views in the API.

### API Documentation

The API documentation is available in Swagger format. To access the Swagger documentation, visit:

```
http://localhost:8000/api/v1/docs/
```

The Swagger documentation provides a detailed view of the API endpoints, allowing users to interact with and test the API directly from the browser.

### Docker

To run the API in Docker, follow these steps:

1. Build the Docker image:

```
docker build -t bond_service_api .
```

2. Run the Docker container:

```
docker run -p 8000:8000 bond_service_api
```

The API will be accessible at `http://localhost:8000/`.

### API Endpoints

#### Authentication

##### Register a new user

Endpoint: `POST /api/v1/auth/register/`

Creates a new user and returns the user details.

Request:

```
http POST http://localhost:8000/api/v1/auth/register/ email="email@email.com" username="USERNAME" password1="PASSWORD" password2="PASSWORD"
```

##### Obtain an access token

Endpoint: `POST /api/v1/auth/token/`

Obtains an access token for an existing user. The access token is required for authentication.

Request:

```
http POST http://localhost:8000/api/v1/auth/token/ username="username" password="password"
```

##### Refresh an access token

Endpoint: `POST /api/v1/auth/token/refresh/`

Refreshes an access token using a refresh token.

Request:

```
http POST http://localhost:8000/api/v1/auth/token/refresh/ refresh="REFRESH_TOKEN"
```

#### Bonds

##### List all bonds

Endpoint: `GET /api/v1/bonds/`

Returns a list of all bonds in the system.

Request:

```
http GET http://localhost:8000/api/v1/bonds/ "Authorization: Token {YOUR_TOKEN}"
```

##### Create a new bond

Endpoint: `POST /api/v1/bond/`

Creates a new bond and returns the bond details.

Request:

```
http POST http://localhost:8000/api/v1/bond/ "Authorization: Token {YOUR_TOKEN}" name="Test Bond" isin="TEST12345678" value=1000 interest_rate=0.05 purchase_date="2023-01-01" expiration_date="2024-01-01" interest_payment_frequency="Annual"
```

##### Retrieve, update, and delete a bond

Endpoint: `GET/PUT/DELETE /api/v1/bond/<isin>/`

Retrieves, updates, or deletes a bond with the given ISIN.

Request:

```
http GET http://localhost:8000/api/v1/bond/<isin>/ "Authorization: Token {YOUR_TOKEN}"
http PUT http://localhost:8000/api/v1/bond/<isin>/ "Authorization: Token {YOUR_TOKEN}" name="Updated Bond" value=1500
http DELETE http://localhost:8000/api/v1/bond/<isin>/ "Authorization: Token {YOUR_TOKEN}"
```

#### Investments

##### List all investments

Endpoint: `GET /api/v1/investments/`

Returns a list of all investments in the system.

Request:

```
http GET http://localhost:8000/api/v1/investments/ "Authorization: Token {YOUR_TOKEN}"
```

##### Create a new investment

Endpoint: `POST /api/v1/investment/`

Creates a new investment and returns the investment details.

Request:

```
http POST http://localhost:8000/api/v1/investment/ "Authorization: Token {YOUR_TOKEN}" username="username" bond_isin="TEST12345678" volume=10
```

##### Retrieve, update, and delete an investment

Endpoint: `GET/PUT/DELETE /api/v1/investment/<pk>/`

Retrieves, updates, or deletes an investment with the given primary key (pk).

Request:

```
http GET http://localhost:8000/api/v1/investment/<pk>/ "Authorization: Token {YOUR_TOKEN}"
http PUT http://localhost:8000/api/v1/investment/<pk>/ "Authorization: Token {YOUR_TOKEN}" volume=5
http DELETE http://localhost:8000/api/v1/investment/<pk>/ "Authorization: Token {YOUR_TOKEN}"
```

#### Portfolio Analysis

Endpoint: `GET /api/v1/portfolio/<username>/`

Analyzes the user's portfolio and returns various metrics, including the average interest rate, soon-to-expire bonds, portfolio balance, and future portfolio balance.

Request:

```
http GET http://localhost:8000/api/v1/portfolio/<username>/ "Authorization: Token {YOUR_TOKEN}"
```

#### User Portfolio

Endpoint: `GET /api/v1/portfolio/bonds/<username>/`

Returns a list of all bonds in the user's portfolio.

Request:

```
http GET http://localhost:8000/api/v1/portfolio/bonds/<username>/ "Authorization: Token {YOUR_TOKEN}"
```

Endpoint: `GET /api/v1/portfolio

/investments/<username>/`

Returns a list of all investments in the user's portfolio.

Request:

```
http GET http://localhost:8000/api/v1/portfolio/investments/<username>/ "Authorization: Token {YOUR_TOKEN}"
```

### Additional Notes

- The API has some restrictions:
  - Only authenticated users can create and access bonds and investments.
  - Users can only update or delete their own investments.
  - The API doesn't allow unauthenticated requests.

- Authentication is done using JWT tokens. Users must obtain an access token to perform authenticated actions. Tokens can be obtained by registering a new user or using existing credentials to obtain an access token.

- Feel free to explore the API using tools like `curl`, `httpie`, or [Postman](https://www.postman.com/) to interact with the endpoints.

For any further assistance or questions, please refer to the documentation or reach out to the API maintainers. Happy coding!