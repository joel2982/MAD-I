from flask import Flask,render_template,request
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

app = Flask(__name__)

def student(id):
    data = pd.read_csv('data.csv')
    student_data = data[id == data['Student id']]
    if student_data.empty:
        return render_template('ErrorTemplate.html')
    total_marks = student_data[' Marks'].sum()
    student_list = student_data.to_dict('records')
    return render_template('StudentTemplate.html',total_marks = total_marks,student_data = student_list)

def course(id):
    data = pd.read_csv('data.csv')
    course_data = pd.DataFrame()
    course_data = data[id == data[' Course id']]
    if course_data.empty:
        return render_template('ErrorTemplate.html')
    avg_marks = course_data[' Marks'].mean()
    max_marks = course_data[' Marks'].max()
    print(course_data[' Marks'])
    plt.hist(course_data[' Marks'])
    plt.title(f'Course ID = {id}')
    plt.xlabel('Marks')
    plt.ylabel('Frequency')
    plt.savefig('static\histogram.png')
    plt.close() # vey important
    return render_template('CourseTemplate.html',avg_marks = avg_marks,max_marks = max_marks)


@app.route('/', methods = ['GET','POST'])
def home():
    if request.method == 'GET':
        return render_template('index.html')
    
    elif request.method == 'POST':
        id = request.form.get('ID')
        value = int(request.form.get('id_value'))
        print(id,value)
        if id == 'student_id':
            return student(value)
        elif id == 'course_id':
            return course(value)
        else:
            return render_template('ErrorTemplate.html')


if __name__ == '__main__':
    app.debug = True
    app.run()
