# 📚 Library Management System (LMS)

![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-2.2-lightgrey?logo=flask)
![Jinja2](https://img.shields.io/badge/Jinja2-Templating-orange)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.0-blueviolet?logo=bootstrap)
![SQLite](https://img.shields.io/badge/SQLite3-Database-lightblue?logo=sqlite)
![Made with ❤️](https://img.shields.io/badge/Made%20with-%E2%9D%A4-red)

A full-stack Library Management System for borrowing, reviewing, and managing digital books with separate roles for users and librarians.

---

## 🔍 Project Overview

This LMS is a multi-user platform where:
- 📖 Users can register, browse e-books by section, borrow for a limited time, rate/review, or buy for lifetime access.
- 🧑‍🏫 Librarians have special permissions to manage books and sections, track user activity, and handle borrow requests.

## 🚀 Live Demo & Walkthrough

🎥 [Project Walkthrough Video](https://drive.google.com/file/d/1aWh2s0B2WL9MzVHMtz5MiUsCga_53vNu/view?usp=sharing)

## 📸 Screenshots

#### 🖥️ User Homepage
![User Homepage](https://github.com/tanishk-agrawal/Library-Management-System/blob/main/LMS-Project%20Report/LMS%20homepage.jpg?raw=true)

#### 📊 Librarian Dashboard
![Librarian Dashboard](https://github.com/tanishk-agrawal/Library-Management-System/blob/main/LMS-Project%20Report/LMS%20librarian-dash.jpg?raw=true)

## 🛠️ Tech Stack

- **Backend**: Flask, Flask-SQLAlchemy, Flask-RESTful
- **Frontend**: Jinja2, HTML, Bootstrap, CSS
- **Database**: SQLite3
- **Libraries**: 
  - `Datetime` – for managing due dates
  - `Matplotlib.pyplot` – to visualize basic stats
  - `FPDF` – for PDF generation

## 🔧 Features

- **Authentication**: Register/Login using Flask sessions
- **Librarian Dashboard**:
  - CRUD operations on sections and books
  - View basic stats and graphs
- **User Portal**:
  - Browse latest books, grouped by sections
  - Smart search (by title, author, or section)
  - Borrow books with due dates
  - Auto-revocation of access after due
  - Add reviews & star ratings
  - Buy e-books with lifetime access
  - Download PDFs of purchased books
- **User & Librarian Profiles**:
  - View and update name/password

## 📁 API Endpoints

📄 [Full API Documentation](https://drive.google.com/file/d/1BGBnBGpESPbdg8QJFQggiI_ZFjlZGUpb/view?usp=sharing)

### 🔹 SectionAPI
- `GET /api/section` — List all sections  
- `POST /api/section` — Create a new section  
- `GET/PUT/DELETE /api/section/<int:id>` — Manage section by ID  

### 🔹 BookAPI
- `GET /api/book` — List all books  
- `POST /api/book` — Add a new book  
- `GET/PUT/DELETE /api/book/<int:id>` — Manage book by ID  

### 🔹 StatsAPI
- `GET /api/stats` — Fetch basic statistics

## 🙋‍♂️ Author

**Tanishk Agrawal**  
📧 [tanishk.agrawal1911@gmail.com](mailto:tanishk.agrawal1911@gmail.com)
