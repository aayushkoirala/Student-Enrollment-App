from enum import unique
from flask import Flask, render_template, jsonify, request, redirect
import json
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder='.')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
db = SQLAlchemy(app)


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    # teachers = db.relationship("Teachers", back_populates="Users")
    students = db.relationship("Students", back_populates="Users")
    
    def __repr__(self) -> str:
        return '<User %r>' % self.username

class Teachers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'))
    user = db.relationship("Users", back_populates="Users")
    classes = db.relationship("Classes")
    
    def __repr__(self) -> str:
        return '<User %r>' % self.name
    
class Students(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'))
    user = db.relationship("Users", back_populates="Users")
    
    def __repr__(self) -> str:
        return '<User %r>' % self.name

Enrollment = db.Table('Enrollment',
                        db.Column('class_id', db.Integer, db.ForeignKey('Classes.id')),
                        db.Column('student_id', db.Integer, db.ForeignKey('Students.id'))
                        )

class Classes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Course_Name = db.Column(db.String(80), unique=True, nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('Teachers.id'))
    Num_enrolled = db.Column(db.Integer, unique=False, nullable=False)
    capacity = db.Column(db.Integer, unique=False, nullable=False)
    day_time = db.Column(db.String(80), unique=False, nullable=False)
    students = db.relationship("Students", secondary=Enrollment)
    def __repr__(self) -> str:
        return '<User %r>' % self.Course_Name
user1 = Users(username='potato', password='12345')
student1 = Students(name='Yoan')
student1.user_id.append(user1)
db.session.add(user1)
db.session.add(student1)

db.session.commit()

# class1.subscribers.append(student1)
# db.session.commit()