from app.models import *

f = open('questions', 'rU')

for question in f.readlines():

    new_question = Question(language='EN', text=question)
    new_question.save()