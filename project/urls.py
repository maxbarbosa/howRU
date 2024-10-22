from app.views import *
from django.urls import path

urlpatterns = [
    path('login/aluno', login_aluno, name='login_aluno'),
    path('login/funcionario/', login_funcionario, name='login_funcionario'),
    
    path('aluno/home', aluno_home, name='aluno_home'),
    path('home/funcionario/', funcionario_home, name='funcionario_home'),
    
]