import datetime
from google.cloud import firestore

db = firestore.Client()

courses = db.collection('cursos')

def course_exists(code):
    doc = courses.document(code).get()
    return doc.exists

def create_course(code):
    courses.document(code).set({})
    return True

def add_to_course(student, major, code):
    if not course_exists(code):
        return 0 # no waitlist with code
    if student_in_course(student, code):
        return 1 # student already in waitlist
    data = {
        student: {
            u'carrera': major,
            u'date': datetime.datetime.now(),
            u'done': False
        }
    }
    courses.document(code).set(data, merge=True)
    return 2 # success

def student_in_course(student, course):
    doc = courses.document(course).get()
    if doc.exists:
        if student in doc.to_dict():
            return True
        else:
            return False
    return False

def delete_student_from_course(student, course):
    course_ref = courses.document(course)
    course_ref.update({
        student: firestore.DELETE_FIELD
    })

def mark_student_done(student, course):
    if not course_exists(course):
        return 0
    if not student_in_course(student, course):
        return 1
    course_ref = courses.document(course)
    course_ref.update({
        f'{student}.done': True
    })
    return 2
