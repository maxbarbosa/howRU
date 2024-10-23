from app.views import *
from django.urls import path

urlpatterns = [
    path('', homepage, name='homepage'),
    path('login/aluno', login_aluno, name='login_aluno'),
    path('login/funcionario/', login_funcionario, name='login_funcionario'),
    
    path('aluno/home', aluno_home, name='aluno_home'),
    path('aluno/perfil', aluno_perfil, name='aluno_perfil'),
    path('aluno/logout', aluno_logout, name='aluno_logout'),
    path('aluno/criar_agendamento', aluno_criar_agendamento, name='aluno_criar_agendamento'),
    path('aluno/editar_agendamento/<int:agendamento_id>', aluno_editar_agendamento, name='aluno_editar_agendamento'),


    path('funcionario/home', funcionario_home, name='funcionario_home'),
    path('funcionario/listar_alunos', listar_alunos, name='listar_alunos'),
    path('funcionario/listar_refeicoes', listar_refeicoes, name='listar_refeicoes'),
    path('funcionario/cadastrar_refeicao', cadastrar_refeicao, name='cadastrar_refeicao'),
    path('funcionario/editar_refeicao/<int:refeicao_id>', editar_refeicao, name='editar_refeicao'),
    path('funcionario/deletar_refeicao/<int:refeicao_id>', deletar_refeicao, name='deletar_refeicao'),
]