from flask import Flask
from models import *
from api import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite3'
db.init_app(app)
api = Api(app)
# print(app.config)
app.app_context().push()

# connecting API classes to the url routes
api.add_resource(CourseApi,'/api/course','/api/course/<int:course_id>')
api.add_resource(StudentApi,'/api/student','/api/student/<int:student_id>')
api.add_resource(EnrollmenrApi,'/api/student/<int:student_id>/course','/api/student/<int:student_id>/course/<int:course_id>')


if __name__ == '__main__':
    app.run(debug=True)