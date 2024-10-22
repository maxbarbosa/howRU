from app.views import *
from django.urls import path

urlpatterns = [
    path('login/aluno', login_aluno, name='login_aluno'),
    path('login/funcionario/', login_funcionario, name='login_funcionario'),
    
    path('aluno/home', aluno_home, name='aluno_home'),
    path('funcionario/home', funcionario_home, name='funcionario_home'),
    path('funcionario/listar_alunos', listar_alunos, name='listar_alunos'),
    path('funcionario/listar_refeicoes', listar_refeicoes, name='listar_refeicoes'),
]