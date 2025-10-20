from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "your_secret_key"
db = SQLAlchemy(app)

# ------------------ Models ------------------
class JobSeeker(db.Model):
    __tablename__ = 'job_seeker'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(15))
    resume = db.relationship("Resume", backref="jobseeker", uselist=False, cascade="all, delete-orphan")
    skills = db.relationship("JobSeekerSkill", backref="jobseeker", lazy=True, cascade="all, delete-orphan")
    applications = db.relationship("Application", backref="jobseeker", lazy=True, cascade="all, delete-orphan")

class Employer(db.Model):
    __tablename__ = 'employer'
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    jobs = db.relationship("Job", backref="employer", lazy=True, cascade="all, delete-orphan")

class Job(db.Model):
    __tablename__ = 'job'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    posted_date = db.Column(db.DateTime, default=datetime.utcnow)
    salary = db.Column(db.Float)
    employer_id = db.Column(db.Integer, db.ForeignKey("employer.id"), nullable=False)
    applications = db.relationship("Application", backref="job", lazy=True, cascade="all, delete-orphan")

class Application(db.Model):
    __tablename__ = 'application'
    id = db.Column(db.Integer, primary_key=True)
    application_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(50), default="Pending")
    seeker_id = db.Column(db.Integer, db.ForeignKey("job_seeker.id"), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey("job.id"), nullable=False)

class Resume(db.Model):
    __tablename__ = 'resume'
    id = db.Column(db.Integer, primary_key=True)
    file_url = db.Column(db.String(200))
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
    seeker_id = db.Column(db.Integer, db.ForeignKey("job_seeker.id"), unique=True, nullable=False)

class Skill(db.Model):
    __tablename__ = 'skill'
    id = db.Column(db.Integer, primary_key=True)
    skill_name = db.Column(db.String(100), nullable=False, unique=True)
    seekers = db.relationship("JobSeekerSkill", backref="skill", lazy=True, cascade="all, delete-orphan")

class JobSeekerSkill(db.Model):
    __tablename__ = 'job_seeker_skill'
    seeker_id = db.Column(db.Integer, db.ForeignKey("job_seeker.id"), primary_key=True)
    skill_id = db.Column(db.Integer, db.ForeignKey("skill.id"), primary_key=True)

with app.app_context():
    db.create_all()

# ------------------ Routes ------------------
@app.route("/")
def index():
    stats = {
        'jobseekers': JobSeeker.query.count(),
        'employers': Employer.query.count(),
        'jobs': Job.query.count(),
        'applications': Application.query.count()
    }
    return render_template("index.html", stats=stats)

# ------------------ JobSeeker Routes ------------------
@app.route("/jobseekers")
def jobseeker_list():
    jobseekers = JobSeeker.query.all()
    return render_template("jobseeker_list.html", jobseekers=jobseekers)

@app.route("/jobseeker/add", methods=["GET", "POST"])
def add_jobseeker():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        phone = request.form["phone"]
        
        new_seeker = JobSeeker(name=name, email=email, password=password, phone=phone)
        db.session.add(new_seeker)
        db.session.commit()
        return redirect(url_for("jobseeker_list"))
    
    return render_template("jobseeker_form.html", jobseeker=None)

@app.route("/jobseeker/edit/<int:id>", methods=["GET", "POST"])
def edit_jobseeker(id):
    jobseeker = JobSeeker.query.get_or_404(id)
    
    if request.method == "POST":
        jobseeker.name = request.form["name"]
        jobseeker.email = request.form["email"]
        jobseeker.password = request.form["password"]
        jobseeker.phone = request.form["phone"]
        
        db.session.commit()
        return redirect(url_for("jobseeker_list"))
    
    return render_template("jobseeker_form.html", jobseeker=jobseeker)

@app.route("/jobseeker/delete/<int:id>")
def delete_jobseeker(id):
    jobseeker = JobSeeker.query.get_or_404(id)
    db.session.delete(jobseeker)
    db.session.commit()
    return redirect(url_for("jobseeker_list"))

# ------------------ Employer Routes ------------------
@app.route("/employers")
def employer_list():
    employers = Employer.query.all()
    return render_template("employer_list.html", employers=employers)

@app.route("/employer/add", methods=["GET", "POST"])
def add_employer():
    if request.method == "POST":
        company_name = request.form["company_name"]
        email = request.form["email"]
        password = request.form["password"]
        
        new_employer = Employer(company_name=company_name, email=email, password=password)
        db.session.add(new_employer)
        db.session.commit()
        return redirect(url_for("employer_list"))
    
    return render_template("employer_form.html", employer=None)

