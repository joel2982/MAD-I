from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Course(db.Model):
    __tablename__ = "course"
    course_id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    course_name = db.Column(db.String(50),nullable=False)
    course_code = db.Column(db.String(10),unique=True,nullable=False)
    course_description = db.Column(db.String(100))
    
class Student(db.Model):
    __tablename__ = "student"
    student_id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    roll_number = db.Column(db.String(10),unique=True,nullable=False)
    first_name = db.Column(db.String(25),nullable=False)
    last_name = db.Column(db.String(25))
    courses = db.relationship('Course',secondary='enrollment',backref='students')

class Enrollment(db.Model):
    __tablename__ = "enrollment"
    enrollment_id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    course_id = db.Column(db.Integer,db.ForeignKey('course.course_id'),nullable=False)
    student_id = db.Column(db.Integer,db.ForeignKey('student.student_id'),nullable=False)
