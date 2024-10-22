from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm
from .models import Aluno

# View para a tela de login
def login_aluno(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            usuario = form.cleaned_data.get("usuario")
            senha = form.cleaned_data.get("senha")
            try:
                aluno = Aluno.objects.get(usuario=usuario, senha=senha)  # Autenticando pelo model Aluno
                request.session['aluno_id'] = aluno.usuario  # Salvando ID do aluno na sessão
                return redirect('aluno_home')  # Redirecionando para a página de boas-vindas
            except Aluno.DoesNotExist:
                form.add_error(None, "Usuário ou senha incorretos")
    else:
        form = LoginForm()
    return render(request, 'aluno/login.html', {'form': form})

# View para a tela de boas-vindas do aluno
def aluno_home(request):
    aluno_id = request.session.get('aluno_id')
    if aluno_id:
        aluno = Aluno.objects.get(usuario=aluno_id)
        return render(request, 'aluno/home.html', {'aluno': aluno})
    else:
        return redirect('login_aluno')
