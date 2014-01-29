from app.models import *

f = open('questions', 'rU')

for question in f.readlines():

    #new_question = Question(english=question.split('/')[0], group=question.split('/')[1][0])
    #new_question.save()
    #print question.split('/')

    split = question.split('\\')
    if len(split) > 2:
        print split
        split_slice = split[1:-1]
        new_question = Question(english=split[0], group=split[-1])
        new_question.save()
        for option in split_slice:
            new_option = Option(english=option)
            new_option.save()
            new_question.options.add(new_option)
    else:
        new_question = Question(english=question.split('\\')[0], group=question.split('\\')[1][0])
        new_question.save()