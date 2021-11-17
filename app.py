from distutils.log import error
from enum import unique
from flask import Flask, render_template, jsonify, request, redirect,session,g
from flask_restful import Api, Resource
import json

from flask.helpers import url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder='.')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
db = SQLAlchemy(app)
api = Api(app)

# secret key requried for sessions
app.secret_key = 'TEAM106'

class Users(db.Model):
    __tablename__='users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    
    #handles 1 to 1
    teachers = db.relationship("Teachers", backref='users', uselist=False)
    students = db.relationship("Students", backref='users', uselist=False)

    
    def __repr__(self) -> str:
        return '<User %r>' % self.username

class Teachers(db.Model):
    __tablename__='teachers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    #handles 1 to many
    classes = db.relationship('Classes', backref='teacher')
    
    def __repr__(self) -> str:
        return '<User %r>' % self.name
    
Enrollment = db.Table('Enrollment',
                        db.Column('class_id', db.Integer, db.ForeignKey('classes.id')),
                        db.Column('student_id', db.Integer, db.ForeignKey('students.id')),
                        db.Column('grade', db.Integer)
                        )
class Students(db.Model):
    __tablename__='students'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    classes = db.relationship('Classes',secondary=Enrollment)
    def __repr__(self) -> str:
        return '<User %r>' % self.name


class Classes(db.Model):
    __tablename__='classes'
    id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(80), unique=True, nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'))
    num_enrolled = db.Column(db.Integer, unique=False, nullable=False)
    capacity = db.Column(db.Integer, unique=False, nullable=False)
    day_time = db.Column(db.String(80), unique=False, nullable=False)
    #handles many to many
    students = db.relationship('Students',secondary=Enrollment)
    
    def __repr__(self) -> str:
        return '<User %r>' % self.course_name


db.drop_all()
db.create_all()
user = Users(id = 1, username='a', password='b')
user23 = Users(id = 2, username='c', password='d')
db.session.add(user)
db.session.add(user23)
db.session.commit()


student = Students(id=100, name='Yoan', user_id=user.id)
db.session.add(student)
student1 = Students(id=101, name='two', user_id=user23.id)
db.session.add(student1)
db.session.commit()

user1 = Users(id=999, username='z', password='d')
db.session.add(user1)
db.session.commit()
teacher1 = Teachers(id=9, name='Cris', user_id=user1.id)
db.session.add(teacher1)
db.session.commit()

# teacher
user2 = Users(id=559, username='r', password='s')
db.session.add(user2)
db.session.commit()
teacher2 = Teachers(id=10, name='Ramon', user_id=user2.id)
db.session.add(teacher2)
db.session.commit()


# student trying to add
user3 = Users(id=555, username='zero', password='pass')
db.session.add(user3)
db.session.commit()
student3 = Students(id=102,name = 'rob',user_id = user3.id)
db.session.add(student3)
db.session.commit()

# another teacher 
user4 = Users(id = 404, username='ander',password='fliv')
db.session.add(user4)
db.session.commit()
teacher3 = Teachers(id=11,name='Anderson',user_id = user4.id)
db.session.add(teacher3)
db.session.commit()

class1 = Classes(id = 69, course_name='CSE106', teacher=teacher1, num_enrolled=100, capacity=120, day_time='MWF 01:30-02:30 PM')
class2 = Classes(id = 79, course_name='CSE116', teacher=teacher2, num_enrolled=100, capacity=120, day_time='MWF 08:00-09:00 AM')
class3 = Classes(id=89, course_name = 'CSE117' , teacher =teacher3, num_enrolled = 100, capacity = 120, day_time = 'MWF 08:30-09:30 AM')
# class1.students.append(student)
# class2.students.append(student1)
db.session.add(class1)
db.session.add(class2)
db.session.add(class3)
db.session.commit()

enrolled1 = Enrollment.insert().values(class_id=class1.id, student_id=student.id, grade=96)
db.session.execute(enrolled1)
db.session.commit()
enrolled3 = Enrollment.insert().values(class_id=class1.id, student_id=student1.id, grade=100)
db.session.execute(enrolled3)
db.session.commit()
enrolled2 = Enrollment.insert().values(class_id=class2.id, student_id=student1.id, grade=97)
db.session.execute(enrolled2)
db.session.commit()
enrolled4 = Enrollment.insert().values(class_id = class3.id, student_id = student3.id, grade = 94)
db.session.execute(enrolled4)
db.session.commit()

# enrolled5 = Enrollment.insert().values(class_id=class2.id, student_id=student.id, grade=97)
# db.session.execute(enrolled5)
# db.session.commit()

# here start to delete

def add_class(current_class, potential_class):
    
    if(len(current_class) == 18):
        # print('here')
        current_class_days = current_class[0:3].strip()
        current_class_start = current_class[3:9].strip()
        current_class_end = current_class[10:15].strip()
        eve_current = current_class[15:].strip()
    else:
        current_class_days = current_class[0:3].strip()
        current_class_start = current_class[2:8].strip()
        current_class_end = current_class[9:14].strip()
        eve_current = current_class[14:].strip()
    if(len(potential_class) == 17):
        potential_class_days = potential_class[0:3].strip()
        potential_class_start = potential_class[2:8].strip()
        potential_class_end = potential_class[9:14].strip()
        eve_potential = potential_class[14:].strip()
    else:
        potential_class_days = potential_class[0:3].strip()
        potential_class_start = potential_class[3:9].strip()
        potential_class_end = potential_class[10:15].strip()
        eve_potential = potential_class[15:].strip()


    
    # print('$$$$$$$$$$$$$$$')
    # print(current_class_start)
    # print(potential_class_start)
    # print(current_class_end)
    # print(potential_class_end)
    # print('$$$$$$$$$$$$$$$')

    for char in current_class_days:
        if char in potential_class_days:
            if(eve_current != eve_potential):
                return True
            else:
                if(( current_class_start > potential_class_start and current_class_start > potential_class_end )  
                     or (current_class_start < potential_class_start and current_class_end < potential_class_start)):
                    return True
                else:
                    return False
    # print('or here')
    return True

