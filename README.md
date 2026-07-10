# 📚 Library Management System

A responsive **Library Management System** built using **Flask**, **SQLite**, **HTML**, **CSS**, **Bootstrap**, and **JavaScript**. The application provides an easy way to manage books, issue and return books, and monitor library statistics through a clean and user-friendly interface.

---

## 🚀 Features

- 📖 Add new books
- ✏️ Edit book details
- 🗑️ Delete books
- 🔍 Search books by title or author
- 👨‍🎓 Issue books with Student Name and Roll Number
- 🔄 Return issued books
- 📅 Automatic Issue Date & Return Date generation
- 📊 Dashboard showing:
  - Total Books
  - Available Books
  - Issued Books
- 📋 View all issued books
- ⚠️ User-friendly alerts for invalid operations
- 🎨 Responsive Bootstrap UI with hover animations
- ⭐ Font Awesome icons for a modern interface

---

## 🛠️ Tech Stack

### Frontend
- HTML5
- CSS3
- Bootstrap 5
- JavaScript
- Font Awesome

### Backend
- Python
- Flask

### Database
- SQLite

### Version Control
- Git
- GitHub

---

## 📂 Project Structure

```
Library-Management-System/
│
├── app.py
├── database.py
├── library.db
│
├── templates/
│   ├── index.html
│   ├── add_book.html
│   ├── edit_book.html
│   ├── issue_book.html
│   └── issued_books.html
│
├── static/
│   └── style.css
│
└── README.md
```

---

## ⚙️ Installation

### Clone the repository

```bash
git clone https://github.com/your-username/Library-Management-System.git
```

### Move into the project folder

```bash
cd Library-Management-System
```

### Install Flask

```bash
pip install flask
```

### Create the database

```bash
python3 database.py
```

### Run the application

```bash
python3 app.py
```

Open your browser and visit:

```
http://127.0.0.1:5000
```

---
