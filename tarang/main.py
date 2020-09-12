from flask import Flask, render_template, request, escape, redirect, url_for, session, flash
from passlib.hash import sha256_crypt
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os
from random import randint
import zipfile


app = Flask(__name__)
app.secret_key = "Tarang_is_secret_key"

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:vishu@127.0.0.1:3306/tarang"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Admin(db.Model):
    __tablename__= 'admin'
    id = db.Column(db.Integer, 
        primary_key=True)
    name = db.Column(db.String(64), 
        index=False, 
        nullable=False)
    email = db.Column(db.String(80),
        index=True, 
        unique=True, 
        nullable=False)
    password = db.Column(db.String(128), 
        nullable=False)
    phone = db.Column(db.Integer(),
        nullable=False)
    remember_token = db.Column(db.String(128), 
        nullable=True)
    updated_at = db.Column(db.DateTime, 
        default=datetime.now)
    created_at = db.Column(db.DateTime,
        default=datetime.now)

    def __init__(self, name, email, password, phone, remember_token=None):
        self.name = name
        self.email = email
        self.password = password
        self.phone = phone

    def __repr__(self):
        return '<Admin %r>' % self.email


class Users(db.Model):
    __tablename__= 'users'
    id = db.Column(db.Integer, 
        primary_key=True)
    name = db.Column(db.String(64), 
        index=False, 
        nullable=False)
    email = db.Column(db.String(80),
        index=True, 
        unique=True, 
        nullable=False)
    password = db.Column(db.String(128), 
        nullable=False)
    phone = db.Column(db.Integer(),
        nullable=False)
    photo = db.Column(db.String(128), 
        nullable=True)
    year = db.Column(db.String(40),
        nullable=True)
    teachers = db.Column(db.String(128), 
        nullable=True)
    email_verified = db.Column(db.SmallInteger(),
        default=0)
    admin_verified = db.Column(db.SmallInteger(),
        default=0)
    google_provider_id = db.Column(db.String(128), 
        nullable=True)
    facebook_provider_id = db.Column(db.String(128), 
        nullable=True)
    batch_ids = db.Column(db.String(128), 
        nullable=True)
    remember_token = db.Column(db.String(128), 
        nullable=True)
    updated_at = db.Column(db.DateTime, 
        default=datetime.now)
    created_at = db.Column(db.DateTime,
        default=datetime.now)

    def __init__(self, name, email, password, phone, year=None, google_provider_id=None,
     facebook_provider_id=None, batch_ids=None, remember_token=None):
        self.name = name
        self.email = email
        self.password = password
        self.phone = phone
        if year:
            self.year=year
        if(google_provider_id):
            self.google_provider_id = google_provider_id
        if(facebook_provider_id):
            self.facebook_provider_id = facebook_provider_id
        if(batch_ids):
            self.batch_ids = batch_ids
        if(remember_token):
            self.remember_token = remember_token

    def __repr__(self):
        return '<Users %r>' % self.email


