from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Turma(models.Model):
    TURNO = (
        ('s/t', 'Sem turno'),
        ('manhã', 'Manhã'),
        ('tarde', 'Tarde'),
        ('noite', 'Noite')
    )

    nome_turma = models.CharField('turma', max_length=250, null=False)
    turno = models.CharField('turno', max_length=10, null=False, choices=TURNO)

    def __str__(self):
        return self.nome_turma + ' ' + self.turno


class Usuario(models.Model):


    data_nascimento = models.DateField('data de nascimento', null=False)
    ip_celular = models.CharField('IP', max_length=250, null=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    turma = models.ForeignKey(Turma, on_delete=models.PROTECT)

    def __str__(self):
        return self.user.username


class Mensagens(models.Model):
    AUTORIZADO = (
        ('Sim', 'Sim'),
        ('Não', 'Não'),
        ('Em Análise', 'Em Análise')
    )

    mensagem = models.TextField('Mensagem', null=False)
    titulo = models.CharField('Titulo', max_length=150, null=False)
    autorizado = models.CharField('autorizadoo', max_length=12, null=False, choices=AUTORIZADO, default='Em Análise')
    feedback = models.TextField('Feedback', null=False)

    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='mensagens_usuario')