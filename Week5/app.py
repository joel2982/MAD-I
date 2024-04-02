from flask import Flask, redirect, request, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
import os

# Instantiate App
app = Flask(__name__)
current_dir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(current_dir, 'database.sqlite3')
db = SQLAlchemy(app)
app.app_context().push()

class Student(db.Model):
    __tablename__ = 'student'
    student_id = db.Column(db.Integer,autoincrement = True,primary_key = True)
    roll_number = db.Column(db.String,unique = True,nullable = False)
    first_name = db.Column(db.String,nullable = False)
    last_name = db.Column(db.String)
    courses = db.relationship("Course",secondary = "enrollments")

class Course(db.Model):
    __tablename__ = 'course'
    course_id = db.Column(db.Integer,autoincrement = True,primary_key = True)
    course_code = db.Column(db.String,nullable = False, unique = True)
    course_name = db.Column(db.String,nullable = False)
    course_description = db.Column(db.String)

class Enrollments(db.Model):
    __tablename__ = 'enrollments'
    enrollment_id = db.Column(db.Integer,autoincrement = True,primary_key = True)
    estudent_id = db.Column(db.Integer,db.ForeignKey('student.student_id'),nullable = False)
    ecourse_id = db.Column(db.Integer,db.ForeignKey('course.course_id'),nullable = False)


@app.route('/')
def home():
    students = Student.query.all()
    if students:
        return render_template('studentList.html',student_data = students)
    else:
        return render_template('noStudent.html')
    
@app.route('/student/<int:student_id>')
def view(student_id):
    student = db.session.query(Student).filter_by(student_id =student_id).one()
    return render_template('viewStudent.html',student = student)

@app.route('/student/create/',methods = ['GET','POST'])
def createStudent():
    if request.method == 'GET':
        return render_template('addStudent.html')
    elif request.method == 'POST':
        roll_number = request.form['roll']
        first_name = request.form['f_name']
        last_name = request.form['l_name']
        courses = request.form.getlist('courses')

        check_duplicate = db.session.query(Student).filter_by(roll_number = roll_number).first()
        if check_duplicate:
            return render_template('studentExisits.html')
        
        try:
            new_student = Student(roll_number = roll_number, first_name = first_name, last_name = last_name)
            for course_id in courses:
                course = db.session.query(Course).filter_by(course_id = int(course_id[-1])).one()
                new_student.courses.append(course)
            db.session.add(new_student)
            db.session.commit()
        except Exception as E:
            print(E)
            print("ROLLING BACK")
            db.session.rollback()
        else:
            print("COMMITTING CHANGES")            
            db.session.commit()

        return redirect('/')

@app.route('/student/<int:student_id>/update',methods = ['GET','POST'])
def update(student_id):
    student_data = db.session.query(Student).filter_by(student_id = student_id).one()
    if request.method == 'GET':
        course_id = []
        for course in student_data.courses:
            course_id.append(course.course_id)
        return render_template('updateStudent.html',student = student_data,course_id = course_id)
    elif request.method == 'POST':
        first_name = request.form['f_name']
        last_name = request.form['l_name']
        courses = request.form.getlist('courses')
        
        try:
            student_data.first_name = first_name
            student_data.last_name = last_name
            student_data.courses = []
            for course_id in courses:
                course = db.session.query(Course).filter_by(course_id = int(course_id[-1])).one()
                student_data.courses.append(course)
            db.session.commit()
        except Exception as E:
            print(E)
            print("ROLLING BACK")
            db.session.rollback()
        else:
            print("COMMITTING CHANGES")            
            db.session.commit()
        return redirect('/')

if __name__ == '__main__':
    app.run(debug = True)