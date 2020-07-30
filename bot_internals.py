import discord
import json
import os

filename = 'bot_data.json'

# Helper functions
def validate_section_in_guild(section, guild_id):
    if section not in guild_dict[guild_id]:
        guild_dict[guild_id][section] = []

def validate_guild_in_dict(guild_id):
    if guild_id not in queue_dict:
        queue_dict[guild_id] = []
    if guild_id not in guild_dict:
        guild_dict[guild_id] = {'courses': []}

def guild_bot_id(guild):
    return f'{guild.name}_{guild.id}'

def user_has_roles(roles, user):
    for role in roles:
        if role in [r.name.lower() for r in user.roles]:
            return True
    return False

def save_data():
    with open(filename, 'w+') as out:
        json.dump(guild_dict, out)

def load_data():
    if not os.path.exists(filename):
        with open(filename, 'w+'): pass
    try:
        with open(filename) as f:
            return json.load(f)
    except:
        return {}

guild_dict = load_data()
queue_dict = {}

def get_all_courses():
    courses = []
    # this could be changed to list comprehension
    for guild in guild_dict:
        for course in guild_dict[guild]['courses']:
            for course_code in course:
                courses.append(course_code)
    return courses

def get_course_waitlist(course_code):
    for guild in guild_dict:
        for course in guild_dict[guild]['courses']:
            if course_code in course:
                return course[course_code]
    return []
