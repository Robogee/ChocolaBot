import discord
import pymongo
import json
from discord.ext import commands,tasks

DBCONNECT = ''
TOKEN = ''
PREFIX = 'c.'

intents = discord.Intents.default()
chocola = commands.Bot(command_prefix=PREFIX,intents=intents)
mongobongo = pymongo.MongoClient(DBCONNECT)

taskdb = mongobongo["taskdb"]
daily = taskdb["daily"]

@chocola.event
async def on_ready():
    print("Chocola is up and running!")
    await chocola.change_presence(activity=discord.Game('Learning new tricks!'))

@chocola.command()
async def test(ctx,arg):
    await ctx.send(arg)

@chocola.command()
async def add(ctx,*,args):
    if len(args) == 0:
        raise commands.CommandError("Insufficient arguments!")
    else:
        new = await add_parse(args)
        new_id = daily.insert_one(new)
        await ctx.channel.send("Successfully added task!")

@chocola.command()
async def list(ctx):
    id = 1
    for task in daily.find():
        task_message = await parse_task(task,id)
        await ctx.channel.send(task_message)
        id += 1

@chocola.command()
async def clear(ctx):
    daily.clear()

@chocola.command()
async def mention(ctx):
    await ctx.channel.send("Hello {}".format(ctx.message.author.mention))

@chocola.command()
async def ohayo(ctx):
    await ctx.channel.send("おはようございます-にゃあ")

#Error Handling
# @add.error
# async def add_error(ctx,CommandError):
#     await ctx.channel.send("Give me something to add-nya!")

#Internal Handling Functions
async def add_parse(message):
    task = {}
    params = message.split('-')

    task['task'] = params[0]
    if (len(params) > 1):
        task['urgent'] = True
    else:
        task['urgent'] = False

    return task

async def parse_task(task,id):
    is_urgent = ""
    if task['urgent'] == False:
        is_urgent = "not "
    message = "Daily Task {}: {}, is {}urgent".format(id,task['task'],is_urgent)
    return message

chocola.run(TOKEN)
