import gspread
from oauth2client.service_account import ServiceAccountCredentials
from bot_internals import *

# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

# Find a workbook by name and open the first sheet
# Make sure you use the right name here.
workspace = client.open("New spreadsheet from python")
sheet = workspace.sheet1

#workspace.share('juanpramoss98@gmail.com', perm_type='user', role='reader')

def export_to_sheets():
    sheet.clear()
    course_codes = get_all_courses()
    sheet.insert_row(course_codes)

    for i in range(len(course_codes)):
        course_code = course_codes[i]
        waitlist = get_course_waitlist(course_code)
        initpos = gspread.utils.rowcol_to_a1(2,i+1)
        finalpos = gspread.utils.rowcol_to_a1(2+len(waitlist),i+1)
        ran = f'{initpos}:{finalpos}'
        formatted = [[y] for y in waitlist]
        sheet.update(ran,formatted)


