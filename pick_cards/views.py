from django.http import HttpResponse
from django.template import loader
from django.conf import settings


import uuid
import os
import random

def get_number_of_tests():
    DIR = "static/quiz"
    return len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])


def index(request):
    session_id = uuid.uuid4()
    quiz_id = random.randint(1, get_number_of_tests())
    
    template = loader.get_template("pick_cards/index.html")
    context = {'N_CARDS': settings.N_CARDS,
               'session_id': session_id, 
               'quiz_id': quiz_id }
    return HttpResponse(template.render(context, request))