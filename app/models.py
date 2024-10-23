import re
from django.core.exceptions import ValidationError
from django.db import models

def validate_cnpj(cnpj):
    if not re.match(r'^\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}$', cnpj):
        raise ValidationError('CNPJ inválido.')

class Universidade(models.Model):
    nome = models.CharField(max_length=100)
    cnpj = models.CharField(max_length=18, unique=True, validators=[validate_cnpj])
    endereco = models.CharField(max_length=255)

    def __str__(self):
        return self.nome

    class Meta:
        db_table = "universidade"

class Aluno(models.Model):
    BOLSISTA_CHOICES = [
        (0, 'Gratuito'),
        (1, 'Meia'),
        (2, 'Integral'),
    ]

    nome = models.CharField(max_length=100)
    usuario = models.CharField(max_length=50, unique=True, primary_key=True)
    senha = models.CharField(max_length=50)
    telefone = models.CharField(max_length=20)
    curso = models.CharField(max_length=100)
    matricula = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)
    universidade = models.ForeignKey(Universidade, on_delete=models.CASCADE)
    bolsista = models.IntegerField(choices=BOLSISTA_CHOICES)
    horario = models.JSONField()

    def __str__(self):
        return self.nome

    class Meta:
        db_table = "aluno"

class Empresa(models.Model):
    nome = models.CharField(max_length=100)
    cnpj = models.CharField(max_length=18, unique=True)
    endereco = models.CharField(max_length=255)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.nome

    class Meta:
        db_table = "empresa"

class Funcionario(models.Model):
    nome = models.CharField(max_length=100)
    usuario = models.CharField(max_length=50, unique=True, primary_key=True)
    senha = models.CharField(max_length=50)
    telefone = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome

    class Meta:
        db_table = "funcionario"

class Contrato(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    universidade = models.ForeignKey(Universidade, on_delete=models.CASCADE)
    data = models.DateField()
    duracao = models.IntegerField()

    def __str__(self):
        return f"{self.empresa} - {self.universidade}"

    class Meta:
        db_table = "contrato"
    
class Refeicao(models.Model):
    TIPO_CHOICES = [
        (0, 'Café da Manhã'),
        (1, 'Almoço'),
        (2, 'Jantar'),
    ]

    tipo = models.IntegerField(choices=TIPO_CHOICES)
    descricao = models.CharField(max_length=255)
    valor = models.DecimalField(max_digits=5, decimal_places=2)
    funcionario = models.ForeignKey(Funcionario, on_delete=models.CASCADE)

    def clean(self):
        super().clean()
        if not (2 <= self.valor <= 20):
            raise ValidationError('O valor deve estar entre 2 e 20.')
        
        if Refeicao.objects.exclude(id=self.id).filter(descricao=self.descricao).exists():
            raise ValidationError('A descrição deve ser única.')

    def __str__(self):
        return self.descricao

    class Meta:
        db_table = "refeicao"

from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

class Agendamento(models.Model):
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('confirmado', 'Confirmado'),
        ('cancelado', 'Cancelado'),
    ]
    
    data = models.DateField(default=timezone.now)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pendente')
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    refeicoes = models.JSONField()  # Este campo armazenará um JSON com as chaves café, almoço, jantar
    
    def clean(self):
        super().clean()
        
        # Validação para garantir que a data do agendamento seja futura
        if self.data < timezone.now().date():
            raise ValidationError('A data do agendamento deve ser futura.')
        
        # Validação para garantir que a data não seja um sábado ou domingo
        if self.data.weekday() in [5, 6]:
            raise ValidationError('Não é possível agendar refeições para sábado ou domingo.')
        
        # Validação para garantir que a data limite seja no máximo 7 dias após a data atual
        if (self.data - timezone.now().date()).days > 7:
            raise ValidationError('A data do agendamento deve ser no máximo 7 dias após a data atual.')

        # Validações para agendamento duplicado para a mesma data
        if Agendamento.objects.exclude(id=self.id).filter(aluno=self.aluno, data=self.data, status='confirmado').exists():
            raise ValidationError('Já existe um agendamento confirmado para esta data.')
        
        # Validação para garantir que pelo menos uma refeição seja escolhida
        if not any(self.refeicoes.values()):
            raise ValidationError('Pelo menos uma refeição deve ser escolhida.')

        # Validação para garantir que não haja duplicações de refeição no mesmo dia
        if len(set(self.refeicoes.keys()) & {'cafe', 'almoco', 'jantar'}) < 1:
            raise ValidationError('Escolha pelo menos uma refeição válida: café, almoço ou jantar.')

        """# Verificação de duplicação de refeições
        if any(self.refeicoes.get(ref) in [None, ''] for ref in ['cafe', 'almoco', 'jantar']):
            raise ValidationError('Não é permitido duplicar o agendamento de refeições no mesmo dia.')"""
    
    def __str__(self):
        return f"Agendamento de {self.aluno.nome} para {self.data}"

    class Meta:
        db_table = "agendamento"
        unique_together = ('aluno', 'data')  # Garante que não haja dois agendamentos confirmados para a mesma data
