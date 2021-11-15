from app import *
query_student = Students.query.filter_by(user_id=1).first()
query = db.session.query(Enrollment).all()
list_classes = []
for cls in query:
    if cls[1] == query_student.id:
        list_classes.append(cls)
        json_data = json.loads("{}")
for cls in list_classes:
    current_cls = Classes.query.filter_by(id=cls[0]).first()
    current_teacher = Teachers.query.filter_by(id = current_cls.teacher_id).first()
    json_data.update({cls[0]:{"class_name":current_cls.course_name,"time":current_cls.day_time, "teacher_name":current_teacher.name, "Enrolled":current_cls.num_enrolled}})
print(json_data)
