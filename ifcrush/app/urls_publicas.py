from django.shortcuts import render
from django.urls import path
from .views import *

urlpatterns = [
    path('aplicativo/home', pagina_inicial, name="pagina_inicial"),
    path('login', login_usuario, name="login_usuario"),
    path('login/rsenha', redefinir_senha, name="redefinir_senha"),
    path('sair', sair_usuario, name="sair_usuario"),
    path('', index_site, name="index_site"),

    #MANIPULAÇÃO DE DADOS
    path('registro', registro_usuario, name="registro_usuario"),
    path('aplicativo/mensagem', enviar_mensagem, name="enviar_mensagem"),
    path('aplicativo/regras', regras_mensagem, name="regras_mensagem"),
    path('aplicativo/perfil', meu_perfil, name="meu_perfil"),
    path('aplicativo/perfil/editar', editar_perfil, name="editar_perfil"),
    path('privacidade', politicas_privacidade, name="politicas_privacidade"),
    path('termos', termos_uso, name="termos_uso")



]