class Lecturers(db.Model):
    __tablename__= 'lecturers'
    id = db.Column(db.Integer, 
        primary_key=True)
    name = db.Column(db.String(64), 
        index=False, 
        nullable=False)
    email = db.Column(db.String(80),
        index=True, 
        unique=True, 
        nullable=False)
    password = db.Column(db.String(128), 
        nullable=False)
    phone = db.Column(db.Integer(),
        nullable=False)
    photo = db.Column(db.String(128), 
        nullable=True)
    designation = db.Column(db.String(128),
        nullable=True)
    education = db.Column(db.String(128),
        nullable=True)
    skills = db.Column(db.String(255),
        nullable=True)
    about = db.Column(db.String(1024),
        nullable=True)
    experience = db.Column(db.String(1024),
        nullable=True)
    achievements = db.Column(db.String(1024),
        nullable=True)
    students_request = db.Column(db.String(128),
        nullable=True)
    linkedin = db.Column(db.String(255),
        nullable=True)
    github = db.Column(db.String(255),
        nullable=True)
    youtube = db.Column(db.String(255),
        nullable=True)
    email_verified = db.Column(db.SmallInteger(),
        default=0)
    google_provider_id = db.Column(db.String(128), 
        nullable=True)
    facebook_provider_id = db.Column(db.String(128), 
        nullable=True)
    batch_ids = db.Column(db.String(128), 
        nullable=True)
    remember_token = db.Column(db.String(128), 
        nullable=True)
    updated_at = db.Column(db.DateTime, 
        default=datetime.now)
    created_at = db.Column(db.DateTime,
        default=datetime.now)

    def __init__(self, name, email, password, phone, designation, 
        education, google_provider_id=None, facebook_provider_id=None):
        self.name = name
        self.email = email
        self.password = password
        self.phone = phone
        self.designation = designation
        self.education = education
        if(google_provider_id):
            self.google_provider_id = google_provider_id
        if(facebook_provider_id):
            self.facebook_provider_id = facebook_provider_id

    def __repr__(self):
        return '<Lecturers %r>' % self.email



class Assignments(db.Model):
    __tablename__= 'assignments'
    id = db.Column(db.Integer, 
        primary_key=True)
    lecturer_id = db.Column(db.Integer,
        nullable=False)
    topic_name = db.Column(db.String(255), 
        index=False, 
        nullable=False)
    path = db.Column(db.String(128), 
        nullable=False)
    updated_at = db.Column(db.DateTime, 
        default=datetime.now)
    created_at = db.Column(db.DateTime,
        default=datetime.now)

    def __init__(self, lecturer_id, topic_name, path):
        self.lecturer_id = lecturer_id
        self.topic_name = topic_name
        self.path = path

    def __repr__(self):
        return '<Assignments %r>' % self.path




def create_user(req: 'flask_request') -> bool:
    try:
        name = str(req.form['name'])
        email = str(req.form['email'])
        password = str(sha256_crypt.hash(req.form['psw']))
        phone = int(req.form['phone'])
        year = str(req.form['year'])
        if year != "":
            user = Users(name,email,password,phone,year)
        else:
            user = Users(name,email,password,phone)
        db.session.add(user)
        db.session.commit()
        return True 

    except Exception:
        return False


def create_lecturer(req: 'flask_request') -> bool:
    try:
        name = str(req.form['name'])
        email = str(req.form['email'])
        password = str(sha256_crypt.hash(req.form['psw']))
        phone = int(req.form['phone'])
        designation = str(req.form['designation'])
        education = str(req.form['education'])
        lecturer = Lecturers(name,email,password,phone,designation,education)
        db.session.add(lecturer)
        db.session.commit()
        return True 
    except Exception:
        return False



@app.route('/update')
def update_user() -> bool:
    try:
        update = Users.query.filter_by(email="zxcv@gmail.com").first()
        update.name = "zxcv"
        db.session.commit()
        return 'True'
    except Exception:
        return 'False'


def login_credential_check(req: 'flask_request') -> bool:
    try:
        username = str(req.form['username'])
        password = str(req.form['pass'])
        user = Users.query.filter_by(email=username).first()
        if user.email == username and sha256_crypt.verify(password, user.password):
            session['tarang_username'] = user.email
            session['student_id'] = user.id
            return True
        else:
            return False
    except Exception:
        return False


def lecturer_login_credential_check(req: 'flask_request') -> bool:
    try:
        username = str(req.form['username'])
        password = str(req.form['pass'])
        lecturer = Lecturers.query.filter_by(email=username).first()
        if lecturer.email == username and sha256_crypt.verify(password, lecturer.password):
            session['lecturer_username'] = lecturer.email
            session['lecturer_id'] = lecturer.id
            return True
        else:
            return False
    except Exception as e:
        raise e


# student section

