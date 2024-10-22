from django import forms

class LoginForm(forms.Form):
    usuario = forms.CharField(max_length=50, label="Usuário")
    senha = forms.CharField(widget=forms.PasswordInput, label="Senha")
