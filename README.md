### Django REST API - Book Management

This is a Django REST Framework-based API built for managing users, books, and personal reading lists as part of an assessment project.

---

### 🔑 Authentication

* Token-based authentication using JWT.
* Access token returned in response.
* Refresh token stored in cookies and can be used to get a new access token.

---

### 📌 API Endpoints Summary

#### ✅ User Auth:

* `POST /api/v1/accounts/register/` – Register a new user
* `POST /api/v1/accounts/login/` – Log in and receive JWT tokens
* `POST /api/v1/accounts/refresh/` – Refresh access token using refresh cookie
* `GET /api/v1/accounts/profile/` – Get current user profile (auth required)

#### 📘 Books:

* `GET /api/v1/books/` – List all books
* `POST /api/v1/books/` – Add a new book (auth required)
* `GET /api/v1/books/:id/` – Retrieve a specific book
* `PATCH /api/v1/books/:id/` – Update a book (owner only)
* `DELETE /api/v1/books/:id/` – Delete a book (owner only)

#### 📚 Reading Lists:

* `GET /api/v1/books/reading-lists/` – List your reading lists (auth required)
* `POST /api/v1/books/reading-lists/` – Create a new reading list
* `PATCH /api/v1/books/reading-lists/:id/` – Update reading list name
* `DELETE /api/v1/books/reading-lists/:id/` – Delete a reading list

#### 📖 Reading List Items:

* `POST /api/v1/books/reading-lists/:id/add/` – Add a book to the list
* `PATCH /api/v1/books/reading-lists/:id/update-position/` – Change book position
* `DELETE /api/v1/books/reading-lists/:id/remove/` – Remove a book from the list

---

### 🗂️ Project Structure

* `accounts/` – User registration, login, token management
* `books/` – Book and reading list management
* `backend/` – Project configs and URLs

---

### 🚀 Setup

1. `git clone https://github.com/AswinNarayananT/book-management.git`
2. Create venv: `python -m venv venv && venv\Scripts\activate`
3. Install deps: `pip install -r requirements.txt`
4. Add `.env` with Django settings
5. Run: `python manage.py migrate && python manage.py runserver`

---

### 👨‍💻 Author

Aswin Narayanan T

---

### 📝 License

For assessment and learning use only.
