import random

def generate_question(index):
    f = open('app/static/questions', 'r')
    index = int(index)
    questions = f.readlines()
    if index >= len(questions):
        return 'Done'
    if index <= 3:
        question = questions[index]
        index = index + 1
        return question
    else:
        list_of_questions = []
        f = 0
        while f < 3:
            question = questions[index]
            list_of_questions.append(question)
            index = index + 1
            f = f + 1
        return list_of_questions
    #index = random.randint(0, (len(questions) - 1))
    # question = questions[index]
    # return question