@app.route('/')
@app.route('/login')
def students_login() -> 'html':
    if 'tarang_username' in session:
        return redirect(url_for('dashboard'))
    return render_template('login.html', the_title='Students Login - Tarang')


@app.route('/login_success', methods = ['POST', 'GET'])
def login_success():
    if request.method == 'POST':
        user = login_credential_check(request)
        if user != False:
            return redirect(url_for('dashboard'))
        else:
            flash('Login credentials do not match')
            return redirect('/login')

    return redirect('/login')



@app.route('/signup')
def students_signup() -> 'html':
    return render_template('signup.html',
                           the_title='Students Sign Up - Tarang')


@app.route('/signup_success', methods = ['POST', 'GET'])
def signup_success():
    if request.method == 'POST':
        boolean = create_user(request)
        if boolean == True:
            flash('Successfully sign up, you can login now')
            return redirect('/login')
        else:
            flash('Error occurred ! Please try again')
            return redirect('/signup')


@app.route('/logout')
def logout():
    session.pop('tarang_username', None)
    session.pop('student_id', None)
    return redirect('login')
    


@app.route('/ForgotPassword')
def ForgotPassword() -> 'html':
    return render_template('ForgotPassword.html',
                           the_title='Forgot Password - Tarang')

@app.route('/dashboard')
def dashboard() -> 'html':
    if 'tarang_username' not in session:
        return redirect('/login')
    else:
        user = Users.query.filter_by(email=session['tarang_username']).first()
        return render_template('dashboard/index.html',
                           the_title='Students Dashboard - Tarang',
                           user=user)


@app.route('/notes')
def notes() -> 'html':
    if 'tarang_username' not in session:
        return redirect('/login')
    else:
        user = Users.query.filter_by(email=session['tarang_username']).first()
        lecturers = Lecturers.query.all()
        notes = Assignments.query.all()
        request_accepted = [int(i) for i in user.teachers.split(',')]
        return render_template('dashboard/notes.html',
                           the_title='Notes - Tarang',
                           user=user,
                           lecturers=lecturers,
                           notes=notes,
                           request_accepted=request_accepted)

@app.route('/notes/<id>')
def lecturer_notes(id) -> 'html':
    if 'tarang_username' not in session:
        return redirect('/login')
    else:
        user = Users.query.filter_by(email=session['tarang_username']).first()
        lecturers = Lecturers.query.all()
        notes = Assignments.query.filter_by(lecturer_id=id).all()
        request_accepted = [int(i) for i in user.teachers.split(',')]
        return render_template('dashboard/lecturer_notes.html',
                           the_title='Notes - Tarang',
                           user=user,
                           lecturers=lecturers,
                           notes=notes,
                           lecturer_id=int(id),
                           request_accepted=request_accepted)



@app.route('/note/<id>')
def note(id) -> 'html':
    if 'tarang_username' not in session:
        return redirect('/login')
    else:
        user = Users.query.filter_by(email=session['tarang_username']).first()
        assignment = Assignments.query.filter_by(id=id).first()
        lecturer = Lecturers.query.filter_by(id=assignment.lecturer_id).first()
        request_accepted = [int(i) for i in user.teachers.split(',')]
        return render_template('dashboard/note.html',
                           the_title='Note - Tarang',
                           user=user,
                           id=int(id),
                           assignment=assignment,
                           lecturer=lecturer,
                           request_accepted=request_accepted)



@app.route('/tests')
def tests() -> 'html':
    if 'tarang_username' not in session:
        return redirect('/login')
    else:
        user = Users.query.filter_by(email=session['tarang_username']).first()
        lecturers = Lecturers.query.all()
        tests = Assignments.query.all()
        request_accepted = [int(i) for i in user.teachers.split(',')]
        return render_template('dashboard/tests.html',
                           the_title='Tests - Tarang',
                           user=user,
                           lecturers=lecturers,
                           tests=tests,
                           request_accepted=request_accepted)



