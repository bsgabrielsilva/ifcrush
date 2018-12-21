from django.urls import path
from .views import *

urlpatterns = [

    #           ROTAS PAINEL ADMINISTRATIVO         #

    #Rota Painel administrativo
    path('administracao', painel_administrativo, name='painel_administrativo'),
    path('', redirecionar1),
    path('autenticacao', autenticacao_painel, name='autenticacao_painel'),
    path('logout', sair_painel, name="sair_painel"),

    #Rotas Usuários da Administração
    path('usuarios_administracao/cadastro', cadastro_usuario_admin, name='cadastrar_usuario_admin'),
    path('usuarios_administracao/editar/<int:pk>', editar_usuario_admin, name='editar_usuario_admin'),
    path('usuarios_administracao/remover/<int:pk>', remover_usuario_admin, name='remover_usuario_admin'),
    path('usuarios_administracao', home_usuario_admin, name='home_usuario_admin'),

    #Rotas Turmas
    path('turmas/cadastro', cadastro_turma, name='cadastrar_turma'),
    path('turmas/editar/<int:pk>', editar_turma, name='editar_turma'),
    path('turmas/informacoes/<int:pk>', info_turma, name='info_turma'),
    path('turmas/remover/<int:pk>', remover_turma, name='remover_turma'),
    path('turmas', home_turma, name='home_turma'),

    #Path
    path('usuarios', home_usuario, name='home_usuario'),
    path('usuarios/info/<int:pk>', info_usuario, name='info_usuario'),
    path('usuarios/remover/<int:pk>', remover_usuario, name='remover_usuario'),

    #Rotas Mensagens
    path('mensagens/autorizar/<int:pk>', editar_mensagem, name="editar_mensagem"),
    path('mensagens/remover/<int:pk>', remover_mensagem, name="remover_mensagem"),
    path('mensagens/para_autorizar', autorizar_mensagem, name="autorizar_mensagem"),
    path('mensagens/nao_autorizadas', nao_mensagem, name="nao_mensagem"),
    path('mensagens', home_mensagem, name="home_mensagem"),

]