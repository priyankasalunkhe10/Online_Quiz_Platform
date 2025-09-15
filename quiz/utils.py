from django.utils import timezone
from .models import Choice

def score_attempt(attempt):
    total_marks = 0
    obtained_marks = 0

    for ans in attempt.answers.all():
        question = ans.question
        total_marks += question.marks
        if question.qtype in ("single", "multi"):
            correct_ids = set(Choice.objects.filter(question=question, is_correct=True).values_list("id", flat=True))
            picked_ids = set(ans.selected_choice_ids or [])
            if picked_ids == correct_ids:
                ans.is_correct = True
                ans.marks_awarded = question.marks
            else:
                ans.is_correct = False
                ans.marks_awarded = 0
        elif question.qtype == "text":
            # Basic check: exact match with first correct choice text
            correct_choice = Choice.objects.filter(question=question, is_correct=True).first()
            if correct_choice and ans.text_answer:
                ans.is_correct = correct_choice.text.strip().lower() in ans.text_answer.strip().lower()
                ans.marks_awarded = question.marks if ans.is_correct else 0
        ans.save()
        obtained_marks += ans.marks_awarded or 0

    attempt.score = obtained_marks
    attempt.completed = True
    attempt.completed_at = timezone.now()
    attempt.save()

    return attempt.score, total_marks
