from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import loader

import json
import csv


from .models import Question


def load_data_deprecated(quiz_id):
    filename = "static/quiz/quiz-" + str(quiz_id) + ".csv"
    
    quiz = []
    
    with open(filename) as f:
        reader = csv.reader(f)
        for row in reader:
            created = Question(
                nominative=row[0],
                inessive=row[1]
                )
            quiz.append(created)
    return quiz


def num2ls(num):
    ls = []
    i = 1
    while num > 0:
        num, r = divmod(num, 2)
        if r == 1: ls.append(i-1)
        i += 1
    return ls


def load_data(quiz_id):
    filename = "static/quiz/questions.csv"
    
    quiz = []
    
    with open(filename) as f:
        reader = csv.reader(f)
        for row in reader:
            created = Question(
                nominative=row[0],
                inessive=row[1]
                )
            quiz.append(created)
            
    idx = num2ls(quiz_id)
    
    return [ quiz[i] for i in idx ]
    




def index(request, session_id="test", quiz_id=1, round_id=1):
    
    if request.method == 'POST':
        print("received POST")
        # Retrieve JSON data from request body
        #data = request.POST.get('data')  # Assuming 'data' is the key for JSON object
        data = json.loads(request.body)
        print(data)
        
        # Process the JSON data
        # For demonstration, let's just echo the received data back to the client
        
        
        if round_id == 1:
            path = '/'.join(["ai_process/index", session_id, str(quiz_id)] )
            print(path)
            return redirect(path)
        else:
            return redirect("conclusion:index")
        
        #return JsonResponse({'received_data': data})
    
    else:
        # Load questions    
        questions = load_data(quiz_id)
        total_questions = len(questions)
        
        submit_button_text = "Get help from the AI teacher" if round_id == 1 else "Continue"
        
        template = loader.get_template("evaluation/index.html")
        
        context = {
            'questions': questions,
            'total_questions': total_questions,
            'submit_button_text': submit_button_text,
            'session_id': session_id,
            'quiz_id': quiz_id, 
            'round_id': round_id
        }
        return HttpResponse(template.render(context, request))

