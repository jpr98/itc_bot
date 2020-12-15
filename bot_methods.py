from enum import Enum, auto
from firestore import *

def user_has_bot_permissions(user):
    return user_has_roles(["admin", "asistente"], user)


def add_course_waitlist(code):
    code = code.upper()
    if course_exists(code):
        return False
    return create_course(code)


class AddStudentResult(Enum):
    SUCCESS = auto()
    NO_COURSE = auto()
    REPEATED_ID = auto()

def add_student_to_course(student_id, course_code, guild):
    course_code = course_code.upper()
    student_id = student_id.upper()
    result = add_to_course(student_id, guild.name, course_code)
    if result == 0:
        return AddStudentResult.NO_COURSE
    elif result == 1:
        return AddStudentResult.REPEATED_ID
    else:
        return AddStudentResult.SUCCESS


class MarkStudentDoneResult(Enum):
    SUCCESS = auto()
    NO_COURSE = auto()
    NO_STUDENT = auto()

def mark_student_as_done_in_course(student_id, course_code):
    course_code = course_code.upper()
    student_id = student_id.upper()
    result = mark_student_done(student_id, course_code)
    if result == 0:
        return MarkStudentDoneResult.NO_COURSE
    elif result == 1:
        return MarkStudentDoneResult.NO_STUDENT
    else:
        return MarkStudentDoneResult.SUCCESS


def remove_student_from_course(student_id, course_code):
    course_code = course_code.upper()
    student_id = student_id.upper()
    delete_student_from_course(student_id, course_code)


############ VOICE QUEUE METHODS #############
queue_dict = {}

def add_to_queue_in_guild(user, guild):
    guild_id = guild_bot_id(guild)
    validate_guild_in_dict(guild_id)
    if user in queue_dict[guild_id]:
        return False
    queue_dict[guild_id].append(user)
    return True


def leave_from_queue_in_guild(user, guild):
    guild_id = guild_bot_id(guild)
    validate_guild_in_dict(guild_id)
    if user in queue_dict[guild_id]:
        queue_dict[guild_id].remove(user)


def get_next_from_queue_in_guild(assistant, guild):
    guild_id = guild_bot_id(guild)
    validate_guild_in_dict(guild_id)
    next_user = queue_dict[guild_id][0]
    queue_dict[guild_id].remove(next_user)
    return next_user


def get_guild_queue(guild):
    """ Use this as read-only
    """
    guild_id = guild_bot_id(guild)
    validate_guild_in_dict(guild_id)
    return queue_dict[guild_id]


def eraseQueue(guild):
    g = guild_bot_id(guild)
    queue_dict[g].clear()


def guild_bot_id(guild):
    return f'{guild.name}_{guild.id}'


def user_has_roles(roles, user):
    for role in roles:
        if role in [r.name.lower() for r in user.roles]:
            return True
    return False


def validate_guild_in_dict(guild_id):
    if guild_id not in queue_dict:
        queue_dict[guild_id] = []