import gspread
from oauth2client.service_account import ServiceAccountCredentials
from bot_internals import *

# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

# Find a workbook by name and open the first sheet
# Make sure you use the right name here.
workspace = client.open("Inscripciones AD2020 Waitlist Discord")
sheet = workspace.sheet1

#workspace.share('juanpramoss98@gmail.com', perm_type='user', role='reader')

def make_formatted_list(waitlist, done):
    vals = []
    for i, val in enumerate(waitlist):
        if done[i]:
            val = f'DONE - {val}'
        vals.append(val)
    return [[y] for y in vals]


def export_to_sheets():
    sheet.clear()
    course_codes = get_all_courses()
    sheet.insert_row(course_codes)

    for i in range(len(course_codes)):
        course_code = course_codes[i]
        course = get_course_waitlist(course_code)
        waitlist = course[course_code]
        done = course['done']
        initpos = gspread.utils.rowcol_to_a1(2,i+1)
        finalpos = gspread.utils.rowcol_to_a1(2+len(waitlist),i+1)
        ran = f'{initpos}:{finalpos}'
        formatted = make_formatted_list(waitlist, done)
        sheet.update(ran,formatted)
