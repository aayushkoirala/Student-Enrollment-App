from enum import unique
from flask import Flask, render_template, jsonify, request, redirect
import json
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder='.')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
db = SQLAlchemy(app)


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
                        db.Column('student_id', db.Integer, db.ForeignKey('students.id'))
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

@app.route('/student/<string:username>,<string:password>', methods=['GET'])
def verifyCredentials(username, password):
    user = Users.query.all()
    for row in user:
        if row.username == username and row.password == password:
            id = row.id
            try:
                teacher = Teachers.query.filter_by(user_id=id).first()
                return teacher.name
            except:
                student = Students.query.filter_by(user_id=id).first()
                return student.name
            
    return 'False'

if __name__ == '__main__':
    app.run(debug=True)