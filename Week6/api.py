from flask_restful import Resource, reqparse, Api, marshal_with, fields
from models import db, Course, Student, Enrollment
from validation import NotFoundError, BusinessValidationError

# ---------------Fields---------------
# user Data Validation
# this helps in orienting the output from the class methods such that it serializes
# converts method returned value into json object with only the specified fields
course_fields = {
    'course_id' : fields.Integer,
    'course_code' : fields.String,
    'course_name' : fields.String,
    'course_description' : fields.String
}

student_fields = {
    'student_id' : fields.Integer,
    'roll_number' : fields.String,
    'first_name' : fields.String,
    'last_name' : fields.String,
}

enrollment_fields = {
    'enrollment_id' : fields.Integer,
    'student_id' : fields.Integer,
    'course_id' : fields.Integer
}
# ------------------------------------

# ---------Praser Arguements----------
# https://flask-restful.readthedocs.io/en/latest/reqparse.html
# accepts and parses the json body given as a Request
course_praser = reqparse.RequestParser()
course_praser.add_argument('course_code')
course_praser.add_argument('course_name')
course_praser.add_argument('course_description')

student_praser = reqparse.RequestParser()
student_praser.add_argument('roll_number')
student_praser.add_argument('first_name')
student_praser.add_argument('last_name')

enrollment_praser = reqparse.RequestParser()
enrollment_praser.add_argument('course_id')
# ------------------------------------

# ------------API Classes-------------
# https://medium.com/@owenadira/flask-restful-data-marshalling-using-fields-2ecee98c45f4
# The decorator marshal_with is what actually takes your data object and applies the field filtering. 
# Data marshalling can work on single objects, dicts, or lists of objects.
class CourseApi(Resource):
    @marshal_with(course_fields)
    def get(self,course_id):
        course = Course.query.filter_by(course_id=course_id).first()
        # throws 404 error if course is not present 
        if course is None:
            raise NotFoundError(status_code=404)
        return course

    @marshal_with(course_fields) 
    def post(self):
        # parsing and getting the arguements
        args = course_praser.parse_args()
        course_name = args.get('course_name',None)
        course_code = args.get('course_code',None) 
        course_description = args.get('course_description',None)
        if course_name is None:
            raise BusinessValidationError(
                status_code=400,
                error_code='COURSE001',
                error_message="Course Name is required"
            )
        if course_code is None:
            raise BusinessValidationError(
                status_code=400,
                error_code='COURSE002',
                error_message="Course Code is required"
            )
        course = Course.query.filter_by(course_code=course_code).first()
        if course is not None:
            raise NotFoundError(status_code=409)
        new_course = Course(
            course_code = course_code,
            course_name = course_name,
            course_description = course_description
        )
        db.session.add(new_course)
        db.session.commit()
        return new_course,201
        
    @marshal_with(course_fields) 
    def put(self,course_id):
        course = Course.query.filter_by(course_id=course_id).first()
        if course is None:
            raise NotFoundError(status_code=404)
        args = course_praser.parse_args()
        course_name = args.get('course_name',None)
        course_code = args.get('course_code',None)
        if course_name is None:
            raise BusinessValidationError(
                status_code=400, 
                error_code='COURSE001', 
                error_message='Course Name is required'
            )
        if course_code is None:
            raise BusinessValidationError(
                status_code=400, 
                error_code='COURSE002', 
                error_message='Course Code is required'
                )
        course.course_name = course_name
        course.course_code = course_code
        course.course_description = args.get('course_description',None)
        db.session.commit()
        return course

    def delete(self,course_id):
        course = Course.query.filter_by(course_id=course_id).first()
        if course is None:
            raise NotFoundError(status_code=404)
        db.session.delete(course)
        db.session.commit()
        return 200
    
