Django REST API - Book Management

This is a Django REST Framework-based API built for managing users, books, and personal reading lists as part of an assessment project.

---

Features

- User registration, login, and profile management
- Book creation, viewing, updating, and deletion
- Public access to all books
- Personalized reading lists for users
- Add/remove books from reading lists
- Token-based authentication using JWT
- Input validation and informative error responses

---

Setup Instructions (Windows)

1. Clone the Project  
Run the following command in your terminal:
git clone https://github.com/yourusername/book-management-api.git
cd backend

2. Create and Activate Virtual Environment  
python -m venv venv  
venv\Scripts\activate

3. Install Dependencies  
pip install -r requirements.txt

4. Create .env File in the Root Directory  
Create a file named .env and add the following:
DEBUG=True  
SECRET_KEY=your-secret-key  
ALLOWED_HOSTS=127.0.0.1,localhost  
CSRF_TRUSTED_ORIGINS=http://127.0.0.1,http://localhost

5. Run Migrations  
python manage.py makemigrations  
python manage.py migrate

6. Create Superuser (Admin)  
python manage.py createsuperuser

7. Run Development Server  
python manage.py runserver

The API will be available at:  
http://127.0.0.1:8000

---

Authentication

The API uses JWT authentication. Tokens are issued upon login and must be included in the Authorization header for protected endpoints.

Example:
Authorization: Bearer your_access_token

---

API Endpoints

API documentation will be added here.

---

Project Structure

backend/
├── accounts/          (User authentication and profile management)
├── backend/           (Project settings and URLs)
├── books/             (Book and reading list features)
├── manage.py
├── requirements.txt
└── README.md

---

Author

Your Name

---

License

This project is created for assessment and learning purposes only.
