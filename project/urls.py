from app.views import *
from django.urls import path

urlpatterns = [
    path('login/aluno', login_aluno, name='login_aluno'),
    path('aluno/home', aluno_home, name='aluno_home'),
]