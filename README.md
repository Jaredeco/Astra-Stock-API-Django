# Django Rest Framework Bond Service API

The Bond Service API is a secure and efficient financial tool that enables administrators to manage bonds through create, retrieve, update, and delete functionalities. Regular users can access their investment portfolio, create new investments, purchase bonds, and manage their holdings. The API also includes robust ISIN validation to ensure the accuracy and authenticity of bond data, enhancing data integrity and providing a comprehensive solution for managing financial assets.

## API Structure

The Django Rest Framework Bond Service API follows the principles of a RESTful API, where endpoints (URLs) define the structure and access points of the API. The endpoints are logically organized around collections and elements, which represent resources.

The API has the following endpoints:

- **Bonds Endpoints:**
  - `GET /bonds/`: Retrieve a list of all bonds. (No authentication required)
  - `POST /bond/`: Create a new bond. (Admin privileges required)
  - `GET /bond/<isin>/`: Retrieve a specific bond by its ISIN. (No authentication required)
  - `PUT /bond/<isin>/`: Update a specific bond by its ISIN. (Admin privileges required)
  - `DELETE /bond/<isin>/`: Delete a specific bond by its ISIN. (Admin privileges required)

- **Users Endpoint:**
  - `GET /users/`: Retrieve a list of all users. (Admin privileges required)

- **Portfolio Analysis Endpoint:**
  - `GET /portfolio/`: Analyze the investment portfolio of the authenticated user. (User authentication required)
  - `GET /portfolio/bonds/`: Retrieve a list of all bonds in portfolio of the authenticated user. (User authentication required)
  - `GET /portfolio/investments/`: Retrieve a list of all investments in portfolio of the authenticated user. (User authentication required)

- **Investments Endpoints:**
  - `POST /investment/`: Purchase a bond by providing the username, bond ISIN, and volume. (User authentication required)
  - `GET /investment/<id>/`: Retrieve a specific investment by its ID. (User authentication required)
  - `PUT /investment/<id>/`: Update a specific investment by its ID. (User authentication required)
  - `DELETE /investment/<id>/`: Delete a specific investment by its ID. (User authentication required)

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

#### Bonds

##### List all bonds

Endpoint: `GET /api/v1/bonds/`

Returns a list of all bonds in the system.

Request:

```
http GET http://localhost:8000/api/v1/bonds/
```

Permissions: None (public access)

##### Create a new bond

Endpoint: `POST /api/v1/bond/`

Creates a new bond and returns the bond details.

Request:

```
http POST http://localhost:8000/api/v1/bond/ "Authorization: Token {YOUR_TOKEN}" name="Test Bond" isin="TEST12345678" value=1000 interest_rate=0.05 purchase_date="2023-01-01" expiration_date="2024-01-01" interest_payment_frequency="Annual"
```

Permissions: Admin privileges required

##### Retrieve, update, and delete a bond

Endpoint: `GET/PUT/DELETE /api/v1/bond/<isin>/`

Retrieves, updates, or deletes a bond with the given ISIN.

Request:

```
http GET http://localhost:8000/api/v1/bond/<isin>/ "Authorization: Token {YOUR_TOKEN}"
http PUT http://localhost:8000/api/v1/bond/<isin>/ "Authorization: Token {YOUR_TOKEN}" name="Updated Bond" value=1500
http DELETE http://localhost:8000/api/v1/bond/<isin>/ "Authorization: Token {YOUR_TOKEN}"
```

Permissions: Admin privileges required

#### Investments

##### List all investments

Endpoint: `GET /api/v1/investments/`

Returns a list of all investments in the system.

Request:

```
http GET http://localhost:8000/api/v1/investments/ "Authorization: Token {YOUR_TOKEN}"
```

Permissions: None (public access)

##### Create a new investment

Endpoint: `POST /api/v1/investment/`

Creates a new investment and returns the investment details.

Request:

```
http POST http://localhost:8000/api/v1/investment/ "Authorization: Token {YOUR_TOKEN}" username="username" bond_isin="TEST12345678" volume=10
```

Permissions: User authentication required

##### Retrieve, update, and delete an investment

Endpoint: `GET/PUT/DELETE /api/v1/investment/<pk>/`

Retrieves, updates, or deletes an investment with the given primary key (pk).

Request:

```
http GET http://localhost:8000/api/v1/investment/<pk>/ "Authorization: Token {YOUR_TOKEN}"
http PUT http://localhost:8000/api/v1/investment/<pk>/ "Authorization: Token {YOUR_TOKEN}" volume=5
http DELETE http://localhost:8000/api/v1/investment/<pk>/ "Authorization: Token {YOUR_TOKEN}"
```

Permissions: User authentication required

#### Portfolio Analysis

Endpoint: `GET /api/v1/portfolio/analyze/`

Analyzes the authenticated user's portfolio and returns various metrics, including the average interest rate, soon-to-expire bonds, portfolio balance, and future portfolio balance.

Request:

```
http GET http://localhost:8000/api/v1/portfolio/analyze/ "Authorization: Token {YOUR_TOKEN}"
```

Permissions: User authentication required

#### User Portfolio

Endpoint: `GET /api/v1/portfolio/bonds/`

Returns a list of all bonds in the authenticated user's portfolio.

Request:

```
http GET http://localhost:8000/api/v1/portfolio/bonds/ "Authorization: Token {YOUR_TOKEN}"
```

Permissions: User authentication required

Endpoint: `GET /api/v1/portfolio/investments/`

Returns a list of all investments in the authenticated user's portfolio.

Request:

```
http GET http://localhost:8000/api/v1/portfolio/investments/ "Authorization: Token {YOUR_TOKEN}"
```

Permissions: User authentication required

### ISIN Validation
The application validates the International Securities Identification Number (ISIN) before creating a new bond. The ISIN validation ensures that the entered ISIN exists and is valid according to the Czech Central Depository for Securities (CDCP) database.

If the provided ISIN is invalid or not found in the database, the system will raise a validation error and prevent the bond from being created.

The validation process sends a GET request to the CDCP API https://www.cdcp.cz/isbpublicjson/api/VydaneISINy with the provided ISIN as a parameter. If the CDCP API returns a status code other than 200, indicating an error, the validation fails, and the bond creation is halted.

Please note that the ISIN validation requires an active internet connection to access the CDCP API. The validation process helps to ensure data integrity and accuracy within the application.

### Additional Notes

- The API has some restrictions:
  - Only authenticated users can create and access bonds and investments.
  - Users can only update or delete their own investments.
  - The API doesn't allow unauthenticated requests.

- Authentication is done using JWT tokens. Users must obtain an access token to perform authenticated actions. Tokens can be obtained by registering a new user or using existing credentials to obtain an access token.

- Feel free to explore the API using tools like `curl`, `httpie`, or [Postman](https://www.postman.com/) to interact with the endpoints.

For any further assistance or questions, please refer to the documentation or reach out to the API maintainers. Happy coding!