@app.route('/tests/<id>')
def lecturer_tests(id) -> 'html':
    if 'tarang_username' not in session:
        return redirect('/login')
    else:
        user = Users.query.filter_by(email=session['tarang_username']).first()
        lecturers = Lecturers.query.all()
        tests = Assignments.query.filter_by(lecturer_id=id).all()
        request_accepted = [int(i) for i in user.teachers.split(',')]
        return render_template('dashboard/lecturer_tests.html',
                           the_title='Notes - Tarang',
                           user=user,
                           lecturers=lecturers,
                           tests=tests,
                           lecturer_id=int(id),
                           request_accepted=request_accepted)



@app.route('/test/<id>')
def test(id) -> 'html':
    if 'tarang_username' not in session:
        return redirect('/login')
    else:
        user = Users.query.filter_by(email=session['tarang_username']).first()
        assignment = Assignments.query.filter_by(id=id).first()
        lecturer = Lecturers.query.filter_by(id=assignment.lecturer_id).first()
        request_accepted = [int(i) for i in user.teachers.split(',')]
        return render_template('dashboard/test.html',
                           the_title='Test - Tarang',
                           user=user,
                           id=int(id),
                           assignment=assignment,
                           lecturer=lecturer,
                           request_accepted=request_accepted)



@app.route('/lecturers')
def lecturers() -> 'html':
    if 'tarang_username' not in session:
        return redirect('/login')
    else:
        user = Users.query.filter_by(email=session['tarang_username']).first()
        lecturers = Lecturers.query.all()
        request_accepted = [int(i) for i in user.teachers.split(',')]
        request_sent = []
        for lecturer in lecturers:
            if lecturer.students_request != None and user.id in [int(i) for i in lecturer.students_request.split(',')]:
                request_sent.append(lecturer.id)

        return render_template('dashboard/teachers.html',
                           the_title='Lecturers - Tarang',
                           user=user,
                           lecturers=lecturers,
                           request_accepted=request_accepted,
                           request_sent=request_sent)


@app.route('/lecturer_info/<id>')
def lecturer_info(id) -> 'html':
    if 'tarang_username' not in session:
        return redirect('/login')
    else:
        user = Users.query.filter_by(email=session['tarang_username']).first()
        lecturers = Lecturers.query.all()
        request_accepted = [int(i) for i in user.teachers.split(',')]
        request_sent = []
        for lect in lecturers:
            if lect.students_request != None and user.id in [int(i) for i in lect.students_request.split(',')]:
                request_sent.append(lect.id)

        lecturer = Lecturers.query.filter_by(id=id).first()        
        return render_template('dashboard/teacher_info.html',
                           the_title='Lecturer - Tarang',
                           user=user,
                           lecturers=lecturers,
                           lecturer=lecturer,
                           request_accepted=request_accepted,
                           request_sent=request_sent)


@app.route('/send_request/<id>')
def send_request(id) -> 'html':
    if 'tarang_username' not in session:
        return redirect('/login')
    else:
        lecturer = Lecturers.query.filter_by(id=id).first()
        if lecturer.students_request != None:
            students_request = [int(i) for i in lecturer.students_request.split(',')]
            students_request.append(session['student_id'])
            students_request = ','.join(str(i) for i in students_request)
            lecturer.students_request = students_request
            db.session.commit()
        else:
            lecturer.students_request = str(session['student_id'])
            db.session.commit()

        return redirect('/lecturers')


@app.route('/cancel_request/<id>')
def cancel_request(id) -> 'html':
    if 'tarang_username' not in session:
        return redirect('/login')
    else:
        lecturer = Lecturers.query.filter_by(id=id).first()

        students_request = [int(i) for i in lecturer.students_request.split(',')]
        students_request.remove(session['student_id'])
        if students_request != []:
            students_request = ','.join(str(i) for i in students_request)
            lecturer.students_request = students_request
            db.session.commit()
        else:
            lecturer.students_request = None
            db.session.commit()

        return redirect('/lecturers')



