#imports
import discord
import os
from replit import db
from keep_alive import keep_alive
from difflib import SequenceMatcher

client = discord.Client()

numbers = '0123456789'
punctuation = ',\'\".!?`:;()@#$%^&*[]{}|\\/<>~_-+='


def FAQ(question):
    message = "We currently have no answer to that question."
    index = find_question(question)

    #if the question is already present in the database
    if index != -1 and len(db["answers"]) > index:
        answer = db["answers"][index]

        #if answer is present in the database
        if answer != None:
            return answer

    #if there are entries in the databse
    if len(db["questions"]) > 0:
        similar = find_similar_questions(question)
        s = 1

        #loops until an answer with enough similarity is found, or until all similar questions have been covered
        while s >= 0.5:
            s, i = find_greatest_similarity(similar)

            #if a similar question is found
            if s >= 0.5:
                answer = db["answers"][i]

                #if the answer is non existant then reset and loop again
                if answer == None:
                    similar[i] = 0

                #otherwise return the answer and update the database
                else:
                    if index == -1:
                        add_question(question)
                        index = len(db["questions"]) - 1
                        add_answer(answer)
                    else:
                        db["answers"][index] = answer
                    return answer
    #otherwise the answer is not present

    #if the question is not in the database
    if index == -1:
        add_question(question)
        add_answer(None)
        index = len(db["questions"]) - 1
    message += " Here is your question's ID: " + str(index)
    return message


def find_greatest_similarity(similarities):
    pos = 0
    largest = similarities[0]
    for i in range(len(similarities)):
        if largest < similarities[i]:
            largest = similarities[i]
            pos = i
    return largest, pos


def find_question(question):
    for i in range(len(db["questions"])):
        question = cleanup_characters(question)

        DBquestion = db["questions"][i]
        DBquestion = cleanup_characters(DBquestion)

        if question.lower() == DBquestion.lower():
            return i
    return -1


def find_similar_questions(question):
    similarities = []
    for q in db["questions"]:
        question = cleanup_characters(question).lower()
        DBquestion = cleanup_characters(q).lower()
        s1 = SequenceMatcher(None, question, DBquestion).ratio()
        s2 = SequenceMatcher(None, DBquestion, question).ratio()
        if s1 > s2:
            s = s1
        else:
            s = s2
        if s != 1:
            similarities.append(s)
        else:
            similarities.append(0)
    return similarities


#clean up spaces and punctuation
def cleanup_characters(string):
    return remove_extra_spaces(remove_punctuation(string))


def remove_punctuation(string):
    newStr = ""
    present = False
    for l in range(len(string)):
        present = False
        for i in punctuation:
            if string[l] == i:
                present = True
        if present == False:
            newStr += string[l]
    return newStr


def remove_extra_spaces(string):
    newStr = ""
    count = 0
    for i in range(len(string)):
        if string[i] == ' ':
            count += 1
            if count < 2:
                newStr += string[i]
        else:
            newStr += string[i]
            count = 0
    return newStr


#add question to list of questions
def add_question(question):
    if "questions" in db.keys():
        questions = db["questions"]
        questions.append(question)
        db["questions"] = questions
    else:
        db["questions"] = []


#add answer to list of answers
def add_answer(answer):
    if "answers" in db.keys():
        answers = db["answers"]
        answers.append(answer)
        db["answers"] = answers
    else:
        db["answers"] = []


#find index
def get_ID(message):
    digits = extract_digits(message)
    return calculate_ID(digits)


def extract_digits(message):
    i = 0
    digits = []
    done = False
    while done == False:
        done = True
        for num in numbers:
            if message[i] == num:
                done = False
                digits.append(int(num))
        i += 1
    return digits


def calculate_ID(digits):
    ID = 0
    for l in range(len(digits)):
        num = digits[l]
        power = len(digits) - l - 1
        position = 10**power
        ID += num * position
    return ID


def extract_answer(message):
    i = 0
    done = False
    while done == False:
        done = True
        for num in numbers:
            if message[i] == num:
                done = False
        i += 1
    return message[i:]


#login
@client.event
async def on_ready():
    print('We have logged in as user {0.user}'.format(client))
    await client.change_presence(activity=discord.Activity(
        type=discord.ActivityType.watching, name="for ?FAQ"))


#find the function being called, and send message back
@client.event
async def on_message(message):

    if message.author == client.user:
        return

    if message.content.startswith('?Reset'):
        db["questions"] = []
        db["answers"] = []
        await message.channel.send("The database has been reset")

    if message.content.startswith("?DeleteIndex"):
        text = message.content[13:] + " "
        index = get_ID(text) - 1
        if index < len(db["questions"]):
            db["questions"].pop(index)
            db["answers"].pop(index)
            await message.channel.send("Index " + str(index + 1) + " deleted.")
        else:
            await message.channel.send(
                "The entry at the index you provided does not exist")

    if message.content.startswith("?All"):
        if len(db["questions"]) == 0:
            await message.channel.send("The database is empty")
        else:
            for i in range(len(db['questions'])):
                if db["answers"][i] == None:
                    answer = "N/A"
                else:
                    answer = db["answers"][i]
                await message.channel.send(
                    str(i + 1) + ". " + db['questions'][i] + ":\n" + answer)

    if message.content.startswith('?FAQQ'):
        question = message.content[6:]
        await message.channel.send(FAQ(question))

    if message.content.startswith('?FAQA'):
        text = message.content[6:]
        index = get_ID(text)
        answer = extract_answer(text)
        db["answers"][index] = answer
        await message.channel.send("The answer has been updated")

    if message.content.startswith('?Help'):
        await message.channel.send(
            "Commands and guides can be found on the website:")
        await message.channel.send("https://aariv428.wixsite.com/faqbot/help")


keep_alive()
client.run(os.getenv('TOKEN'))