# 🌐 OpenSource Job Portal  

A full-stack **Django-based job portal** that connects **recruiters** and **job seekers**.  
Recruiters can post jobs, manage company profiles, and track applications, while job seekers can create profiles, upload resumes, and apply for jobs.

---

## 🚀 Features  

### 👨‍💼 Recruiters
- Register as a recruiter
- Create and edit recruiter/company profile
- Post job openings (with salary, skills, requirements, qualifications, etc.)
- View applicants for jobs

### 👩‍💻 Job Seekers
- Register as a job seeker
- Upload resumes and list skills
- Browse available jobs
- Apply directly to jobs with cover letter + resume
- View job application history

### 🔑 Authentication & Accounts
- Custom user model with **is_recruiter** flag
- User registration & login/logout
- Password reset with email verification
- Profile editing for both recruiters & job seekers

### 📬 Notifications
- Email sent to users upon registration
- Admin gets notified of new signups
- Success/error messages with Django messages framework

---

## 🛠️ Tech Stack

- **Backend**: Django (Python)  
- **Frontend**: HTML, CSS, Django Templates  
- **Database**: SQLite (default, can be switched to PostgreSQL/MySQL)  
- **Authentication**: Django Auth + Custom User model  
- **Email Service**: Django `send_mail`  

---


## ⚙️ Installation & Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/YourUsername/opensource_jobportal.git
   cd opensource_jobportal
2. **Create a virtual environment :** 
  python -m venv env
  source env/bin/activate   # Linux/Mac
  env\Scripts\activate      # Windows

3. **Install Dependencies:**
   pip install -r requirements.txt

4. **Apply migrations:**
   python manage.py migrate

5. **Create superuser:**
   python manage.py createsuperuser

6. **Run the development server:**
   python manage.py runserver

7. **Open browser and visit:** http://127.0.0.1:8000/
---



