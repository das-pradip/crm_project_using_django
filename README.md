# 🚀 CRM Management System 

A **role-based CRM (Customer Relationship Management) system** built using **Django**, designed to handle real-world business workflows such as **lead tracking, conversion, user roles, and analytics**.

This project was developed to demonstrate **production-level Django skills**, **clean architecture**, and **scalable design principles**.

---

## 🎯 Why This Project? 

This CRM solves common business problems:

* Managing leads across teams
* Preventing data duplication
* Enforcing role-based access
* Tracking conversions and performance metrics

It reflects **how enterprise CRMs work**, not just CRUD operations.

---

## 🧠 Core Concepts Demonstrated

✔ Django Authentication & Authorization
✔ Role-Based Access Control (RBAC)
✔ Business Logic Enforcement
✔ Secure Media Handling
✔ Analytics & Reporting
✔ Environment-based Configuration
✔ Clean MVC Architecture

---

## 🔑 Key Features

### 👥 Role-Based User Management

* Roles: **Admin, Manager, Sales**
* Permissions enforced at **view level**
* Admin cannot demote themselves (edge case handled)
* Sales users can access only assigned leads

---

### 📋 Lead Lifecycle Management

* Lead creation, update, delete
* Status pipeline:

  * New → Contacted → Qualified → Converted / Lost
* Converted leads are **locked from modification**
* Business rules enforced at model & view level

---

### 🔄 Lead to Customer Conversion

* One-click conversion for qualified leads
* Prevents duplicate customer creation
* Automatically updates lead status
* Conversion audit consistency maintained

---

### 📊 Analytics Dashboard

* Status-wise lead counts
* Conversion rate (%)
* Visual charts (Pie & Bar)
* Restricted to Admin & Manager roles

---

### 🧩 Kanban-Style Pipeline

* Visual representation of lead status
* Business-friendly UI
* Improves usability and tracking

---

### 🖼️ User Profile & Security

* Profile image upload with default fallback
* Change password functionality
* Secure media configuration
* CSRF & authentication protection

---

## 🛠️ Tech Stack

| Layer           | Technology           |
| --------------- | -------------------- |
| Backend         | Python, Django       |
| Database        | SQLite3 (Dev)        |
| Frontend        | HTML, CSS, Bootstrap |
| Charts          | Chart.js             |
| Forms           | Django Crispy Forms  |
| Auth            | Django Auth System   |
| Version Control | Git & GitHub         |

---

## 🧱 Architecture Overview

```
Client (Browser)
   ↓
Django Views (RBAC enforced)
   ↓
Business Logic Layer
   ↓
Django ORM (Models)
   ↓
SQLite Database
```

---

## 📁 Project Structure

```
crm/
│── crm/                # Settings & configuration
│── webapp/             # Core application logic
│   ├── models.py       # Lead, Customer, Profile
│   ├── views.py        # Business logic
│   ├── urls.py
│   ├── templates/
│   ├── static/
│── media/              # Profile images
│── .env                # Environment variables
│── .gitignore
│── manage.py
```

---

## 🔐 Security & Best Practices

* Environment variables for secrets
* CSRF protection
* Login required decorators
* Media isolation (`MEDIA_ROOT`)
* Debug disabled in production
* Modular app structure

---

## ⚙️ Setup Instructions

```bash
git clone https://github.com/your-username/crm-django.git
cd crm
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

---

## 🧪 Edge Cases Handled (Interview Gold)

✔ Admin cannot remove own privileges
✔ Converted leads cannot be edited
✔ Duplicate customer prevention
✔ Profile image fallback handling
✔ Unauthorized role access blocked

---

## 📈 Future Improvements

* PostgreSQL support
* Django REST Framework API
* Email notifications
* Role-based dashboards
* Dockerization
* Production deployment (Render/AWS)

---



## 👨‍💻 Author

**Pradip Das**
Full Stack Developer
📍 West Bengal, India

---

⭐ **This project was built with real business logic in mind, not just CRUD.**

---




