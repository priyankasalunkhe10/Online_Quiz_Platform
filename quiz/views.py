from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.http import JsonResponse
from .models import Quiz, Question, Option, Result, User
from django.utils import timezone

# ---------------- Admin API ----------------

# ---------- Authentication Views ----------
def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if user.is_admin:
                return redirect("admin_dashboard")
            else:
                return redirect("student_dashboard")
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "quiz/login.html")


def logout_view(request):
    logout(request)
    return redirect("login")


# ---------- Admin Views ----------
@login_required
def admin_dashboard(request):
    if not request.user.is_admin:
        return redirect("student_dashboard")

    quizzes = Quiz.objects.filter(created_by=request.user)
    return render(request, "quiz/admin_dashboard.html", {"quizzes": quizzes})


@login_required
def create_quiz(request):
    if request.method == "POST" and request.user.is_admin:
        title = request.POST["title"]
        description = request.POST.get("description", "")
        duration = int(request.POST["duration"])

        quiz = Quiz.objects.create(
            title=title, description=description, duration=duration, created_by=request.user
        )
        messages.success(request, "Quiz created successfully!")
        return redirect("admin_dashboard")

    return render(request, "quiz/create_quiz.html")


# ---------- Student Views ----------
@login_required
def student_dashboard(request):
    quizzes = Quiz.objects.all()
    return render(request, "quiz/student_dashboard.html", {"quizzes": quizzes})


@login_required
def take_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.questions.prefetch_related("options").all()

    if request.method == "POST":
        score = 0
        for question in questions:
            selected_option_id = request.POST.get(str(question.id))
            if selected_option_id:
                selected_option = Option.objects.get(id=selected_option_id)
                if selected_option.is_correct:
                    score += 1

        # Save result
        Result.objects.create(
            student=request.user,
            quiz=quiz,
            score=score,
            submitted_at=timezone.now(),
        )
        return render(request, "quiz/result.html", {"score": score, "quiz": quiz})

    return render(request, "quiz/take_quiz.html", {"quiz": quiz, "questions": questions})
