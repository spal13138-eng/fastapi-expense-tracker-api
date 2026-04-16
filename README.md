# Expense Tracker API

![Python](https://img.shields.io/badge/Python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-blue)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-ORM-red)

A FastAPI-based backend project for managing personal expenses. Users can securely create, update, delete, and analyze their expenses with authentication, pagination, category-wise tracking, and daily/monthly summaries.


## Features

* Secure User Signup and Login
* JWT Authentication
* User-specific expense management
* CRUD operations for expenses
* Pagination and sorting
* Filtering by category
* Daily, monthly, and category-wise expenditure tracking
* Highest and lowest expense by category
* PostgreSQL database integration
* Alembic migrations


## Tech Stack

* Python
* FastAPI
* PostgreSQL
* SQLAlchemy
* Alembic
* JWT Authentication

## Project Structure

```text
app/
├── routers/
│   ├── expense.py
│   ├── user.py
│   ├── auth.py
├── config.py
├── database.py
├── main.py
├── models.py
├── oauth2.py
├── schemas.py
├── utils.py
├── alembic/
│   ├── versions/
│   ├── env.py
├── alembic.ini
├── requirements.txt
├── README.md
```


## Installation

Clone the repository:

```bash
git clone <your-github-repo-url>
cd Expense Tracker API
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate the virtual environment:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```


## Environment Variables

Create a `.env` file in the root directory:

```env
DATABASE_URL=your_database_url
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```


## Run the Project

```bash
uvicorn app.main:app --reload
```

API documentation available at:

```text
http://127.0.0.1:8000/docs
```


## API Endpoints

### Authentication

```text
POST /signup
POST /login
```

### Expenses

```text
GET /expenses
GET /expenses/{id}
POST /expenses
PUT /expenses/{id}
DELETE /expenses/{id}
```

### Analytics

```text
GET /expenses/daily-total/{date}
GET /expenses/monthly-total/{month}
GET /expenses/category-total/{category}
GET /expenses/highest-expense/{category}
GET /expenses/lowest-expense/{category}
```


## Future Improvements

* Receipt upload
* CSV export
* Budget tracking
* Redis caching
* Pytest testing


## Author

Shiva
