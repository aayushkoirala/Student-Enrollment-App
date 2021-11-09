from enum import unique
from flask import Flask, render_template, jsonify, request, redirect,session,g
import json

from flask.helpers import url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder='.')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
db = SQLAlchemy(app)

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
        return '<User %r>' % self.Course_Name

db.drop_all()
db.create_all()
user = Users(id = 1, username='a', password='b')
db.session.add(user)
db.session.commit()
student = Students(id=100, name='Yoan', user_id=user.id)
db.session.add(student)
db.session.commit()
user1 = Users(id=999, username='c', password='d')
db.session.add(user1)
db.session.commit()
teacher1 = Teachers(id=9, name='Cris', user_id=user1.id)
db.session.add(teacher1)
db.session.commit()

class1 = Classes(course_name='CSE106', teacher=teacher1, num_enrolled=100, capacity=120, day_time='MWF 1:30-2:30')
class1.students.append(student)
db.session.add(class1)
db.session.commit()

def to_json(data):
    try:
        json_data = json.loads("{}")
        for student in data:
            json_data.update({'username':student.username, 'password':student.password})
    except:
        json_data = json.loads("{}")
        json_data.update({'username':data.username, 'password':data.password})
    return json_data

def to_json_class(data):
    try:
        json_data = []
        for cls in data:
            json_data.append({'class_id':cls.class_id, 'student_id':cls.student_id, 'grade':cls.grade})
    except:
        json_data = []
        json_data.append({'class_id':data.class_id, 'student_id':data.student_id, 'grade':cls.grade})
    return json.dumps(json_data)

@app.route('/home/<string:username>')
def home(username):
    #trys to query data if its student or not, this probably will need some ajustments since I think the try will always succeed even if theres no data the exist in the db
    try:
        data = Students.query.filter_by(username=username).first()
        student = True
    except:
        data = Teachers.query.filter_by(username=username).first()
        student = False
        
    if student:
        #if student then do the queries to enrollment table
        enrl = Enrollment.query.filter_by(student_id=data.id).first()
        enrl = to_json_class(enrl) #[{'class_id':class_id, 'studen_id':student_id, 'grade':grade}, {'class_id':class_id, 'studen_id':student_id},{'class_id':class_id, 'studen_id':student_id}]
        table = [] #list of tuple (couse name, teacher, time, etc.)
        for cls in enrl:
            #after we know the data from enrollment table then we can query Classes and Teachers to get the neccesary data
            cls_temp = Classes.query.filter_by(id=cls.class_id)
            cls_teacher = Teachers.query.filter_by(id=cls_temp.teacher_id)
            #table is the variable that im using to store all the data and be ready to be sent out
            table.append({'course_name':cls_temp.course_name, 'teacher_name':cls_teacher.name, 'day_time':cls_temp.day_time, 'num_enrolled':cls_temp.num_enrolled})
        table = json.dumps(table) #making sure its an json object
    else:
        #similar concept as student except that we only need to query
        table = [] #list of tuple (couse name, teacher, time, etc.)
        cls_temp = Classes.query.filter_by(id=data.id) #queries Classes to retrieve where current teacher (the user login ass) is teaching those classes
        for cls in cls_temp: #itterates thru each class
            #inserts into variable table 
            table.append({'course_name':cls_temp.course_name, 'teacher_name':data.name, 'day_time':cls_temp.day_time, 'num_enrolled':cls_temp.num_enrolled})
        table = json.dumps(table) #making sure its an json object
    return 'Successfully query data'

# assume no user if there is in session then get user g.user for now did only student but have to add teacher also this g.user is used in student html to get name
@app.before_request
def before_request():
    g.user = None
    if 'user_id' in session:
        query = Students.query.filter_by(user_id=session['user_id']).first()
        g.user = query
        
        
# if there does not exist a user in session then will require them to login, if not then redirect them to student.html or teacher.html which havent implemented
@app.route('/student',methods = ['GET','POST'])
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
    # if request.method == 'POST':
    #     
    #     username = req["username"]
    #     password = req["password"]
    #     print("11111111111111111")
    #     print(username)
    #     print(password)
    #     # return render_template('student.html')
    #     query = Users.query.filter_by(username=username).first()
    #     if query is not None:
    #         if password == query.password:
    #             return render_template('student.html')
    # else:
    #     return render_template('login.html')
# -----------------------------------------------

    # if request.method == 'POST':
    #     username = request.form['username']
    #     usr_entered = request.form['password']
    # #queries username and password from db
    # query = Users.query.filter_by(username=username).first()
    # if query is not None:
    #     #if username exist
    #     try:
    #         data = to_json(query)
    #         password = data['password']
    #     except Exception:
    #         error = 'Invalid Username or Password'
    #         return render_template('login.html', error=error)
    #     if password == usr_entered: #check if its correct password
    #         return 'You successfully login' #redirect to home and send username on the url
    #         #return redirect(f'/home/{username}')
    #     else: #else return invalid
    #         error = 'Invalid Username or Password'
    #         return f'Fail: {error}'
    #         #return render_template('login.html', error=error)

    # else:
    #     error = 'Invalid Username or Password'
    #     #return render_template('login.html', error=error)
    #     return f'Fail: {error}'

    

# @app.route('/login')
# def login():
#     return render_template('login.html')


# this is to logout the user
@app.route('/my-link/')
def my_link():
#  pop the user fro the current session then redirect to login
  session.pop('user_id',None)
  return redirect(url_for('login_post'))

if __name__ == '__main__':
    app.run(debug=True)