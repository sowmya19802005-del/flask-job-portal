# Online Job Portal - Database Management System

## 🚀 Features
- **Complete CRUD Operations** for all entities
- **User Management** - Job Seekers and Employers  
- **Job Posting System** - Create, edit, and manage job listings
- **Application Tracking** - Track job applications with status updates
- **Skills Management** - Manage and assign skills to job seekers
- **Responsive Design** - Professional UI that works on all devices
- **Database Relationships** - Properly implemented 1:1, 1:N, and M:N relationships

## 🛠️ Tech Stack
- **Backend**: Flask, SQLAlchemy
- **Database**: SQLite  
- **Frontend**: HTML5, CSS3, JavaScript
- **Styling**: Custom CSS with modern design
- **ORM**: Flask-SQLAlchemy

## 📋 Entity Relationships
- **JobSeeker** ↔ **Application** (1:N)
- **Job** ↔ **Application** (1:N) 
- **Employer** ↔ **Job** (1:N)
- **JobSeeker** ↔ **Resume** (1:1)
- **JobSeeker** ↔ **Skill** (M:N)

## 🗂️ Project Structure
```
online_job_portal/
├── app.py                 # Main Flask application
├── database.db           # SQLite database (auto-generated)
├── requirements.txt      # Python dependencies
├── static/
│   └── style.css        # Professional styling
└── templates/           # All HTML templates
    ├── base.html        # Base template
    ├── index.html       # Dashboard
    ├── jobseeker_list.html
    ├── jobseeker_form.html
    ├── employer_list.html
    ├── employer_form.html
    ├── job_list.html
    ├── job_form.html
    ├── application_list.html
    ├── application_form.html
    ├── skill_list.html
    └── skill_form.html
```

## 🚀 Quick Start

### Installation & Setup
1. **Create project folder**
   ```bash
   mkdir online_job_portal
   cd online_job_portal
   ```

2. **Create folder structure**
   ```bash
   mkdir templates static
   ```

3. **Install dependencies**
   ```bash
   pip install flask flask-sqlalchemy
   ```

4. **Copy all provided files** to their respective folders

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Access the application**
   ```
   http://127.0.0.1:5000
   ```

## 📊 Database Tables
- `job_seeker` - Job seeker information
- `employer` - Employer/company details  
- `job` - Job postings
- `application` - Job applications
- `resume` - Resume files (1:1 with job_seeker)
- `skill` - Available skills
- `job_seeker_skill` - M:N relationship table

## 🎯 Usage
1. **Start by adding** Job Seekers and Employers
2. **Post Jobs** from employer accounts  
3. **Create Applications** linking job seekers to jobs
4. **Manage Skills** and assign to job seekers
5. **Track Application Status** (Pending/Reviewed/Accepted/Rejected)

## 👥 Team
- **Abhishek Ashok Rodagi** (23BCE0795)
- **Mohith V** (23BCT0181)

- **Slot**: L43 + L44
- **Venue**: SJT515

---

*Built as a case study for Database Systems course demonstrating complete CRUD operations and database relationships.*
