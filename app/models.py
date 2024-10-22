from django.db import models

class Universidade(models.Model):
    nome = models.CharField(max_length=100)
    cnpj = models.CharField(max_length=18, unique=True)
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
