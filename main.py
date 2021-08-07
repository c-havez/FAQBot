import discord
import os
import requests
from replit import db
#from keep_alive import keep_alive

client = discord.Client()

# def FAQ(question):
#   QinDB = find_question(question)
#   if QinDB == True:
#     AinDB = find_answer(question)
#   else:
#     update_questions(question, answer)

# def find_question(question):
#   for i in questions:
#     if question == i:
#       return True
#   return False

# def update_questions():
#   yes = "y"
#   #if "questions" in db.key():
#     #questions = db["questions"]
#     #questions.append(question_message)

# def find_answer(question):


#def update_question(question):
  # if "question" in db.keys():



@client.event
async def on_ready():
  print('We have logged in as user {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return
  
  if message.content.startswith('?FAQ'):
    question = message.content[4:]
    await message.channel.send(question)


#keep_alive()
client.run(os.getenv('TOKEN'))