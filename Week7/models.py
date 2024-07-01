from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Student(db.Model):
    __tablename__ = "student"
    student_id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    roll_number = db.Column(db.String(10),nullable=False,unique=True)
    first_name = db.Column(db.String(25),nullable=False)
    last_name = db.Column(db.String(50))
    courses = db.relationship('Course',secondary='enrollment',backref='students')

class Course(db.Model):
    __tablename__ = "course"
    course_id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    course_code = db.Column(db.String(10),nullable=False,unique=True)
    course_name = db.Column(db.String(25),nullable=False)
    course_description = db.Column(db.String(50))

class Enrollment(db.Model):
    __tablename__ = "enrollment"
    enrollment_id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    student_id = db.Column(db.Integer,db.ForeignKey('student.student_id'),nullable=False)
    course_id = db.Column(db.Integer,db.ForeignKey('course.course_id'),nullable=False)
    