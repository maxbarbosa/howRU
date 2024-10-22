from django import forms
from .models import Refeicao


class AlunoLoginForm(forms.Form):
    usuario = forms.CharField(max_length=50, label="Usuário")
    senha = forms.CharField(widget=forms.PasswordInput, label="Senha")

class FuncionarioLoginForm(forms.Form):
    usuario = forms.CharField(max_length=50, label="Usuário")
    senha = forms.CharField(widget=forms.PasswordInput, label="Senha")

class RefeicaoForm(forms.ModelForm):
    class Meta:
        model = Refeicao
        fields = ['tipo', 'descricao', 'valor']
