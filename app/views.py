from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login
from .forms import *
from .models import *

# View para a tela de login
def login_aluno(request):
    if request.method == "POST":
        form = AlunoLoginForm(request.POST)
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
        form = AlunoLoginForm()
    return render(request, 'aluno/login.html', {'form': form})

# View para a tela de boas-vindas do aluno
def aluno_home(request):
    aluno_id = request.session.get('aluno_id')
    if aluno_id:
        aluno = Aluno.objects.get(usuario=aluno_id)
        return render(request, 'aluno/home.html', {'aluno': aluno})
    else:
        return redirect('login_aluno')

# View para a tela de login do funcionário
def login_funcionario(request):
    if request.method == "POST":
        form = FuncionarioLoginForm(request.POST)
        if form.is_valid():
            usuario = form.cleaned_data.get("usuario")
            senha = form.cleaned_data.get("senha")
            try:
                funcionario = Funcionario.objects.get(usuario=usuario, senha=senha)  # Autenticando pelo model Funcionario
                request.session['funcionario_id'] = funcionario.usuario  # Salvando o ID do funcionário na sessão
                return redirect('funcionario_home')  # Redirecionando para a página de boas-vindas
            except Funcionario.DoesNotExist:
                form.add_error(None, "Usuário ou senha incorretos")
    else:
        form = FuncionarioLoginForm()
    return render(request, 'funcionario/login.html', {'form': form})

# View para a tela de boas-vindas do funcionário
def funcionario_home(request):
    funcionario_id = request.session.get('funcionario_id')
    if funcionario_id:
        funcionario = Funcionario.objects.get(usuario=funcionario_id)
        return render(request, 'funcionario/home.html', {'funcionario': funcionario})
    else:
        return redirect('login_funcionario')
    
# View para listar os alunos relacionados ao contrato do funcionário
def listar_alunos(request):
    funcionario_id = request.session.get('funcionario_id')
    if funcionario_id:
        funcionario = Funcionario.objects.get(usuario=funcionario_id)
        # Encontrar o contrato da empresa do funcionário
        contrato = Contrato.objects.filter(empresa=funcionario.empresa).first()
        
        if contrato:
            # Listar os alunos que pertencem à mesma universidade do contrato
            alunos = Aluno.objects.filter(universidade=contrato.universidade)
            return render(request, 'funcionario/listar_alunos.html', {'alunos': alunos})
        else:
            return render(request, 'funcionario/listar_alunos.html', {'error': 'Nenhum contrato encontrado para a empresa.'})
    else:
        return redirect('login_funcionario')
    
# View para listar as refeições cadastradas pelo funcionário e pela empresa
def listar_refeicoes(request):
    funcionario_id = request.session.get('funcionario_id')
    if funcionario_id:
        funcionario = Funcionario.objects.get(usuario=funcionario_id)
        # Listar as refeições cadastradas por funcionários da mesma empresa
        refeicoes = Refeicao.objects.filter(funcionario__empresa=funcionario.empresa).order_by('tipo')
        return render(request, 'funcionario/listar_refeicoes.html', {'refeicoes': refeicoes})
    else:
        return redirect('login_funcionario')
    
from django.shortcuts import render, redirect
from .forms import RefeicaoForm

# View para cadastrar uma nova refeição
def cadastrar_refeicao(request):
    funcionario_id = request.session.get('funcionario_id')
    if funcionario_id:
        funcionario = Funcionario.objects.get(usuario=funcionario_id)
        if request.method == 'POST':
            form = RefeicaoForm(request.POST)
            if form.is_valid():
                refeicao = form.save(commit=False)
                refeicao.funcionario = funcionario  # Associando a refeição ao funcionário logado
                refeicao.save()
                return redirect('listar_refeicoes')  # Redireciona para listar refeições após o cadastro
        else:
            form = RefeicaoForm()
        return render(request, 'funcionario/cadastrar_refeicao.html', {'form': form})
    else:
        return redirect('login_funcionario')

# View para editar uma refeição
def editar_refeicao(request, refeicao_id):
    refeicao = get_object_or_404(Refeicao, id=refeicao_id)
    if request.method == 'POST':
        form = RefeicaoForm(request.POST, instance=refeicao)
        if form.is_valid():
            form.save()
            return redirect('listar_refeicoes')
    else:
        form = RefeicaoForm(instance=refeicao)
    return render(request, 'funcionario/editar_refeicao.html', {'form': form})

# View para deletar uma refeição
def deletar_refeicao(request, refeicao_id):
    refeicao = get_object_or_404(Refeicao, id=refeicao_id)
    if request.method == 'POST':
        refeicao.delete()
        return redirect('listar_refeicoes')
    return render(request, 'funcionario/deletar_refeicao_confirm.html', {'refeicao': refeicao})