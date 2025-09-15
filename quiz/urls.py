from django.urls import path
from . import views

urlpatterns = [
    path("", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),

    # Admin
    path("admin-dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("create-quiz/", views.create_quiz, name="create_quiz"),

    # Student
    path("student-dashboard/", views.student_dashboard, name="student_dashboard"),
    path("quiz/<int:quiz_id>/", views.take_quiz, name="take_quiz"),
]