@app.route('/results')
def results() -> 'html':
    if 'tarang_username' not in session:
        return redirect('/login')
    else:
        user = Users.query.filter_by(email=session['tarang_username']).first()
        return render_template('dashboard/results.html',
                           the_title='Test Results - Tarang',
                           user=user)



# Lecturer section
@app.route('/lecturer')
@app.route('/lecturer/login')
def lecturer_login() -> 'html':
    if 'lecturer_username' in session:
        return redirect(url_for('lecturer_dashboard'))
    return render_template('lecturer_login.html', the_title='Lecturers Login - Tarang')


@app.route('/lecturer_login_success', methods = ['POST', 'GET'])
def lecturer_login_success():
    if request.method == 'POST':
        lecturer = lecturer_login_credential_check(request)
        if lecturer == True:
            return redirect(url_for('lecturer_dashboard'))
        else:
            flash('Login credentials do not match')
            return redirect('/lecturer/login')

    return redirect('/lecturer/login')



@app.route('/lecturer/signup')
def lecturer_signup() -> 'html':
    return render_template('lecturer_signup.html',
                           the_title='Lecturers Sign Up - Tarang')


@app.route('/lecturer/signup_success', methods = ['POST', 'GET'])
def lecturer_signup_success():
    if request.method == 'POST':
        boolean = create_lecturer(request)
        if boolean == True:
            flash('Successfully sign up, you can login now')
            return redirect('/lecturer/login')
        else:
            flash('Error occurred ! Please try again')
            return redirect('/lecturer/signup')


@app.route('/lecturer/logout')
def lecturer_logout():
    session.pop('lecturer_username', None)
    session.pop('lecturer_id', None)
    return redirect('/lecturer/login')
    


@app.route('/lecturer/ForgotPassword')
def LecturerForgotPassword() -> 'html':
    return render_template('LecturerForgotPassword.html',
                           the_title='Forgot Password - Tarang')


@app.route('/lecturer/dashboard')
def lecturer_dashboard() -> 'html':
    if 'lecturer_username' not in session:
        return redirect('/lecturer/login')
    else:
        lecturer = Lecturers.query.filter_by(email=session['lecturer_username']).first()
        return render_template('dashboard/lecturer_index.html',
                           the_title='Lecturer Dashboard - Tarang',
                           lecturer=lecturer)



@app.route('/lecturer/edit_dashboard')
def lecturer_edit_dashboard() -> 'html':
    if 'lecturer_username' not in session:
        return redirect('/lecturer/login')
    else:
        lecturer = Lecturers.query.filter_by(email=session['lecturer_username']).first()
        return render_template('dashboard/lecturer_edit_dashboard.html',
                           the_title='Edit - Tarang',
                           lecturer=lecturer)


@app.route('/lecturer/edit_dashboard_success', methods = ['GET','POST'])
def lecturer_edit_dashboard_success() -> 'html':
    if 'lecturer_username' not in session:
        return redirect('/lecturer/login')
    elif request.method == 'POST':
        try:
            lecturer = Lecturers.query.filter_by(email=session['lecturer_username']).first()
            lecturer.name = request.form['name']
            lecturer.phone = request.form['phone']
            lecturer.designation = request.form['designation']
            lecturer.education = request.form['education']
            if request.form['skills'] != None:
                lecturer.skills = request.form['skills']
            if request.form['about'] != None: 
                lecturer.about = request.form['about']
            if request.form['experience'] != None:
                lecturer.experience = request.form['experience']
            if request.form['achievements'] != None:
                lecturer.achievements = request.form['achievements']
            if request.form['linkedin'] != None:
                lecturer.linkedin = request.form['linkedin']
            if request.form['github'] != None:
                lecturer.github = request.form['github']
            if request.form['youtube'] != None:
                lecturer.youtube = request.form['youtube']
            db.session.commit()
            return redirect('/lecturer/dashboard')
        except Exception:
            raise redirect('/lecturer/dashboard')



