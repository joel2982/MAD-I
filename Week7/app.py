from flask import Flask, redirect, render_template, request
from models import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite3'
db.init_app(app)
app.app_context().push()

#----------------------- Student APIs -----------------------

@app.route('/')
def home():
    students = Student.query.all()
    return render_template('home.html',students=students)

@app.route('/student/create',methods=['GET','POST'])
def create_student():
    if request.method == 'POST':
        roll_number = request.form['roll_number']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        course_ids = request.form.getlist('course')
        check_duplicate = Student.query.filter_by(roll_number=roll_number).first()
        if check_duplicate:
            return render_template('student_exists.html')
        new_student = Student(
            roll_number=roll_number,
            first_name=first_name,
            last_name=last_name,
        )
        for course_id in course_ids:
            course = Course.query.filter_by(course_id=int(course_id)).first()
            new_student.courses.append(course)
        db.session.add(new_student)
        db.session.commit()
        return redirect('/')
    else:
        courses = Course.query.all()
        return render_template('create_student.html',courses=courses)
    
@app.route("/student/<int:student_id>")
def display_student(student_id):
    student = Student.query.filter_by(student_id=student_id).first()
    return render_template('display_student.html',student=student)

@app.route("/student/<int:student_id>/withdraw/<int:course_id>")
def withdraw_course(student_id,course_id):
    student = Student.query.get(student_id)
    course_to_withdrawn = Course.query.get(course_id)
    student.courses.remove(course_to_withdrawn)
    db.session.commit()
    return redirect('/')

@app.route("/student/<int:student_id>/update",methods=['GET','POST'])
def update_student(student_id):
    if request.method == 'POST':
        student = Student.query.get(student_id)
        student.first_name = request.form.get('first_name')
        student.last_name = request.form.get('last_name')
        course_id = request.form.get('course',None)
        if course_id is not None:
            course = Course.query.filter_by(course_id=int(course_id)).first()
            student.courses.append(course)
        db.session.commit()
        return redirect('/')
    else:
        student = Student.query.get(student_id)
        courses = Course.query.all()
        return render_template('update_student.html',student=student,courses=courses)


@app.route("/student/<int:student_id>/delete")
def delete_student(student_id):
    student = Student.query.get(student_id)
    db.session.delete(student)
    db.session.commit()
    return redirect('/')
    
#----------------------- Course APIs -----------------------

@app.route("/courses")
def all_courses():
    courses = Course.query.all()
    return render_template('course_list.html',courses=courses)

@app.route("/course/<int:course_id>")
def display_course(course_id):
    course = Course.query.get(course_id)
    return render_template('display_course.html',course=course)


@app.route("/course/create",methods=['GET','POST'])
def create_course():
    if request.method == 'POST':
        course_code = request.form.get('course_code')
        course_name = request.form.get('course_name')
        course_description = request.form.get('course_description',None)
        duplicate = Course.query.filter_by(course_code=course_code).first()
        if duplicate:
            return render_template('course_exists.html')
        else:
            new_course = Course(
                    course_code=course_code,
                    course_name=course_name,
                    course_description=course_description
                )
            db.session.add(new_course)
            db.session.commit()
            return redirect('/courses')
    else:
        return render_template('create_course.html')
    
@app.route("/course/<int:course_id>/update",methods=['GET','POST'])
def update_course(course_id):
    if request.method == 'POST':
        course = Course.query.get(course_id)
        course_name = request.form.get('course_name')
        course_description = request.form.get('course_description',None)
        course.course_name = course_name
        course.course_description = course_description
        db.session.commit()
        return redirect('/courses')
    else:
        course = Course.query.get(course_id)    
        return render_template('update_course.html',course=course)

@app.route("/course/<int:course_id>/delete")
def delete_course(course_id):
    course = Course.query.get(course_id)
    db.session.delete(course)
    db.session.commit()
    return redirect('/courses')

if __name__ == '__main__':
    app.run(debug=True)