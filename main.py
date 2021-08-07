import discord
import os
import requests
from replit import db
#from keep_alive import keep_alive

client = discord.Client()

# for i in range(len(db["questions"])):
#   del db["questions"][i]

# for i in range(len(db["answers"])):
#   del db["answers"][i]
# db["questions"] = []
# db["answers"] = []

# print (db["questions"])

def FAQ(question):
  message = "We currently have no answer to that question"
  index = find_question(question)
  print(db["questions"], db["answers"])
  if index != -1 and len(db["answers"]) > index:
    answer = db["answers"][index]
    if answer != None:
      message = answer
  else:
     add_question(question)
     add_answer(None)
  return message

def find_question(question):
   for i in range (len(db["questions"])):
     if question == db["questions"][i]:
       print(i)
       return i
   return -1

def add_question(question):
  if "questions" in db.keys():
    questions = db["questions"]
    questions.append(question)
    print(questions)
    db["questions"] = questions
  else:
    db["questions"] = [] 

def add_answer(answer):
  if "answers" in db.keys():
    answers = db["answers"]
    answers.append(answer)
    db["answers"] = answers
  else:
    db["answers"] = [] 

def modify_question(question):
  yes = 1

def modify_answer(answer):
  yes = 1

@client.event
async def on_ready():
  print('We have logged in as user {0.user}'.format(client))
  await client.change_presence(activity = discord.Activity(type = discord.ActivityType.watching, name = "for ?FAQ"))

@client.event
async def on_message(message):
  if message.author == client.user:
    return
  
  if message.content.startswith('?FAQ'):
    question = message.content[4:]
    print(FAQ(question))
    await message.channel.send(FAQ(question))

#keep_alive()
client.run(os.getenv('TOKEN'))