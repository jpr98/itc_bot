from enum import Enum, auto
from bot_internals import *
from sheets import *

def load():
    load_data()

def save_info():
    save_data()
    export_to_sheets()

def view():
    print(guild_dict)

def user_has_bot_permissions(user):
    return user_has_roles(["admin", "asistente"], user)

def add_course_to_guild(code, global_course=False, guild='global'): # gets global_course parameter to make explicit call
    if global_course:
        guild_id = guild
    else:
        guild_id = guild_bot_id(guild)
    validate_guild_in_dict(guild_id)
    if code in guild_dict[guild_id]['courses']:
        return False
    guild_dict[guild_id]['courses'].append({str(code): []})
    save_info()
    return True

class AddStudentResult(Enum):
    SUCCESS = auto()
    NO_COURSE = auto()
    REPEATED_ID = auto()

def add_student_to_course(student_id, course_code, guild):
    result = add_student_to_course_in_guild(student_id, course_code, guild)
    if result is AddStudentResult.NO_COURSE:
        return add_student_to_global_course(student_id, course_code)
    else:
        return result
        
def add_student_to_course_in_guild(student_id, course_code, guild):
    """This function should only be used internally in bot_methods.py
        It looks for a course in a specific guild and adds the student_id
        to the list
    """
    guild_id = guild_bot_id(guild)
    validate_guild_in_dict(guild_id)
    for course in guild_dict[guild_id]['courses']:
        if course_code in course:
            if student_id in course[course_code]:
                return AddStudentResult.REPEATED_ID
            course[course_code].append(student_id)
            save_info()
            return AddStudentResult.SUCCESS
    return AddStudentResult.NO_COURSE

def add_student_to_global_course(student_id, course_code):
    """This function should only be used internally in bot_methods.py
        It looks for a course in the global list and adds the student_id
        to the list
    """
    validate_guild_in_dict('global')
    for course in guild_dict['global']['courses']:
        if course_code in course:
            if student_id in course[course_code]:
                return AddStudentResult.REPEATED_ID
            course[course_code].append(student_id)
            save_info()
            return AddStudentResult.SUCCESS
    return AddStudentResult.NO_COURSE

class GetWaitlistResult(Enum):
    SUCCESS = auto()
    NO_COURSE = auto()

def get_course_waitlist(course_code):
    for guild in guild_dict:
        for course in guild_dict[guild]['courses']:
            if course_code in course:
                return course[course_code], GetWaitlistResult.SUCCESS
    return [], GetWaitlistResult.NO_COURSE