@app.route('/lecturer/assignments')
def lecturer_assignments() -> 'html':
    if 'lecturer_username' not in session:
        return redirect('/lecturer/login')
    else:
        lecturer = Lecturers.query.filter_by(email=session['lecturer_username']).first()
        assignments = Assignments.query.filter_by(lecturer_id=lecturer.id).all()
        return render_template('dashboard/lecturer_assignments.html',
                           the_title='Lecturer Assignments - Tarang',
                           lecturer=lecturer,
                           assignments=assignments)



@app.route('/lecturer/create_assignment')
def lecturer_create_assignment() -> 'html':
    if 'lecturer_username' not in session:
        return redirect('/lecturer/login')
    else:
        lecturer = Lecturers.query.filter_by(email=session['lecturer_username']).first()
        return render_template('dashboard/create_assignment.html',
                           the_title='Create Assignments - Tarang',
                           lecturer=lecturer)


@app.route('/lecturer/create_assignment_success', methods = ['POST', 'GET'])
def lecturer_create_assignment_success() -> 'html':
    if 'lecturer_username' not in session:
        return redirect('/lecturer/login')
    elif request.method == 'POST':
        try:
            directory = str(randint(1000000000, 9999999999))
            parent_dir = "./static/uploads"
            path = os.path.join(parent_dir, directory)
            os.mkdir(path, 0o777)
            app.config['UPLOAD_FOLDER'] = path
            file = request.files['zip_file']
            file_name = secure_filename(file.filename)
            filename = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
            file.save(filename)
            with zipfile.ZipFile(filename, 'r') as zip_ref:
                zip_ref.extractall(path)

            lecturer_id = request.form['lecturer_id']
            topic_name = str(request.form['topic_name'])
            path = "uploads/" + directory + "/" + file_name.split('.')[0]
            assignment = Assignments(lecturer_id,topic_name,path)
            db.session.add(assignment)
            db.session.commit()
            flash('Successfully created a assignment')
            return redirect('/lecturer/assignments')
        except Exception:
            flash('Error occurred ! Please try again')
            return redirect('/lecturer/create_assignment')
    else:
        flash('Error occurred ! Please try again')
        return redirect('/lecturer/create_assignment')


@app.route('/lecturer/edit_assignment/<id>')
def lecturer_edit_assignment(id) -> 'html':
    if 'lecturer_username' not in session:
        return redirect('/lecturer/login')
    else:
        assignment = Assignments.query.filter_by(id=id).first()
        return render_template('dashboard/edit_assignment.html',
                           the_title='Create Assignments - Tarang',
                           assignment=assignment)



@app.route('/lecturer/edit_assignment_success', methods = ['POST', 'GET'])
def lecturer_edit_assignment_success() -> 'html':
    if 'lecturer_username' not in session:
        return redirect('/lecturer/login')
    elif request.method == 'POST':
        try: 
            update_assignment = Assignments.query.filter_by(id=request.form['assignment_id']).first()
            update_assignment.topic_name = request.form['topic_name']
            db.session.commit()        
            return redirect('/lecturer/assignments')
        except Exception:
            return redirect('/lecturer/assignments') 


@app.route('/lecturer/delete_assignment/<id>')
def lecturer_delete_assignment(id) -> 'html':
    if 'lecturer_username' not in session:
        return redirect('/lecturer/login')
    else:
        try:
            assignment = Assignments.query.filter_by(id=id).first()
            db.session.delete(assignment)
            db.session.commit()
            return redirect('/lecturer/assignments')
        except Exception:
            return redirect('/lecturer/assignments')


