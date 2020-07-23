import discord
from discord.ext import commands
from bot_methods import *

client = commands.Bot(command_prefix = '!')

@client.event
async def on_ready():
    print('Bot is ready')
    print(f'Active on {[g.name for g in client.guilds]}')
    load()

@client.command()
async def debug(ctx):
    if user_has_bot_permissions(ctx.author):
        view()
        msg = 'Content shown in server\'s shell'
    else:
        msg = 'You can\'t to that'
    await ctx.send(msg)

@client.command()
async def save(ctx):
    save_info()
    
# @client.command()
# async def add(ctx, course_code):
#     if user_has_bot_permissions(ctx.author):
#         created = add_course_to_guild(course_code, global_course=False, guild=ctx.guild)
#         msg = f'{course_code}\'s waitlist created.' if created else f'{course_code} already has a waitlist'
#         msg += f'\nStudents can join it by typing  **!join {course_code} <their id>**'
#     else:
#         msg = 'You can\'t do that'
#     await ctx.send(msg)

@client.command()
async def add(ctx, course_code):
    if user_has_bot_permissions(ctx.author):
        created = add_course_to_guild(course_code, global_course=True)
        msg = f'{course_code}\'s waitlist created for all TEC servers.' if created else f'{course_code} already has a waitlist'
        msg += f'\nStudents can join it by typing  **!join {course_code} <their id>**'
    else:
        msg = 'You can\'t do that'
    await ctx.send(msg)

@client.command()
async def join(ctx, course_code, student_id):
    if user_has_bot_permissions(ctx.author):
        result = add_student_to_course(student_id, course_code, ctx.guild)
        if result is AddStudentResult.SUCCESS:
            msg = f'{student_id} is now on the waitlist for {course_code}!'
        elif result is AddStudentResult.NO_COURSE:
            msg = f'{course_code} has no waitlist'
        elif result is AddStudentResult.REPEATED_ID:
            msg = f'{student_id} is already on that waitlist'
        else:
            msg = f'Error joining {course_code}\'s waitlist'
    else:
        msg = 'You can\'t do that'
    await ctx.send(msg)

@client.command(aliases=['list'])
async def _list(ctx, course_code):
    waitlist, result = get_course_waitlist(course_code)
    if result == GetWaitlistResult.SUCCESS:
        if len(waitlist) == 0:
            msg = f'The waitlist for {course_code} is empty'
        else:
            msg = f'{course_code}\'s waitlist:'
            for student in waitlist:
                msg += f'\n\t{student}'
    elif result == GetWaitlistResult.NO_COURSE:
        msg = f'{course_code} has no waitlist'
    await ctx.send(msg)

client.run(open('bot_secret.txt', 'r').read())