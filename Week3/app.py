import sys
import pandas as pd
from jinja2 import Template 
import matplotlib.pyplot as plt 

data = pd.read_csv('data.csv')


def student_html(student_data):
    total_marks = student_data[' Marks'].sum()
    file = open('Templates\StudentTemplate.html.jinja2','r')
    student_html_template = file.read()
    file.close()

    html_template = Template(student_html_template)
    student_list = student_data.to_dict('records')
    content = html_template.render(student_data = student_list, total_marks = total_marks)

    student_html_doc = open('output.html','w')
    student_html_doc.write(content)
    student_html_doc.close()


def course_html(course_data):
    max_marks = course_data[' Marks'].max()
    avg_marks = course_data[' Marks'].mean()
    file = open('Templates\CourseTemplate.html.jinja2','r')
    course_html_template = file.read()
    file.close()
    
    plt.hist(course_data[' Marks'])
    course_id = course_data[' Course id'].iloc[0]
    print(course_id)
    plt.title(f"Course ID = {course_id}")
    plt.xlabel("Marks")
    plt.ylabel("Frequency")
    plt.savefig('histogram.png')

    html_template = Template(course_html_template)
    content = html_template.render(avg_marks = avg_marks, max_marks = max_marks)

    course_html_doc = open('output.html','w')
    course_html_doc.write(content)
    course_html_doc.close()
    
def error_html():
    file = open('Templates\ErrorTemplate.html.jinja2','r')
    error_html_template = file.read()
    file.close()

    html_template = Template(error_html_template)
    content = html_template.render()

    error_html_doc = open('output.html','w')
    error_html_doc.write(content)
    error_html_doc.close()

def main():
    try :
        option = sys.argv[1].lower()
        value = int(sys.argv[2])
        if option == '-s' and data['Student id'].isin([value]).any():
            student_data = data[data['Student id'] == value]
            student_html(student_data)
        elif option == '-c' and value in data[' Course id'].values:
            course_data = data[data[' Course id'] == value]
            course_html(course_data)
        else:
            raise Exception
    except:
        print('Wrong Inputs')
        error_html()


if __name__ == '__main__' :
    main()