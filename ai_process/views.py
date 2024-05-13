from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
from django.template import loader
from django.conf import settings

import json

from .ai import ai



def index(request, session_id="test", quiz_id=1, predictions="", recommendations=""):
    print("loading index")
    
    if request.method == 'POST':
        print("-- From POST")
        data = json.loads(request.body)
        questions = data['questions']
        answers = data['answers']
        correct_answers = data['correct_answers']
        
        results = { 'X': questions, 'Y': answers }
        
        # Loading the AI:
        CB_path = "static/cards/cards.csv"
        
        teacher = ai.AI_Teacher(CB_path, questions, correct_answers)
        
        teacher.analyze_results(results)
        
        print(teacher.inference.probas_cb)
        print(teacher.inference.probas_dist)
        print(teacher.inference.proba_harmony)
        
        
        # Prediction:
        
        predicted_cases = teacher.predict_CB(settings.N_WORDS_PREDICTED)
        #recommendations = teacher.give_recommendations(settings.N_RECOMMENDATIONS)
        
        predictions = '-'.join([str(x) for x in predicted_cases])
        
        if predictions == '': predictions = '0'
        
        
        # Recommendation:
        recommended_cards = teacher.give_recommendations(settings.N_RECOMMENDATIONS, predicted_cases)
        recommendations = '-'.join([str(x) for x in recommended_cards])
        
        print(session_id)
        
        print("redirecting")
        return redirect('ai_process:display_results', 
                        session_id = session_id, 
                        quiz_id = quiz_id, 
                        predictions = predictions, 
                        recommendations = recommendations)
    else:
        print("not POST")
        print(predictions, recommendations)
        template = loader.get_template("ai_process/index.html")
        context = {'predictions': _format_lists_from_concatenation(predictions, '-'), 
                   'recommendations': _format_lists_from_concatenation(recommendations, '-') }
        return HttpResponse(template.render(context, request))
    

def _format_lists_from_concatenation(concatenated_L: str, delimiter: str):
    L = concatenated_L.split(delimiter)
    if len(L) == 1:
        return L[0]
    return ', '.join(L[:-1]) + ' and ' + L[-1] 
    

    
def display_results(request, session_id="test", quiz_id=1, predictions="", recommendations=""):
    print("Display results")
    template = loader.get_template("ai_process/index.html")
    context = {'predictions': _format_lists_from_concatenation(predictions, '-'), 
               'recommendations': _format_lists_from_concatenation(recommendations, '-'),
               'session_id': session_id, 
               'quiz_id': quiz_id}
    return HttpResponse(template.render(context, request))