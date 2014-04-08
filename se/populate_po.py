# App specific import
from app.models import *

f = open('questions_po', 'rU')

i = 1

for question in f.readlines():

    split = question.split('\\')
    if len(split) > 3:
        split_slice = split[1:-2]
        print split
        new_question = Question.objects.get(id=i)
        new_question.polish = split[0]
        new_question.save()
        for option in split_slice:
            new_option = Option(polish=option)
            new_option.save()
            new_question.options.add(new_option)
    else:
        new_question = Question.objects.get(id=i)
        new_question.polish = split[0]
        new_question.save()
    i = i + 1