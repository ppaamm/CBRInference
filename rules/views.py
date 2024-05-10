from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.conf import settings
    

def index(request):
    template = loader.get_template("rules/index.html")
    context = {'N_WORDS_TEST': settings.N_WORDS_TEST,
               'N_CARDS': settings.N_CARDS, 
               }
    return HttpResponse(template.render(context, request))