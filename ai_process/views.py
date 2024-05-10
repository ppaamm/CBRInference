from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.conf import settings

import json

from .ai import ai



def index(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        questions = data['questions']
        answers = data['answers']
        correct_answers = data['correct_answers']
        print(questions)
        
        results = { 'X': questions, 'Y': answers }
        
        # Loading the AI:
        CB_path = "static/cards/cards.csv"
        
        teacher = ai.AI_Teacher(CB_path, questions)
        
        teacher.analyze_results(results)
        predicted_cases = teacher.predict_CB(settings.N_WORDS_PREDICTED)
        #recommendations = teacher.give_recommendations(settings.N_RECOMMENDATIONS)
        
        print(predicted_cases)
        
        #text = "Predicted words: " + ", ".join(predicted_cases)
        #print(text)
        
        
        
    return HttpResponse("text")