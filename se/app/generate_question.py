import random

from app.models import *

from django.templatetags.static import static

def generate_question(index):
    questions = Question.objects.filter()
    index = int(index)
    if index >= len(Question.objects.filter()):
        return 'Done'
    if index <= 3:
        question = questions[index].text
        print questions[index]
        index = index + 1
        return question
    else:
        list_of_questions = []
        f = 0
        while f < 3:
            question = questions[index].text
            list_of_questions.append(question)
            index = index + 1
            f = f + 1
        return list_of_questions
    #index = random.randint(0, (len(questions) - 1))
    # question = questions[index]
    # return question
