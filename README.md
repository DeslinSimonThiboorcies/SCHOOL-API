<div align="center">

![Header](https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=6,11,20&height=160&section=header&text=School%20Management%20API&fontSize=36&fontColor=fff&animation=twinkling&fontAlignY=35&desc=Flask%20%7C%20JWT%20%7C%20Repository-Service%20Architecture&descAlignY=58&descSize=15)

**A RESTful backend for managing students and teachers — built with Flask, following clean Repository-Service layer architecture.**

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=flat-square&logo=flask&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-D71F00?style=flat-square&logo=python&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=flat-square&logo=mysql&logoColor=white)
![JWT](https://img.shields.io/badge/JWT-000000?style=flat-square&logo=jsonwebtokens&logoColor=white)

</div>

---

<img align="right" width="280" src="https://raw.githubusercontent.com/TheDudeThatCode/TheDudeThatCode/master/Assets/Developer.gif" alt="Developer GIF">
## 📖 About

This project is a school management backend exposing two core resources — **Students** and **Teachers** — with JWT-based authentication and role-based access control (`STUDENT`, `TEACHER`, `PRINCIPAL`). It follows a layered architecture that separates concerns cleanly:

```
Route  →  Service  →  Repository  →  Model
```

- **Route** — handles HTTP requests/responses
- **Service** — business logic and validation
- **Repository** — database queries
- **Model** — SQLAlchemy ORM schema

## ✨ Features

- Student registration & login
- Teacher registration & login
- JWT authentication for protected routes
- Role-based authorization (Principal / Teacher / Student access levels)
- View all students / view all teachers (restricted to staff roles)
- View, update, and delete individual profiles
- Passwords hashed with Werkzeug security (never stored in plain text)

----

<img align="right" width="280" src="https://media.giphy.com/media/qgQUggAC3Pfv687qPC/giphy.gif" alt="Programmer">
## 🧰 Tech Stack

| Category | Technology |
|---|---|
| Language | Python |
| Framework | Flask |
| ORM | Flask-SQLAlchemy |
| Auth | Flask-JWT-Extended |
| Database | MySQL (PyMySQL driver) |
| Config | python-dotenv |

## 🖥️ Run The Application

Start the Flask API from the project root:

```bash
python app.py
```

Start the React workspace in a second terminal:

```bash
cd school-frontend
npm install
npm run dev
```

Open `http://localhost:5173`. The frontend uses the Vite `/api` proxy locally and authenticates staff through the JWT login endpoint. Set `FRONTEND_URL` in the backend environment when deploying to a different frontend origin.

## 📂 Project Structure

```
SCHOOL API/
├── school/
│   ├── route/            # Blueprints — students_route.py, teacher_services.py
│   ├── services/         # Business logic — students_services.py, teacher_service.py
│   ├── repositories/     # DB access layer — students_repo.py, teacher_repo.py
│   ├── models/           # SQLAlchemy models — students.py, teacher.py
│   ├── utils/            # Role-based access decorators
│   ├── extensison/       # db.py, jwt.py — extension initializers
│   ├── config.py         # Environment-based configuration
│   └── __init__.py       # App factory (create_app)
├── requirements.txt
```
## 🔐 Authentication Flow

1. Register via `/register` or `/register_teachers`
2. Log in via `/login` or `/login_teachers` to receive a JWT access token
3. Pass the token as a Bearer token in the `Authorization` header for protected routes:
   ```
   Authorization: Bearer <your_jwt_token>
   ```
4. Role-based decorators (`@school_principal`, `@principal`) restrict certain routes to `TEACHER`/`PRINCIPAL` roles

## 👤 Author
**Deslin Simon Thiboorcies**

## 📫 Connect With Me

<div align="center">

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=flat-square&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/deslin-simon-94615030b)
[![Gmail](https://img.shields.io/badge/Gmail-D14836?style=flat-square&logo=gmail&logoColor=white)](mailto:deslinsimon01@gmail.com)

</div>

<div align="center">

</div>

![Footer](https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=6,11,20&height=120&section=footer&animation=twinkling)