@app.route("/employer/edit/<int:id>", methods=["GET", "POST"])
def edit_employer(id):
    employer = Employer.query.get_or_404(id)
    
    if request.method == "POST":
        employer.company_name = request.form["company_name"]
        employer.email = request.form["email"]
        employer.password = request.form["password"]
        
        db.session.commit()
        return redirect(url_for("employer_list"))
    
    return render_template("employer_form.html", employer=employer)

@app.route("/employer/delete/<int:id>")
def delete_employer(id):
    employer = Employer.query.get_or_404(id)
    db.session.delete(employer)
    db.session.commit()
    return redirect(url_for("employer_list"))

# ------------------ Job Routes ------------------
@app.route("/jobs")
def job_list():
    jobs = Job.query.all()
    return render_template("job_list.html", jobs=jobs)

@app.route("/job/add", methods=["GET", "POST"])
def add_job():
    employers = Employer.query.all()
    
    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        salary = request.form["salary"]
        employer_id = request.form["employer_id"]
        
        new_job = Job(title=title, description=description, salary=salary, employer_id=employer_id)
        db.session.add(new_job)
        db.session.commit()
        return redirect(url_for("job_list"))
    
    return render_template("job_form.html", job=None, employers=employers)

@app.route("/job/edit/<int:id>", methods=["GET", "POST"])
def edit_job(id):
    job = Job.query.get_or_404(id)
    employers = Employer.query.all()
    
    if request.method == "POST":
        job.title = request.form["title"]
        job.description = request.form["description"]
        job.salary = request.form["salary"]
        job.employer_id = request.form["employer_id"]
        
        db.session.commit()
        return redirect(url_for("job_list"))
    
    return render_template("job_form.html", job=job, employers=employers)

@app.route("/job/delete/<int:id>")
def delete_job(id):
    job = Job.query.get_or_404(id)
    db.session.delete(job)
    db.session.commit()
    return redirect(url_for("job_list"))

# ------------------ Application Routes ------------------
@app.route("/applications")
def application_list():
    applications = Application.query.all()
    return render_template("application_list.html", applications=applications)

@app.route("/application/add", methods=["GET", "POST"])
def add_application():
    jobseekers = JobSeeker.query.all()
    jobs = Job.query.all()
    
    if request.method == "POST":
        seeker_id = request.form["seeker_id"]
        job_id = request.form["job_id"]
        status = request.form["status"]
        
        new_application = Application(seeker_id=seeker_id, job_id=job_id, status=status)
        db.session.add(new_application)
        db.session.commit()
        return redirect(url_for("application_list"))
    
    return render_template("application_form.html", application=None, jobseekers=jobseekers, jobs=jobs)

@app.route("/application/edit/<int:id>", methods=["GET", "POST"])
def edit_application(id):
    application = Application.query.get_or_404(id)
    jobseekers = JobSeeker.query.all()
    jobs = Job.query.all()
    
    if request.method == "POST":
        application.seeker_id = request.form["seeker_id"]
        application.job_id = request.form["job_id"]
        application.status = request.form["status"]
        
        db.session.commit()
        return redirect(url_for("application_list"))
    
    return render_template("application_form.html", application=application, jobseekers=jobseekers, jobs=jobs)

@app.route("/application/delete/<int:id>")
def delete_application(id):
    application = Application.query.get_or_404(id)
    db.session.delete(application)
    db.session.commit()
    return redirect(url_for("application_list"))

# ------------------ Skill Routes ------------------
@app.route("/skills")
def skill_list():
    skills = Skill.query.all()
    return render_template("skill_list.html", skills=skills)

@app.route("/skill/add", methods=["GET", "POST"])
def add_skill():
    if request.method == "POST":
        skill_name = request.form["skill_name"]
        
        new_skill = Skill(skill_name=skill_name)
        db.session.add(new_skill)
        db.session.commit()
        return redirect(url_for("skill_list"))
    
    return render_template("skill_form.html", skill=None)

@app.route("/skill/edit/<int:id>", methods=["GET", "POST"])
def edit_skill(id):
    skill = Skill.query.get_or_404(id)
    
    if request.method == "POST":
        skill.skill_name = request.form["skill_name"]
        db.session.commit()
        return redirect(url_for("skill_list"))
    
    return render_template("skill_form.html", skill=skill)

@app.route("/skill/delete/<int:id>")
def delete_skill(id):
    skill = Skill.query.get_or_404(id)
    db.session.delete(skill)
    db.session.commit()
    return redirect(url_for("skill_list"))

# ------------------ Initialize DB ------------------
with app.app_context():
    db.create_all()
    
    # Add sample data if no skills exist
    if Skill.query.count() == 0:
        sample_skills = ['Python', 'Java', 'JavaScript', 'SQL', 'HTML/CSS', 'React', 'Node.js', 'Flask', 'Django']
        for skill_name in sample_skills:
            db.session.add(Skill(skill_name=skill_name))
        db.session.commit()

if __name__ == "__main__":
    app.run(debug=True)