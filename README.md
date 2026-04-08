# 🚀 Masterblog API (Flask + JSON + Swagger)

![Python](https://img.shields.io/badge/Python-3.11%2B-blue)
![Flask](https://img.shields.io/badge/Flask-2.x-black)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Completed-success)
![Bootcamp](https://img.shields.io/badge/Masterschool-Bootcamp-orange)
![API](https://img.shields.io/badge/API-REST-green)

> A **RESTful Flask API** for managing blog posts with **JSON storage**,
> including CRUD, search, sorting, and Swagger UI documentation.

------------------------------------------------------------------------

# 📌 Overview

This project demonstrates how to:

-   Build a REST API with Flask
-   Implement full CRUD operations
-   Use JSON as a lightweight database
-   Add search & sorting functionality
-   Integrate Swagger / OpenAPI documentation
-   Connect backend with a simple frontend

------------------------------------------------------------------------

# 🖥️ Demo Flow

1.  Start the Flask backend\
2.  Open Swagger UI or frontend\
3.  Perform operations:
    -   Create posts
    -   Read posts
    -   Update posts
    -   Delete posts
    -   Search & sort posts

Run:

``` bash
python3 backend/backend_app.py
```

Swagger UI:

    http://localhost:5002/api/docs

------------------------------------------------------------------------

# ✨ Core Features

-   GET all posts
-   POST new post
-   PUT update post
-   DELETE post
-   SEARCH posts (title/content)
-   SORT posts (title/content, asc/desc)
-   JSON file persistence
-   Swagger UI documentation
-   Frontend integration

------------------------------------------------------------------------

# 📂 Project Structure

Masterblog/ │ ├── backend/ │ └── backend_app.py │ ├── masterblog-api/ │
└── data/ │ └── posts.json │ ├── static/ │ ├── main.js │ ├── styles.css
│ └── masterblog.json │ ├── index.html └── README.md

------------------------------------------------------------------------

# 🚀 Installation & Usage

## Requirements

-   Python 3.10+

Install dependencies:

``` bash
pip install flask flask-cors flask-swagger-ui
```

------------------------------------------------------------------------

## Run the API

``` bash
python3 backend/backend_app.py
```

------------------------------------------------------------------------

## Frontend Usage

Open `index.html` in browser and set API URL:

    https://<your-codio-url>/api

------------------------------------------------------------------------

# 🔗 API Endpoints

  Method   Endpoint            Description
  -------- ------------------- ------------------------------
  GET      /api/posts          Get all posts (with sorting)
  POST     /api/posts          Create new post
  PUT      /api/posts/{id}     Update post
  DELETE   /api/posts/{id}     Delete post
  GET      /api/posts/search   Search posts

------------------------------------------------------------------------

# 🧠 Technical Concepts Applied

-   REST API design
-   Flask routing
-   JSON file handling
-   CRUD operations
-   Query parameters (search & sort)
-   Error handling
-   Swagger/OpenAPI integration
-   Frontend ↔ Backend communication

------------------------------------------------------------------------

# 🔐 Error Handling

Handles:

-   Invalid JSON file
-   Missing request body
-   Missing fields (POST)
-   Invalid query parameters
-   Resource not found (404)

------------------------------------------------------------------------

# 🎓 Learning Objectives

-   Understand RESTful APIs
-   Build full backend systems
-   Work with JSON as storage
-   Structure scalable code
-   Connect frontend with API
-   Document APIs professionally

------------------------------------------------------------------------

# 📈 Portfolio Upgrade Ideas

-   Replace JSON with PostgreSQL
-   Add authentication (JWT)
-   Add pagination
-   Add user system
-   Deploy API (Docker + Cloud)
-   Switch to FastAPI for performance
-   Build React frontend

------------------------------------------------------------------------

# 🇩🇪 Kurzbeschreibung

Eine REST-API mit Flask zur Verwaltung von Blogposts.

Unterstützt CRUD, Suche, Sortierung und Swagger-Dokumentation.\
Daten werden in einer JSON-Datei gespeichert.

------------------------------------------------------------------------

# 📄 License

MIT License

------------------------------------------------------------------------

# 👤 Author

Hakan Yildirim\
Python Software Developer (AI Track)\
Masterschool Bootcamp

GitHub: https://github.com/haki36\
LinkedIn: https://linkedin.com/in/hakan-yildirim-tech
