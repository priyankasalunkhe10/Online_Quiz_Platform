from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Quiz(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField(blank = True)
    time_limit = models.PositiveIntegerField(help_text='time limit in minutes')
    created_by = models.ForeignKey(User,on_delete = models.CASCADE, related_name="quizzes_created")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class Question(models.Model):
    ANSWER_CHOICES = [('A','A'),('B','B'),('C','C'),('D','D')]
    quiz = models.ForeignKey(Quiz, related_name='questions', on_delete=models.CASCADE)
    question_text = models.TextField()
    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    option_d = models.CharField(max_length=255)
    correct_answer = models.CharField(max_length=1, choices=ANSWER_CHOICES)

    def __str__(self):
        return self.question_text[:50]

class StudentScore(models.Model):
    student = models.ForeignKey(User,on_delete=models.CASCADE,related_name="quiz_scores")
    quiz = models.ForeignKey(Quiz,on_delete=models.CASCADE,related_name="scores")
    score = models.FloatField()
    total = models.PositiveIntegerField()
    taken_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} - {self.quiz.title} - {self.score}/{self.total}"
