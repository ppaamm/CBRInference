from django.http import HttpResponse
from django.template import loader
from django.conf import settings


import uuid
import os
import random


def ls2num(ls):
    return sum([pow(2, x) for x in ls])

def get_number_of_tests():
    DIR = "static/quiz"
    return len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])


def get_quiz_id(n_questions):
    num_lines = sum(1 for _ in open('static/quiz/questions.csv'))
    print(num_lines)
    idx = random.sample(range(num_lines), n_questions)
    print(idx)
    print(ls2num(idx))
    return ls2num(idx)
    


def index(request):
    session_id = uuid.uuid4()
    #quiz_id = random.randint(1, get_number_of_tests())
    
    quiz_id = get_quiz_id(settings.N_WORDS_TEST)
    
    template = loader.get_template("pick_cards/index.html")
    context = {'N_CARDS': settings.N_CARDS,
               'session_id': session_id, 
               'quiz_id': quiz_id }
    return HttpResponse(template.render(context, request))