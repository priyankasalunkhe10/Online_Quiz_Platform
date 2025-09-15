from rest_framework import serializers
from .models import Quiz, Question, Choice, QuizAttempt, StudentAnswer

class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ['id', 'text', 'is_correct']

class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['id','quiz', 'text','qtype','marks','order', 'choices']

class QuizSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Quiz
        fields = ['id', 'title', 'description', 'duration','is_active','created_by','created_at']

class QuizDetailSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Quiz
        fields = ["id", "title", "description", "duration_minutes", "is_active", "questions"]

class StudentAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentAnswer
        fields = ["question", "selected_choice_ids", "text_answer"]

class QuizAttemptSerializer(serializers.ModelSerializer):
    answers = StudentAnswerSerializer(many=True, write_only=True, required=False)

    class Meta:
        model = QuizAttempt
        fields = ["id", "quiz", "student", "start_time", "completed", "completed_at", "score", "answers"]
        read_only_fields = ["start_time", "completed", "completed_at", "score"]

    def create(self, validated_data):
        answers_data = validated_data.pop("answers", [])
        attempt = QuizAttempt.objects.create(**validated_data)
        for ans in answers_data:
            StudentAnswer.objects.create(attempt=attempt, **ans)
        return attempt
