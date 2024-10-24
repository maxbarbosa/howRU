from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as django_logout
from .forms import *
from .models import *

def homepage(request):
    return render(request, 'home/index.html')  # Renderiza a página index.html

# View para a tela de login
def login_aluno(request):
    error_message = None
    if request.method == "POST":
        usuario = request.POST.get("usuario")
        senha = request.POST.get("senha")
        
        try:
            aluno = Aluno.objects.get(usuario=usuario, senha=senha)
            request.session['aluno_id'] = aluno.usuario  # Salvando o ID do aluno na sessão
            return redirect('aluno_home')  # Redirecionando para a página de boas-vindas
        except Aluno.DoesNotExist:
            error_message = "Usuário ou senha incorretos"  # Definindo a mensagem de erro

    return render(request, 'aluno/login.html', {'error_message': error_message})

# View para a tela de boas-vindas do aluno
def aluno_home(request):
    aluno_id = request.session.get('aluno_id')
    if not aluno_id:
        return redirect('login_aluno')

    aluno = Aluno.objects.get(usuario=aluno_id)
    agendamentos = Agendamento.objects.filter(aluno=aluno)

    return render(request, 'aluno/home.html', {
        'aluno': aluno,
        'agendamentos': agendamentos
    })


# View para exibir os dados do aluno
def aluno_perfil(request):
    aluno_id = request.session.get('aluno_id')
    if aluno_id:
        aluno = Aluno.objects.get(usuario=aluno_id)
        return render(request, 'aluno/perfil.html', {'aluno': aluno})
    else:
        return redirect('login_aluno')

# View para fazer logout do aluno
def aluno_logout(request):
    if request.session.get('aluno_id'):
        request.session.flush()  # Remove todos os dados da sessão
        django_logout(request)
    return redirect('login_aluno')

# View para a tela de login do funcionário
def login_funcionario(request):
    error_message = None
    if request.method == "POST":
        usuario = request.POST.get("usuario")
        senha = request.POST.get("senha")
        
        try:
            funcionario = Funcionario.objects.get(usuario=usuario, senha=senha)
            request.session['funcionario_id'] = funcionario.usuario  # Salvando o ID do funcionário na sessão
            return redirect('funcionario_home')  # Redirecionando para a página de boas-vindas
        except Funcionario.DoesNotExist:
            error_message = "Usuário ou senha incorretos"  # Definindo a mensagem de erro

    return render(request, 'funcionario/login.html', {'error_message': error_message})

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

def aluno_criar_agendamento(request):
    aluno_id = request.session.get('aluno_id')
    if not aluno_id:
        return redirect('login_aluno')

    aluno = Aluno.objects.get(usuario=aluno_id)
    
    refeicoes_cafe = Refeicao.objects.filter(tipo=0)
    refeicoes_almoco = Refeicao.objects.filter(tipo=1)
    refeicoes_jantar = Refeicao.objects.filter(tipo=2)

    error_message = None  # Variável para armazenar a mensagem de erro

    if request.method == 'POST':
        data = request.POST.get('data')
        cafe = request.POST.get('cafe')
        almoco = request.POST.get('almoco')
        jantar = request.POST.get('jantar')
        status = request.POST.get('status')

        refeicoes = {
            'cafe': cafe,
            'almoco': almoco,
            'jantar': jantar
        }

        agendamento = Agendamento(
            data=data,
            status=status,
            aluno=aluno,
            refeicoes=refeicoes
        )

        # Tentando validar o agendamento antes de salvar
        try:
            agendamento.full_clean()  # Chama todas as validações do model
            agendamento.save()  # Salva no banco de dados se tudo estiver válido
            return redirect('aluno_home')
        except ValidationError as e:
            error_message = e.messages  # Captura as mensagens de erro

    return render(request, 'aluno/criar_agendamento.html', {
        'refeicoes_cafe': refeicoes_cafe,
        'refeicoes_almoco': refeicoes_almoco,
        'refeicoes_jantar': refeicoes_jantar,
        'error_message': error_message  # Passa a mensagem de erro para o template
    })

def aluno_editar_agendamento(request, agendamento_id):
    agendamento = get_object_or_404(Agendamento, id=agendamento_id)
    refeicoes_cafe = Refeicao.objects.filter(tipo=0)
    refeicoes_almoco = Refeicao.objects.filter(tipo=1)
    refeicoes_jantar = Refeicao.objects.filter(tipo=2)

    error_message = None  # Variável para armazenar a mensagem de erro

    if request.method == 'POST':
        agendamento.data = request.POST.get('data')
        agendamento.refeicoes['cafe'] = request.POST.get('cafe')
        agendamento.refeicoes['almoco'] = request.POST.get('almoco')
        agendamento.refeicoes['jantar'] = request.POST.get('jantar')
        agendamento.status = request.POST.get('status')

        # Tentando validar o agendamento antes de salvar
        try:
            agendamento.full_clean()  # Chama as validações do model
            agendamento.save()  # Salva no banco de dados se tudo estiver válido
            return redirect('aluno_home')
        except ValidationError as e:
            error_message = e.messages  # Captura as mensagens de erro

    return render(request, 'aluno/editar_agendamento.html', {
        'agendamento': agendamento,
        'refeicoes_cafe': refeicoes_cafe,
        'refeicoes_almoco': refeicoes_almoco,
        'refeicoes_jantar': refeicoes_jantar,
        'error_message': error_message  # Passa a mensagem de erro para o template
    })

def funcionario_dashboard(request):
    funcionario_id = request.session.get('funcionario_id')
    if funcionario_id:
        funcionario = Funcionario.objects.get(usuario=funcionario_id)
        return render(request, 'funcionario/dashboard.html', {'funcionario': funcionario})
    else:
        return redirect('login_funcionario')
