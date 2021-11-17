# from app import *
# query_student = Students.query.filter_by(user_id=1).first()
# query = db.session.query(Enrollment).all()
# potential_classes = []
# class_id = []
# for cls in query:
#     if cls[1] == query_student.id:
#         potential_classes.append(cls)
#         class_id.append(cls[0])
#         json_data = json.loads("{}")
# print('--------------')
# print(potential_classes)
# print('--------------')
# all_classes = db.session.query(Classes.metadata.tables['classes']).all()
# for cls in potential_classes:
#     potential_cls = Classes.query.filter_by(id=cls[0]).first()
#     potential_teacher = Teachers.query.filter_by(id = potential_cls.teacher_id).first()
#     json_data.update({cls[0]:{"class_name":potential_cls.course_name,"time":potential_cls.day_time, "teacher_name":potential_teacher.name, "Enrolled":potential_cls.num_enrolled}})
# print(json_data)


from app import *
# query_student = Students.query.filter_by(user_id=1).first()
# query = db.session.query(Enrollment).all()
# potential_classes = []
# class_id = []
# for cls in query:
#     if cls[1] == query_student.id:
#         class_id.append(cls[0])
#         json_data = json.loads("{}")
# print('--------------')
# print(class_id)
# print('--------------')
# all_classes = db.session.query(Classes.metadata.tables['classes']).all()
# for cls in all_classes:
#     if cls[0] not in class_id:
#         potential_cls = Classes.query.filter_by(id=cls[0]).first()
#         potential_teacher = Teachers.query.filter_by(id = potential_cls.teacher_id).first()
#         json_data.update({cls[0]:{"class_name":potential_cls.course_name,"time":potential_cls.day_time, "teacher_name":potential_teacher.name, "Enrolled":potential_cls.num_enrolled}})
# print(json_data)

# cha = db.session.query(Enrollment.metadata.tables['Enrollment']).all()
# print(cha)


    
        
query_student = Students.query.filter_by(user_id=2).first()
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
# print(current_classes)
# print(json_data)

# so i have a list of classes, class 1, class 2, class 3
# and i have a list of classes that i could add class 3, class 4, class 5
# iterate over classes that i could add and then iterate over current classes then see if i can add class on current class and potential class

print(query)
for c in db.session.query(Enrollment).all():
    if c.class_id == 79:
        print(c.grade)
        print(c[2])
        db.session.commit()
print(type(query))


