import discord
from discord.ext import commands
from bot_methods import *

client = commands.Bot(command_prefix='!')


@client.event
async def on_ready():
    print('Bot is ready')
    print(f'Active on {[g.name for g in client.guilds]}')


@client.event
async def on_member_join(member):
    msg = f'Bienvenido a {member.guild}'
    msg += '\nPara facilitar este proceso te recuerdo algunas reglas'
    msg += '\n\t1. En el canal de fila de asistencia puedes llamar el comando !join para que te atiendan de manera personal'
    msg += '\n\t2. Utiliza los canales de texto correspondientes para aclarar dudas'
    msg += '\n\t3. Recuerda que este proceso es nuevo para todos, se paciente'
    msg += '\nEspero que esta herramienta te ayude en el proceso de inscripciones :)'
    await member.send(msg)


############ HELPER COMMANDS #############
@commands.has_any_role("admin", "asistente")
@client.command(brief="Elimina n lineas del chat")
async def clear(ctx, amount=10):
    if user_has_bot_permissions(ctx.author):
        await ctx.channel.purge(limit=amount)
    else:
        await ctx.send('You can\'t do that')


############ COURSE QUEUE COMMANDS #############
@commands.has_any_role("admin", "asistente")
@client.command(brief="Crea una fila de espera de una materia")
async def add(ctx, course_code):
    if user_has_bot_permissions(ctx.author):
        created = add_course_waitlist(course_code)
        msg = f'{course_code}\'s waitlist created for all TEC servers.' if created else f'{course_code} already has a waitlist'
        msg += f'\nAsistentes can add students by typing **!join_waitlist {course_code} <their id>**'
    else:
        msg = 'You can\'t do that'
    await ctx.send(msg)


@commands.has_any_role("admin", "asistente")
@client.command(brief="Añade una matrícula a la fila de espera de una materia")
async def join_waitlist(ctx, course_code, student_id):
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


@commands.has_any_role("admin", "asistente")
@client.command(brief="Elimina un alumno de una lista de espera")
async def leave_waitlist(ctx, course_code, student_id):
    if user_has_bot_permissions(ctx.author):
        remove_student_from_course(student_id, course_code)
        msg = 'Done'
    else:
        msg = 'You can\'t do that'
    await ctx.send(msg)


@commands.has_any_role("admin", "asistente")
@client.command(brief="Marca como listo a un alumno")
async def done(ctx, course_code, *student_id):
    if user_has_bot_permissions(ctx.author):
        msg = ''
        for student in student_id:
            result = mark_student_as_done_in_course(student, course_code)
            if result is MarkStudentDoneResult.NO_COURSE:
                msg = f'{course_code} has no waitlist'
                break
            elif result is MarkStudentDoneResult.NO_STUDENT:
                msg += f'{student} not in waitlist for {course_code}\n'
            elif result is MarkStudentDoneResult.SUCCESS:
                msg += f'{student} - done\n'
    else:
        msg = 'You can\'t do that'
    await ctx.send(msg)
    

############ VOICE QUEUE COMMANDS #############
@commands.has_any_role("admin", "asistente")
#  TODO: validate asistente in voice channel, index out of range
@client.command(brief="Pasa al siguiente en la fila de asistencia")
async def next(ctx):
    if user_has_bot_permissions(ctx.author):
        next_user = get_next_from_queue_in_guild(ctx.author, ctx.guild)
        chan = str(ctx.message.author.voice.channel)
        embed = discord.Embed(title="Por favor pasa a ",
                              description="", color=0x00ff00)
        embed.add_field(name=chan, value=next_user.mention, inline=False)
        await ctx.send(embed=embed)
    else:
        await ctx.send('You can\'t do that')


@client.command(brief="Añade al usuario a la fila de asistencia")
async def join(ctx):
    added = add_to_queue_in_guild(ctx.author, ctx.guild)
    if added:
        queue = get_guild_queue(ctx.guild)
        embed = discord.Embed(title="Lista de Espera",
                              description="Ayuda Inscripciones", color=0x00ff00)
        embed.set_footer(text="inserta el comando **!join**")
        if len(queue) is 0:
            embed.add_field(name="Lista", value="Vacía")
        else:
            embed.add_field(name="Lista", value="\n".join(
                [f'{i+1} {student.mention}' for i, student in enumerate(queue)]), inline=False)
    else:
        embed = discord.Embed(title="Lista de Espera",
                              description="Ayuda Inscripciones", color=0xff0000)
        embed.add_field(name="Ups", value="Ya estas en la lista", inline=False)
    await ctx.send(embed=embed)


@client.command(brief="Remueve al usuario de la fila de asistencia")
async def leave(ctx):
    leave_from_queue_in_guild(ctx.author, ctx.guild)
    queue = get_guild_queue(ctx.guild)
    embed = discord.Embed(title="Lista de Espera",
                          description="Ayuda Inscripciones", color=0xffff00)
    embed.set_footer(text="inserta el comando **!join**")
    if len(queue) is 0:
        embed.add_field(name="Lista", value="Vacía")
    else:
        embed.add_field(name="Lista", value="\n".join(
            [f'{i+1} {student.mention}' for i, student in enumerate(queue)]), inline=False)
    await ctx.send(embed=embed)


@client.command(brief="Muestra la fila de asistencia")
async def list(ctx):
    queue = get_guild_queue(ctx.guild)
    embed = discord.Embed(title="Lista de Espera",
                          description="Ayuda Inscripciones", color=0x00ff00)
    embed.set_footer(text="inserta el comando **!join**")
    if len(queue) is 0:
        embed.add_field(name="Lista", value="Vacía")
    else:
        embed.add_field(name="Lista", value="\n".join(
            [f'{i+1} {student.mention}' for i, student in enumerate(queue)]), inline=False)
    await ctx.send(embed=embed)


@client.command(brief="Vacia la fila de espera")
async def empty(ctx):
    if(user_has_bot_permissions(ctx.author)):
        eraseQueue(ctx.guild)
    else:
        await ctx.send('You can\'t do that')

client.run(open('bot_secret.txt', 'r').read())