from app.models import *

f = open('questions', 'rU')

for question in f.readlines():

    new_question = Question(language='EN', text=question.split('/')[0], group=question.split('/')[1][0])
    new_question.save()
    print question.split('/')