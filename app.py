from flask import Flask, render_template, jsonify, request, redirect, session, g
from flask_restful import Api, Resource
from flask.helpers import url_for
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from distutils.log import error
import json

app = Flask(__name__, template_folder='.')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
db = SQLAlchemy(app)
api = Api(app)
admin = Admin(app)
# secret key requried for sessions
app.secret_key = 'TEAM106'


class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    # handles 1 to 1
    teachers = db.relationship("Teachers", backref='users', uselist=False)
    students = db.relationship("Students", backref='users', uselist=False)

    def __repr__(self) -> str:
        return '<User %r>' % self.username


class Teachers(db.Model):
    __tablename__ = 'teachers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    # handles 1 to many
    classes = db.relationship('Classes', backref='teacher')

    def __repr__(self) -> str:
        return '<User %r>' % self.name


class Enrollment_table(db.Model):
    __tablename__ = 'enrollment_table'
    id = db.Column(db.Integer, primary_key=True)
    class_id = db.Column('class_id', db.Integer)
    student_id = db.Column('student_id', db.Integer)
    grade = db.Column('grade', db.Integer)

    def __repr__(self) -> str:
        return '<User %r>' % self.id


class Students(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self) -> str:
        return '<User %r>' % self.name


class Classes(db.Model):
    __tablename__ = 'classes'
    id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(80), unique=True, nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'))
    num_enrolled = db.Column(db.Integer, unique=False, nullable=False)
    capacity = db.Column(db.Integer, unique=False, nullable=False)
    day_time = db.Column(db.String(80), unique=False, nullable=False)

    def __repr__(self) -> str:
        return '<User %r>' % self.course_name


class SecureModelView(ModelView):
    def is_accessible(self):
        try:
            return session['user_id'] == Users.query.filter_by(id=1).first().id
        except:
            return False


admin.add_view(SecureModelView(Classes, db.session))
admin.add_view(SecureModelView(Students, db.session))
admin.add_view(SecureModelView(Enrollment_table, db.session))
admin.add_view(SecureModelView(Teachers, db.session))
admin.add_view(SecureModelView(Users, db.session))

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
            query = db.session.query(Enrollment_table.metadata.tables['enrollment_table']).all()
            class_id = []
            potential_classes = []
            current_classes = []

            bool_classes = []

            for cls in query:
                if cls[2] == query_student.id:
                    class_id.append(cls[1])
                    current_classes.append([cls[1],cls[2],cls[3]])
                    json_data = json.loads("{}")
            for cls in query:
                if cls[2] != query_student.id and cls[1] not in class_id:
                    potential_classes.append([cls[1],cls[2],cls[3]])
        # all_classes = db.session.query(Classes.metadata.tables['classes']).all()
        # all_enrollment_classes = db.session.query(Enrollment.metadata.tables['Enrollment']).all()

        #this is calculating the number of students enrolled in potential classes
            for i, cls in enumerate(potential_classes):
                count = 0
                for q in query:
                    if cls[0] == q[1]:
                        count += 1
                potential_classes[i].append(count)
            for i, cls in enumerate(current_classes):
                count = 0
                for q in query:
                    if cls[0] == q[1]:
                        count += 1
                current_classes[i].append(count)
        # this is formatting the data to be sent out
            for cls in potential_classes:
                potential_cls = Classes.query.filter_by(id=cls[0]).first()
                potential_teacher = Teachers.query.filter_by(id = potential_cls.teacher_id).first()
                for cur in current_classes:
                    current_cls = Classes.query.filter_by(id=cur[0]).first()
                    current_teacher = Teachers.query.filter_by(id = current_cls.teacher_id).first()
                    bool_classes.append(add_class(current_cls.day_time,potential_cls.day_time))
                    json_data.update({cur[0]:{"class_name":current_cls.course_name,"time":current_cls.day_time, "teacher_name":current_teacher.name, "num_enrolled":cur[3], 'capacity':current_cls.capacity, "addable":0}})
                if False not in bool_classes and cls[3] < potential_cls.capacity:
                    json_data.update({cls[0]:{"class_name":potential_cls.course_name,"time":potential_cls.day_time, "teacher_name":potential_teacher.name, "num_enrolled":cls[3], 'capacity':potential_cls.capacity, "addable":1}})
                    bool_classes.clear()
                else:
                    json_data.update({cls[0]:{"class_name":potential_cls.course_name,"time":potential_cls.day_time, "teacher_name":potential_teacher.name, "num_enrolled":cls[3], 'capacity':potential_cls.capacity, "addable":0}})
                    bool_classes.clear()
            return json_data
        return error(400)

class updateDB(Resource):
    def put(self):
        json_data = request.data
        # to double quotes to make it valid JSON
        my_json = json_data.decode('utf8').replace("'", '"')

        # Load the JSON to a Python list & dump it back out as formatted JSON
        data = json.loads(my_json)
        s = json.dumps(data, indent=4, sort_keys=True)
        json_data = json.loads(s)
        for name in json_data['student']:
            query_student = Students.query.filter_by(name=name).first()
            query = Enrollment_table.query.filter_by(
                student_id=query_student.id, class_id=json_data['class_id']).first()
            print(query.class_id, query.student_id)
            query.grade = json_data['student'][name]
            db.session.commit()

class addCourse(Resource):
    def post(self):
        json_data = json.loads(request.data)
        course = json_data["class_id"]
        query_student = Students.query.filter_by(user_id=session['user_id']).first()
        current_cls = Classes.query.filter_by(course_name=course).first()
        enrolled1 = Enrollment_table(class_id=current_cls.id, student_id=query_student.id, grade=0)
        db.session.add(enrolled1)
        db.session.commit()
        return 200

