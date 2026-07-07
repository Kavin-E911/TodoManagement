# 📝 Todo Management System

A full-stack **Todo Management System** developed using **Python Flask**, **SQLite**, **HTML**, **CSS**, and **JavaScript**. The application enables users to securely manage their personal todo lists and tasks with authentication, task organization, and sharing features.

---

## 🚀 Features

### 👤 User Authentication
- User Signup
- User Login
- User Logout
- Session-based Authentication

### 📂 Todo List Management
- Create Multiple Todo Lists
- Rename Todo Lists
- Delete Todo Lists
- Each User Can Access Only Their Own Todo Lists

### ✅ Todo Item Management
- Add Todo Items
- Edit Todo Items
- Delete Todo Items
- Mark Tasks as Completed / Pending
- Assign Tags to Tasks
- Filter Tasks by Tags

### 📊 Statistics
- Total Todo Lists
- Completed Tasks
- Pending Tasks
- Task Progress

### 🔗 Public Sharing
- Generate Unique Share Link
- View Shared Todo Lists Without Login

### 🎨 User Interface
- Professional Dark Theme
- Responsive Layout
- Clean Dashboard
- Interactive User Experience

---

## 🛠️ Technologies Used

### Backend
- Python
- Flask
- SQLite

### Frontend
- HTML5
- CSS3
- JavaScript

### Database
- SQLite

---

## 📁 Project Structure

```
TodoManagement
│
├── backend
│   ├── app.py
│   ├── requirements.txt
│   ├── static
│   │   ├── style.css
│   │   └── script.js
│   │
│   └── templates
│       ├── login.html
│       ├── signup.html
│       ├── dashboard.html
│       └── todo.html
│
└── README.md
```

---

## ⚙️ Installation

### Clone Repository

```bash
git clone https://github.com/Kavin-E911/TodoManagement.git
```

### Navigate to Project

```bash
cd TodoManagement/backend
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Virtual Environment

#### Windows

```bash
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run Application

```bash
python app.py
```

---

## 🌐 Open in Browser

```
http://127.0.0.1:5000
```

---

## 📷 Application Workflow

1. Create an Account
2. Login
3. Create Todo Lists
4. Add Tasks
5. Edit or Delete Tasks
6. Mark Tasks as Completed
7. Filter Tasks by Tags
8. Share Todo Lists
9. Logout

---

## 🔒 Security

- Session-based User Authentication
- Personal Todo Lists for Each User
- Users Cannot Access Other Users' Todo Lists
- Protected Routes Using Flask Sessions

---

## 📌 Future Enhancements

- Password Encryption (bcrypt)
- Email Reminder Notifications
- Drag-and-Drop Task Reordering
- Mobile Application
- Due Dates and Calendar View
- Search Functionality
- User Profile Management

---

## 👨‍💻 Developer

**Kavin E**

Computer Science and Engineering Student

KPR Institute of Engineering and Technology

GitHub: https://github.com/Kavin-E911

---

## 📜 License

This project was developed for learning purposes and academic evaluation.
