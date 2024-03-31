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
    print(students)
    return render_template('student.html',student_data = students)

if __name__ == '__main__':
    app.debug = True
    app.run()