class StudentApi(Resource):
    @marshal_with(student_fields)
    def get(self,student_id):
        student = Student.query.filter_by(student_id=student_id).first()
        if student is None:
            raise NotFoundError(status_code=404)
        return student
    
    @marshal_with(student_fields)
    def post(self):
        args = student_praser.parse_args()
        roll_number = args.get('roll_number',None)
        first_name = args.get('first_name',None)
        last_name = args.get('last_name',None)
        if roll_number is None:
            raise BusinessValidationError(
                status_code=400,
                error_code='STUDENT001',
                error_message='Roll Number required'
            )
        if first_name is None:
            raise BusinessValidationError(
                status_code=400,
                error_code='STUDENT002',
                error_message='First Name is required'
            )
        student = Student.query.filter_by(roll_number=roll_number).first()
        if student is not None:
            raise NotFoundError(status_code=409)
        new_student = Student(
            roll_number=roll_number,
            first_name=first_name,
            last_name=last_name
        )
        db.session.add(new_student)
        db.session.commit()
        return new_student,201
    
    @marshal_with(student_fields)
    def put(self,student_id):
        student = Student.query.filter_by(student_id=student_id).first()
        if student is None:
            raise NotFoundError(status_code=404)
        args = student_praser.parse_args()
        roll_number = args.get('roll_number',None)
        first_name = args.get('first_name',None)
        last_name = args.get('last_name',None)
        if roll_number is None:
            raise BusinessValidationError(
                status_code=400,
                error_code='STUDENT001',
                error_message='Roll Number required'
            )
        if first_name is None:
            raise BusinessValidationError(
                status_code=400,
                error_code='STUDENT002',
                error_message='First Name is required'    
            )
        student.roll_number = roll_number
        student.first_name = first_name
        student.last_name = last_name
        db.session.commit()
        return student

    def delete(self,student_id):
        student = Student.query.filter_by(student_id=student_id).first()
        if student is None:
            raise NotFoundError(status_code=404)
        db.session.delete(student)
        db.session.commit()
        return 200
    
class EnrollmenrApi(Resource):
    @marshal_with(enrollment_fields)
    def get(self,student_id):
        student = Student.query.filter_by(student_id=student_id).first()
        if student is None:
            raise BusinessValidationError(
                status_code=400,
                error_code='ENROLLMENT002',
                error_message='Student does not exist.'
            )
        enrollments = Enrollment.query.filter_by(student_id=student_id).all()
        if enrollments == []:
            raise NotFoundError(status_code=404)
        return enrollments
    
    @marshal_with(enrollment_fields)
    def post(self,student_id):
        student = Student.query.filter_by(student_id=student_id).first()
        if student is None:
            raise NotFoundError(status_code=404)
        args = enrollment_praser.parse_args()
        course_id = args.get('course_id',None)
        if course_id is None:
            raise BusinessValidationError(
                status_code=400,
                error_code='COURSE002',
                error_message='Course Code is required'
            )
        course = Course.query.filter_by(course_id=course_id).first()
        if course is None:
            raise BusinessValidationError(
                status_code=400,
                error_code='ENROLLMENT001',
                error_message='Course does not exist'
            )
        new_enrollment = Enrollment(
            student_id=student_id,
            course_id=course_id
        )
        db.session.add(new_enrollment)
        db.session.commit()
        return new_enrollment,201
    
    def delete(self,student_id,course_id):
        student = Student.query.filter_by(student_id=student_id).first()
        if student is None:
            raise BusinessValidationError(
                status_code=400,
                error_code='ENROLLMENT002',
                error_message='Student does not exist.'
            )
        course = Course.query.filter_by(course_id=course_id).first()
        if course is None:
            raise BusinessValidationError(
                status_code=400,
                error_code='ENROLLMENT001',
                error_message='Course does not exist'
            )
        enrollment = Enrollment.query.filter_by(student_id=student_id,course_id=course_id).first()
        if enrollment is None:
            raise NotFoundError(status_code=404)
        db.session.delete(enrollment)
        db.session.commit()
        return 200

# ------------------------------------