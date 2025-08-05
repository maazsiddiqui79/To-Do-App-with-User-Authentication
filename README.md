
---
# 🔐 To‑Do App with User Authentication & Multi-Table Task Lists

[![Python](https://img.shields.io/badge/Python-3.10-blue.svg)](https://www.python.org/) [![Flask](https://img.shields.io/badge/Flask-Web%20Framework-000000.svg)](https://flask.palletsprojects.com/) [![SQLite](https://img.shields.io/badge/Database-SQLite-003B57.svg)](https://www.sqlite.org/index.html) [![Render](https://img.shields.io/badge/Hosted%20on-Render-blueviolet.svg)](https://render.com/) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A secure, user-specific To‑Do List web application built with Flask and SQLite. This application allows users to register, log in, and manage personal task lists — now with the ability to create, rename, and delete **multiple task tables**.

---

# 🚀 Live Demo

📍 **Live Now on Vercel**
🔗 [https://go-todo-task.com](https://go-todo-task.onrender.com/)

---

# 📚 Project Overview

This is the **advanced version** of my [Go‑Todo Task](https://github.com/maazsiddiqui79/To-Do-List-Web-Application) project, now enhanced and **fully deployed** with:

* User authentication (register/login/logout)
* Secure session handling and password hashing
* Private task lists per user
* **Create, rename, and delete multiple task tables**
* Task priority functionality
* Persistent data storage with SQLite
* Intuitive, mobile-first design

---

# 🔁 Related Project

➡️ **Looking for the basic version?**
Check out the simplified app without login:
🔗 [Go‑Todo Task](https://github.com/maazsiddiqui79/To-Do-List-Web-Application)

---

# 📁 Project Structure

```
To-Do-List-With-Auth/
├── static/
│   ├── style.css
│   └── screenshots/
│       ├── register.png
│       └── dashboard.png
│
├── templates/
│   ├── base.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   └── index.html
│
├── app.py
├── auth.py
├── tasks.py
├── requirements.txt
├── Dockerfile
├── .env
└── README.md
```

---

# 🔐 Core Features

| Feature             | Description                                                |
| ------------------- | ---------------------------------------------------------- |
| **User Accounts**   | Register, login, and logout functionality                  |
| **Security**        | Passwords securely hashed using Werkzeug                   |
| **Session Mgmt.**   | Persistent user sessions with protected routes             |
| **Private Tasks**   | Each user has a personalized to-do list                    |
| **Task Priority**   | Set and filter tasks based on priority levels              |
| **Multiple Tables** | Users can create, rename, and delete their own task tables |
| **Database**        | SQLite-based persistent storage                            |
| **Clean UI**        | Responsive layout using HTML5, CSS3, Bootstrap & Jinja2    |

---

# 🧰 Tech Stack

| Tool             | Purpose                         |
| ---------------- | ------------------------------- |
| **Python 3.10+** | Core language                   |
| **Flask**        | Web framework                   |
| **SQLite**       | Lightweight embedded database   |
| **Werkzeug**     | Secure password hashing         |
| **Jinja2**       | HTML templating engine          |
| **Bootstrap 4**  | Mobile-first responsive design  |
| **Git & GitHub** | Version control & collaboration |

---

# 🛠️ Local Setup

To run the project locally:

1. **Clone the repo**

   ```bash
   git clone https://github.com/maazsiddiqui79/To-Do-List-With-Auth.git
   cd To-Do-List-With-Auth
   ```

2. **Set up virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # For Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**

   ```bash
   flask run
   ```

5. Open in browser at: `http://127.0.0.1:5000`

---

# 📈 Planned Enhancements

| Feature                        | Status |
| ------------------------------ | ------ |
| Add, update, delete tasks      | ✅      |
| Mark tasks as complete         | ✅      |
| Task priority levels           | ✅      |
| Secure user authentication     | ✅      |
| Private task views per user    | ✅      |
| Secure session handling        | ✅      |
| Create multiple task tables    | ✅      |
| Rename and delete task tables  | ✅      |
| Intuitive, mobile-first design | ✅      |
| Host on Render or Vercel       | ✅      |
| Password reset functionality   | 🔜     |
| Task categories & tags         | 🔜     |
| Dark mode toggle               | 🔜     |
| UI/UX enhancements             | 🔜     |
| Admin dashboard (future scope) | 🔜     |

---

# 🧑‍💻 Author

**Maaz Siddiqui**
🎓 Diploma in Computer Engineering
🔗 GitHub: [maazsiddiqui79](https://github.com/maazsiddiqui79)
💻 Passionate about backend systems and clean UI design

---

Let me know if you'd like this written in a format suited for a GitHub project page (with markdown badges, collapsible sections, etc.), or want screenshots / GIFs added.
