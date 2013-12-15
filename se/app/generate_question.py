import random

def generate_question():
    f = open('app/static/questions', 'r')
    questions = f.readlines()
    index = random.randint(0, (len(questions) - 1))
    question = questions[index]
    return question