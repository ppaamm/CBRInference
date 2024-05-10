from django.db import models

class Question(models.Model):
    nominative = models.CharField(max_length=100, primary_key=True)
    inessive = models.CharField(max_length=100)

    def __str__(self):
        return f"Question: {self.nominative} -> {self.inessive}"


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    givenAnswer = models.CharField(max_length=100)
    
    
    