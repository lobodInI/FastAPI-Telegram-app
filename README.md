# FastAPI-Telegram-app
The project was carried out according to the conditions and recommendations of the technical specifications:
```bash
https://docs.google.com/document/d/1XD6q9Y2dtP4gyyKNA6BIjmI6cevjjArsXUhHyN0oSrA/edit
```

## Starting the Application

###### Install PostgresSQL and create db

### Installation
1. Navigate to the project directory:
```
cd projects/fastapi_telegram_app
```

2. Clone this repository:
```
git clone https://github.com/lobodInI/FastAPI-Telegram-app/tree/development
```

3. Create a virtual environment:
```
python -m venv venv
```

4. Activate the virtual environment:

- On Windows:

  ```
  venv\Scripts\activate
  ```

- On macOS/Linux:

  ```
  source venv/bin/activate
  ```
  
5. Install dependencies:
```
pip install -r requirements.txt
```

6. Create and fill out a `.env` file following the example of `.env.sample`
## Migrations

### Creating Migrations

To create a new migration, use the following command:
```
alembic revision --autogenerate -m "Add new table"
```

### Applying Migrations
To apply migrations and update the database schema, use the following command:
```
alembic upgrade head
```

### Rolling Back Migrations
Use the downgrade command followed by the revision ID:
```
alembic downgrade <revision_id>
```

### Running the Application

To start the application, run the following command:
```
python -m app.main
```
## Documentation
Use FastAPI Swagger UI - http://127.0.0.1:8000/docs

## Endpoints

- http://127.0.0.1:8000/auth/signin/ - getting a login JWT token
- http://127.0.0.1:8000/user/all/ - information about all users in the system
- http://127.0.0.1:8000/user/{user_id}/ - information about one user with a specific ID
- http://127.0.0.1:8000/user/create/ - creating new user
- http://127.0.0.1:8000/user/update/{user_id}/ - update user with a specific ID
- http://127.0.0.1:8000/user/delete/{user_id}/ - delete user with a specific ID
- http://127.0.0.1:8000/me/ - information about the current user
- http://127.0.0.1:8000/request/all/ - information about all requests according to the role
- http://127.0.0.1:8000/request/{request_id}/ - information about one request with a specific ID
- http://127.0.0.1:8000/request/create/ - creating new request (bot ID must exist and be in chat with chat ID)
- http://127.0.0.1:8000/request/delete/ - delete request with a specific ID

## Loading test data

```
python -m app.dump_test_data
```