@app.route('/lecturer/students')
def lecturer_students() -> 'html':
    if 'lecturer_username' not in session:
        return redirect('/lecturer/login')
    else:
        lecturer = Lecturers.query.filter_by(email=session['lecturer_username']).first()
        students = Users.query.all()
        students_id = []
        for student in students:
            if student.teachers != None and lecturer.id in [int(i) for i in student.teachers.split(',')]:
                students_id.append(student.id)

        return render_template('dashboard/lecturer_students.html',
                           the_title='All Students - Tarang',
                           lecturer=lecturer,
                           students=students,
                           students_id=students_id)



@app.route('/lecturer/student_remove/<id>')
def lecturer_student_remove(id)-> 'html':
    if 'lecturer_username' not in session:
        return redirect('/lecturer/login')
    else:
        student = Users.query.filter_by(id=id).first()
        teachers_list = list(set([int(i) for i in student.teachers.split(',')]))
        teachers_list.remove(session['lecturer_id'])
        if teachers_list:
            teachers_str = ','.join(str(i) for i in teachers_list)
            student.teachers = teachers_str
            db.session.commit()
        else:
            student.teachers = None
            db.session.commit()
        return redirect('/lecturer/students')




@app.route('/lecturer/studentsrequest')
def lecturer_studentsrequest() -> 'html':
    if 'lecturer_username' not in session:
        return redirect('/lecturer/login')
    else:
        lecturer = Lecturers.query.filter_by(email=session['lecturer_username']).first()        
        students = Users.query.all()
        students_request = []
        if lecturer.students_request:
            students_request = list(set([int(i) for i in lecturer.students_request.split(',')]))
        return render_template('dashboard/lecturer_studentsrequest.html',
                           the_title='New Students Request - Tarang',
                           lecturer=lecturer,
                           students=students,
                           students_request=students_request)


@app.route('/lecturer/student_request_accept/<id>')
def lecturer_student_request_accept(id)-> 'html':
    if 'lecturer_username' not in session:
        return redirect('/lecturer/login')
    else:
        student = Users.query.filter_by(id=id).first()
        lecturer = Lecturers.query.filter_by(id=session['lecturer_id']).first()
        students_request = list(set([int(i) for i in lecturer.students_request.split(',')]))        
        students_request.remove(int(id))
        if students_request:
            students_request_str = ','.join(str(i) for i in students_request)
            lecturer.students_request = students_request_str
            db.session.commit()
        else:
            lecturer.students_request = None
            db.session.commit()

        if student.teachers:
            teachers_list = list(set([int(i) for i in student.teachers.split(',')]))
            teachers_list.append(lecturer.id)
            teachers_str = ','.join(str(i) for i in teachers_list)
            student.teachers = teachers_str
            db.session.commit()
        else:
            student.teachers = str(lecturer.id)
            db.session.commit()

        return redirect('/lecturer/studentsrequest')



@app.route('/lecturer/student_request_deny/<id>')
def lecturer_student_request_deny(id)-> 'html':
    if 'lecturer_username' not in session:
        return redirect('/lecturer/login')
    else:
        lecturer = Lecturers.query.filter_by(id=session['lecturer_id']).first()
        students_request = list(set([int(i) for i in lecturer.students_request.split(',')]))        
        students_request.remove(int(id))
        if students_request:
            students_request_str = ','.join(str(i) for i in students_request)
            lecturer.students_request = students_request_str
            db.session.commit()
        else:
            lecturer.students_request = None
            db.session.commit()
        return redirect('/lecturer/studentsrequest')



@app.route('/lecturer/results')
def lecturer_results() -> 'html':
    if 'lecturer_username' not in session:
        return redirect('/lecturer/login')
    else:
        lecturer = Lecturers.query.filter_by(email=session['lecturer_username']).first()
        return render_template('dashboard/lecturer_results.html',
                           the_title='Students Results- Tarang',
                           lecturer=lecturer)




if __name__ == '__main__':
    app.run()
