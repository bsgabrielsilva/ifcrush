from django import forms
from django.contrib.auth.models import User
from .models import *

class DateInput(forms.DateInput):
    input_type = 'date'

class TurmaForm(forms.ModelForm):
    class Meta:
        model = Turma
        fields = ['nome_turma', 'turno']
        widgets = {
            'nome_turma': forms.TextInput(attrs={'class':'form-control'}),
            'turno': forms.Select(attrs={'class':'form-control'})
        }

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['data_nascimento', 'turma']
        widgets = {
            'data_nascimento': DateInput(attrs={'class':'form-control', 'max':"2005-01-02"}),
            'turma': forms.Select(attrs={'class':'form-control'}),
        }

class MensagemForm(forms.ModelForm):
    class Meta:
        model = Mensagens
        fields = ['mensagem', 'titulo', 'autorizado', 'feedback', 'usuario']
        widgets = {
            'titulo': forms.TextInput(attrs={'type':'hidden', 'class':'form-control'}),
            'mensagem': forms.TextInput(attrs={'type':'hidden','class':'form-control'}),
            'autorizado': forms.Select(attrs={'class':'form-control'}),
            'feedback': forms.Textarea(attrs={'class':'form-control'}),
            'usuario': forms.Select(attrs={'class':'form-control'})
        }

class EnviarMensagemForm(forms.ModelForm):
    class Meta:
        model = Mensagens
        fields = ['titulo', 'mensagem']
        widgets = {
            'titulo': forms.TextInput(attrs={'style':"border-style:none;",'class':'form-control','placeholder':'Titulo'}),
            'mensagem': forms.Textarea(attrs={'style':"border-style:none;",'class':'form-control','placeholder':'Escreva Sua mensagem'})
        }

class UserAdminForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']
        widgets = {
            'first_name': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Seu Nome'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Seu Sobrenome'}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Seu apelido no sistema'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder':'Seu Email'}),
            'password': forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Sua senha'})
        }