class getClasses(Resource):
    def get(self):
        if 'user_id' in session:
            query_student = Students.query.filter_by(
                user_id=session['user_id']).first()
            query = Enrollment_table.query.all()
            list_classes = []
            # retrieve all classes for the given student
            for cls in query:
                if cls.student_id == query_student.id:
                    list_classes.append(
                        [cls.class_id, cls.student_id, cls.grade])
            json_data = json.loads("{}")

            # this is calculating the number of students enrolled in 1 class
            for i, cls in enumerate(list_classes):
                count = 0
                for q in query:
                    if cls[0] == q.class_id:
                        count += 1
                list_classes[i].append(count)
            # this is formatting the data to be sent out
            for cls in list_classes:
                current_cls = Classes.query.filter_by(id=cls[0]).first()
                current_teacher = Teachers.query.filter_by(
                    id=current_cls.teacher_id).first()
                json_data.update({cls[0]: {"class_name": current_cls.course_name, "time": current_cls.day_time,
                                           "teacher_name": current_teacher.name, "num_enrolled": cls[3], 'capacity': current_cls.capacity}})
            return json_data
        return error(400)


class getTeacherClasses(Resource):
    def get(self):
        if 'user_id' in session:
            query_teacher = Teachers.query.filter_by(
                user_id=session['user_id']).first()
            query_classes = Classes.query.filter_by(
                teacher_id=query_teacher.id).all()
            query = Enrollment_table.query.all()

            list_classes = []
            list_class_id = []
            # retrieve all classes for the given student
            for cls in query:
                for q in query_classes:
                    if cls.class_id == q.id:
                        list_classes.append(
                            [cls.class_id, cls.student_id, cls.grade])
                        list_class_id.append(cls.class_id)
            json_data = json.loads("{}")

            # this is calculating the number of students enrolled in 1 class
            for i, cls in enumerate(list_classes):
                count = 0
                for q in query:
                    if cls[0] == q.class_id:
                        count += 1
                list_classes[i].append(count)
            # this is formatting the data to be sent out
            for cls in query_classes:
                if cls.id in list_class_id:
                    index = list_class_id.index(cls.id)
                    num_enrolled = list_classes[index][3]
                else:
                    num_enrolled = 0
                json_data.update({cls.id: {"class_name": cls.course_name, "time": cls.day_time,
                                           "teacher_name": query_teacher.name, "num_enrolled": num_enrolled, 'capacity': cls.capacity}})
            return json_data
        return error(400)

api.add_resource(getClasses, '/student/classes')
api.add_resource(getTeacherClasses, '/teacher/classes')
api.add_resource(updateDB, '/update_grades')
api.add_resource(getPotentialClasses,'/student/potential_classes')
api.add_resource(addCourse,'/student/add_course')
# assume no user if there is in session then get user g.user for now did only student but have to add teacher also this g.user is used in student html to get name
@app.before_request
def before_request():
    g.user = None
    if 'user_id' in session:
        query = Students.query.filter_by(user_id=session['user_id']).first()
        if query is None:
            query = Teachers.query.filter_by(
                user_id=session['user_id']).first()
        g.user = query


# if there does not exist a user in session then will require them to login, if not then redirect them to student.html or teacher.html which havent implemented
@app.route('/student')
def student_logged():
    if not g.user:
        return redirect(url_for('login_post'))
    return render_template('student.html')


@app.route('/teacher')
def teacher_logged():
    if not g.user:
        return redirect(url_for('login_post'))
    return render_template('teacher.html')


@app.route('/student_grades/<id>')
def edit_grades(id):
    if not g.user:
        return redirect(url_for('login_post'))
    return render_template(f'edit_grades.html', id=id)


@app.route('/student_get_grades/<id>')
def edit_get_grades(id):
    query = Enrollment_table.query.all()
    data = []
    for q in query:
        if q.class_id == int(id):
            data.append([q.class_id, q.student_id, q.grade])
    json_data = json.loads("{}")

    for i, cls in enumerate(data):
        student = Students.query.filter_by(id=cls[1]).first()
        json_data.update({i: {"student_name": student.name, "grade": cls[2]}})

    return json_data


@app.route('/', methods=['GET', 'POST'])
def login_post():
    if request.method == 'POST':
        session.pop('user_id', None)
        username = request.form['username']
        password = request.form['password']
        query_user = Users.query.filter_by(username=username).first()
        if query_user is not None:
            if password == query_user.password:
                session['user_id'] = query_user.id
                print(session['user_id'])
                print(Users.query.filter_by(id=1).first().id)
                if session['user_id'] == Users.query.filter_by(id=1).first().id:
                    return redirect('/admin')
                query = Students.query.filter_by(user_id=query_user.id).first()
                isTeacher = False
                if query == None:
                    query = Teachers.query.filter_by(
                        user_id=query_user.id).first()
                    isTeacher = True
                if isTeacher:
                    return redirect(url_for('teacher_logged'))
                return redirect(url_for('student_logged'))

            else:
                return redirect(url_for('login_post'))
    return render_template('login.html')

# this is to logout the user
@app.route('/my-link/')
def my_link():
    #  pop the user fro the current session then redirect to login
    session.pop('user_id', None)
    return redirect(url_for('login_post'))


if __name__ == '__main__':
    app.run(debug=True)