class getPotentialClasses(Resource):
    def get(self):
        if 'user_id' in session:
            query_student = Students.query.filter_by(user_id=session['user_id']).first()
            query = db.session.query(Enrollment).all()
            class_id = []
            potential_classes = []
            current_classes = []

            bool_classes = []

            for cls in query:
                if cls[1] == query_student.id:
                    class_id.append(cls[0])
                    current_classes.append([cls[0],cls[1],cls[2]])
                    json_data = json.loads("{}")
            for cls in query:
                if cls[1] != query_student.id and cls[0] not in class_id:
                    potential_classes.append([cls[0],cls[1],cls[2]])
        # all_classes = db.session.query(Classes.metadata.tables['classes']).all()
        # all_enrollment_classes = db.session.query(Enrollment.metadata.tables['Enrollment']).all()

        #this is calculating the number of students enrolled in potential classes
            for i, cls in enumerate(potential_classes):
                count = 0
                for q in query:
                    if cls[0] == q[0]:
                        count += 1
                potential_classes[i].append(count)
        # this is formatting the data to be sent out
            for cls in potential_classes:
                potential_cls = Classes.query.filter_by(id=cls[0]).first()
                potential_teacher = Teachers.query.filter_by(id = potential_cls.teacher_id).first()
                for cur in current_classes:
                    current_cls = Classes.query.filter_by(id=cur[0]).first()
                    bool_classes.append(add_class(current_cls.day_time,potential_cls.day_time))
                if False not in bool_classes and cls[3] < potential_cls.capacity:
                    json_data.update({cls[0]:{"class_name":potential_cls.course_name,"time":potential_cls.day_time, "teacher_name":potential_teacher.name, "num_enrolled":cls[3], 'capacity':potential_cls.capacity, "addable":1}})
                    bool_classes.clear()
                else:
                    json_data.update({cls[0]:{"class_name":potential_cls.course_name,"time":potential_cls.day_time, "teacher_name":potential_teacher.name, "num_enrolled":cls[3], 'capacity':potential_cls.capacity, "addable":0}})
                    bool_classes.clear()
            return json_data
        return error(400)

class getClasses(Resource):
    def get(self):
        if 'user_id' in session:
            query_student = Students.query.filter_by(user_id=session['user_id']).first()
            query = db.session.query(Enrollment).all()
            list_classes = []
            #retrieve all classes for the given student
            for cls in query:
                if cls[1] == query_student.id:
                    list_classes.append([cls[0],cls[1],cls[2]])
            json_data = json.loads("{}")

            #this is calculating the number of students enrolled in 1 class
            for i, cls in enumerate(list_classes):
                count = 0
                for q in query:
                    if cls[0] == q[0]:
                        count += 1
                list_classes[i].append(count)
            #this is formatting the data to be sent out
            for cls in list_classes:
                current_cls = Classes.query.filter_by(id=cls[0]).first()
                current_teacher = Teachers.query.filter_by(id = current_cls.teacher_id).first()
                json_data.update({cls[0]:{"class_name":current_cls.course_name,"time":current_cls.day_time, "teacher_name":current_teacher.name, "num_enrolled":cls[3], 'capacity':current_cls.capacity}})
            
            return json_data
        return error(400)

class getAllClasses(Resource):
    def get(self):
        return 'help'

api.add_resource(getClasses, '/student/classes')
api.add_resource(getAllClasses, '/student/all_classes')

api.add_resource(getPotentialClasses,'/student/potential_classes')

# assume no user if there is in session then get user g.user for now did only student but have to add teacher also this g.user is used in student html to get name
@app.before_request
def before_request():
    g.user = None
    if 'user_id' in session:
        query = Students.query.filter_by(user_id=session['user_id']).first()
        g.user = query
        
        
# if there does not exist a user in session then will require them to login, if not then redirect them to student.html or teacher.html which havent implemented
@app.route('/student')
def student_logged():
    if not g.user:
        return redirect(url_for('login_post'))
    return render_template('student.html')

@app.route('/login', methods=['GET', 'POST'])
def login_post():
    if request.method == 'POST':
        session.pop('user_id',None)
        username = request.form['username']
        password = request.form['password']
        query = Users.query.filter_by(username=username).first()
        if query is not None:
            if password == query.password:
                session['user_id'] = query.id
                # query = Students.query.filter_by(user_id=query.id).first()
                print(session['user_id'])
                return redirect(url_for('student_logged'))
                # return render_template('student.html')
            else:
                return redirect(url_for('login_post'))
    return render_template('login.html')

# this is to logout the user
@app.route('/my-link/')
def my_link():
#  pop the user fro the current session then redirect to login
    session.pop('user_id',None)
    return redirect(url_for('login_post'))

if __name__ == '__main__':
    app.run(debug=True)