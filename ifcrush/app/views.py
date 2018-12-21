from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, InvalidPage
from django.db.models.query import QuerySet
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

from .forms import *

#                    ROTAS NORMAIS
# Todas as rotas do painel administrativo está aqui #
ITEMS_PER_PAGE = 5
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


@login_required
def painel_administrativo(request, template_name="administracao/painel.html"):
    if request.user.is_staff:
        page = request.GET.get('page')
        paginator = Paginator(Mensagens.objects.filter(autorizado='Em Análise'), ITEMS_PER_PAGE)
        total = paginator.count
        try:
            mensagens = paginator.page(page)
        except InvalidPage:
            mensagens = paginator.page(1)

        usuario = Usuario.objects.all()
        turma = Turma.objects.all()
        mensagem = Mensagens.objects.all()
        nao_autorizados = Mensagens.objects.filter(autorizado="Não")
        autorizados = Mensagens.objects.filter(autorizado="Sim")
        return render(request, template_name,
                      {'lista':mensagens, 'usuario':usuario, 'turma':turma,
                       'mensagem':mensagem, 'nao_autorizados': nao_autorizados, 'autorizados': autorizados})
    else:
        return redirect('pagina_inicial')

def autenticacao_painel(request, template_name="administracao/login_administracao.html"):
    next = request.GET.get('next', '/painel/administracao')
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login realizado com sucesso!")
            return HttpResponseRedirect(next)
        else:
            messages.error(request, "Email e/ou Senha incorretos.")
            return HttpResponseRedirect(settings.LOGIN_URL)

    return render(request, template_name, {'redirect_to':next})

def sair_painel(request):
    logout(request)
    return HttpResponseRedirect(settings.LOGIN_URL)

# redirecionamentos
def redirecionar1(request):
    return redirect('painel_administrativo')

#Usuários da Administração
@login_required
def cadastro_usuario_admin(request, template_name="administracao/usuarios_administracao/cadastrar.html"):
    if request.user.is_superuser:
        try:
            form = UserAdminForm(request.POST or None)
            if request.method == "POST":
                tipo = request.POST['tipo']
                if form.is_valid():
                    user = form.save(commit=False)
                    user.set_password(user.password)
                    user.is_staff = True
                    user.save()
                    messages.success(request, "Administrador criado com sucesso")
                    return redirect('home_usuario_admin')
        except Exception:
            messages.error(request, "Erro ao cadastrar usuário!")
        return render(request, template_name, {'form': form})
    else:
        messages.error(request, "Você não tem permissão para acessar essa página.")
        return redirect('painel_administrativo')

@login_required
def editar_usuario_admin(request, pk, template_name="administracao/usuarios_administracao/cadastrar.html"):
    if request.user.is_superuser:
        try:
            user = get_object_or_404(User, pk=pk)
            if request.method == 'POST':
                form = UserAdminForm(request.POST, instance=user)
                tipo = request.POST['tipo']
                if form.is_valid():
                    if tipo == "administrador":
                        user2 = form.save(commit=False)
                        user2.set_password(user2.password)
                        user2.is_staff = True
                        user2.save()
                        messages.success(request, "Administrador atualizado com sucesso.")
                    else:
                        user2 = form.save(commit=False)
                        user2.set_password(user2.password)
                        user2.is_staff = False
                        user2.save()
                        messages.success(request, "Gerente atualizado com sucesso.")
                    return redirect('home_usuario_admin')
            else:
                form = UserAdminForm(instance=user)
        except Exception:
            messages.error(request, "Erro ao atualizar usuario.")
        return render(request, template_name, {'form':form, 'user':user})
    else:
        messages.error(request, "Você não tem permissão para acessar essa página.")
        return redirect('painel_administrativo')
@login_required
def remover_usuario_admin(request, pk):
    if request.user.is_superuser:
        try:
            user = User.objects.get(pk=pk)
            if request.user.is_superuser:
                user.delete()
                messages.success(request, "Usuário removido com sucesso.")
            else:
                messages.error(request, "Permissão negada!")
        except Exception:
            messages.error(request, "Erro ao remover usuário.")
        return redirect('home_usuario_admin')
    else:
        messages.error(request, "Você não tem permissão para acessar essa página.")
        return redirect('painel_administrativo')

@login_required
def home_usuario_admin(request, template_name="administracao/usuarios_administracao/home.html"):
    if request.user.is_staff:
        user = User.objects.filter(is_staff=True)
        users = {'lista':user}
        return render(request, template_name, users)
    else:
        messages.error(request, "Você não tem permissão para acessar essa página.")
        return redirect('painel_administrativo')

#Turmas
@login_required
def cadastro_turma(request, template_name="administracao/turmas/cadastrar.html"):
    if request.user.is_staff:
        try:
            form = TurmaForm(request.POST or None)
            if form.is_valid():
                form.save()
                messages.success(request, "Turma cadastrada com sucesso")
                return redirect('home_turma')
        except Exception:
            messages.error(request, "Erro ao cadastrar nova turma")
        return render(request, template_name, {'form':form})
    else:
        messages.error(request, "Você não tem permissão para acessar essa página.")
        return redirect('painel_administrativo')

@login_required
def info_turma(request, pk, template_name="administracao/turmas/info.html"):
    if request.user.is_staff:
        turma = get_object_or_404(Turma, pk=pk)
        return render(request, template_name, {'turma':turma})
    else:
        messages.error(request, "Você não tem permissão para acessar essa página.")
        return redirect('painel_administrativo')

@login_required
def editar_turma(request, pk, template_name="administracao/turmas/cadastrar.html"):
    if request.user.is_staff:
        try:
            turma = get_object_or_404(Turma, pk=pk)
            if request.method == 'POST':
                form = TurmaForm(request.POST, instance=turma)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Turma atualizada com sucesso!")
                    return redirect('home_turma')
            else:
                form = TurmaForm(instance=turma)
        except Exception:
            messages.error(request, "Erro ao atualizar turma!")
        return render(request, template_name, {'form':form})
    else:
        messages.error(request, "Você não tem permissão para acessar essa página.")
        return redirect('painel_administrativo')

@login_required
def remover_turma(request, pk):
    if request.user.is_staff:
        try:
            turma = Turma.objects.get(pk=pk)
            turma.delete()
            messages.success(request, "Turma removida com Sucesso")
        except Exception:
            messages.error(request, "Não foi possível remover turma")
        return redirect('home_turma')
    else:
        messages.error(request, "Você não tem permissão para acessar essa página.")
        return redirect('painel_administrativo')

@login_required
def home_turma(request, template_name="administracao/turmas/home.html"):
    if request.user.is_staff:
        page = request.GET.get('page')
        paginator = Paginator(Turma.objects.all(), ITEMS_PER_PAGE)
        total = paginator.count
        try:
            turma = paginator.page(page)
        except InvalidPage:
            turma = paginator.page(1)
        turmas = {'lista':turma}
        return render(request, template_name, turmas)
    else:
        messages.error(request, "Você não tem permissão para acessar essa página.")
        return redirect('painel_administrativo')

#Usuários
@login_required
def info_usuario(request, pk, template_name="administracao/usuarios/info.html"):
    if request.user.is_staff:
        usuario = get_object_or_404(Usuario, pk=pk)
        return render(request, template_name, {'usuario':usuario})
    else:
        messages.error(request, "Você não tem permissão para acessar essa página.")
        return redirect('painel_administrativo')

@login_required
def remover_usuario(request, pk):
    if request.user.is_staff:
        try:
            usuario = Usuario.objects.get(pk=pk)
            user = User.objects.get(pk=usuario.user.pk)
            usuario.delete()
            user.delete()
            messages.success(request, "Usuário removida com Sucesso")
        except Exception:
            messages.error(request, "Não foi possível remover usuário")
        return redirect('home_usuario')
    else:
        messages.error(request, "Você não tem permissão para acessar essa página.")
        return redirect('painel_administrativo')

@login_required
def home_usuario(request, template_name="administracao/usuarios/home.html"):
    if request.user.is_staff:
        usuario = Usuario.objects.all()
        user = User.objects.all()
        apelido = request.GET.get('buscar')
        if apelido is not None:
            teste = user.filter(username__icontains = apelido)
            if teste is not None:
                resposta = []
                for i in teste:
                    try:
                        resposta.append(usuario.get(user=i))
                    except Exception:
                        resposta = []

            else:
                resposta = usuario
        else:
            resposta = usuario

        paginator = Paginator(resposta, ITEMS_PER_PAGE)

        page = request.GET.get('page')
        total = paginator.count
        try:
            usuario = paginator.page(page)
        except InvalidPage:
            usuario = paginator.page(1)

        usuarios = {'lista':usuario}
        return render(request, template_name, usuarios)
    else:
        messages.error(request, "Você não tem permissão para acessar essa página.")
        return redirect('painel_administrativo')


#Mensagem
@login_required
def editar_mensagem(request, pk, template_name="administracao/mensagens/autorizar.html"):
    if request.user.is_staff:
        try:
            mensagem = get_object_or_404(Mensagens, pk=pk)
            if request.method == 'POST':
                form = MensagemForm(request.POST, instance=mensagem)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Mensagem atualizada com sucesso!")
                    return redirect('autorizar_mensagem')
            else:
                form = MensagemForm(instance=mensagem)
        except Exception:
            messages.error(request, "Erro ao atualizar mensagem!")
        return render(request, template_name, {'form':form})
    else:
        messages.error(request, "Você não tem permissão para acessar essa página.")
        return redirect('painel_administrativo')

@login_required
def home_mensagem(request, template_name="administracao/mensagens/home.html"):
    if request.user.is_staff:
        page = request.GET.get('page')
        paginator = Paginator(Mensagens.objects.all(), ITEMS_PER_PAGE)
        total = paginator.count
        try:
            mensagem = paginator.page(page)
        except InvalidPage:
            mensagem = paginator.page(1)
        mensagem = {'lista':mensagem}
        return render(request, template_name, mensagem)
    else:
        messages.error(request, "Você não tem permissão para acessar essa página.")
        return redirect('painel_administrativo')

@login_required
def autorizar_mensagem(request, template_name="administracao/mensagens/para_autorizar.html"):
    if request.user.is_staff:
        page = request.GET.get('page')
        paginator = Paginator(Mensagens.objects.filter(autorizado='Em Análise'), ITEMS_PER_PAGE)
        total = paginator.count
        try:
            mensagem = paginator.page(page)
        except InvalidPage:
            mensagem = paginator.page(1)
        mensagem = {'lista':mensagem}
        return render(request, template_name, mensagem)
    else:
        messages.error(request, "Você não tem permissão para acessar essa página.")
        return redirect('painel_administrativo')

@login_required
def nao_mensagem(request, template_name="administracao/mensagens/nao_autorizados.html"):
    if request.user.is_staff:
        page = request.GET.get('page')
        paginator = Paginator(Mensagens.objects.filter(autorizado='Não'), ITEMS_PER_PAGE)
        total = paginator.count
        try:
            mensagem = paginator.page(page)
        except InvalidPage:
            mensagem = paginator.page(1)
        mensagem = {'lista':mensagem}
        return render(request, template_name, mensagem)
    else:
        messages.error(request, "Você não tem permissão para acessar essa página.")
        return redirect('painel_administrativo')

@login_required
def remover_mensagem(request, pk):
    if request.user.is_staff:
        try:
            mensagem = Mensagens.objects.get(pk=pk)
            mensagem.delete()
            messages.success(request, "Mensagem removida com Sucesso")
        except Exception:
            messages.error(request, "Não foi possível remover mensagem")
        return redirect('home_mensagem')
    else:
        messages.error(request, "Você não tem permissão para acessar essa página.")
        return redirect('painel_administrativo')

########################################################
################ PÁGINAS PÚBLICAS ######################
########################################################

@login_required(login_url='/login')
def pagina_inicial(request, template_name="publico/home.html"):
    mensagens = Mensagens.objects.filter(autorizado='Sim').order_by('-id')
    return render(request, template_name, {'mensagens': mensagens})

@login_required(login_url='/login')
def enviar_mensagem(request, template_name="publico/aplicativo/enviar_mensagem.html"):
    form = EnviarMensagemForm(request.POST or None)
    if form.is_valid():
        mensagem = form.save(commit=False)
        mensagem.usuario = request.user.usuario
        mensagem.save()
        messages.success(request, "Mensagem enviada com sucesso!")
        return redirect('pagina_inicial')
    return render(request, template_name, {'form': form})

@login_required(login_url='/login')
def meu_perfil(request, template_name="publico/aplicativo/meu_perfil.html"):
    page = request.GET.get('page')
    paginator = Paginator(Mensagens.objects.filter(usuario=request.user.usuario), ITEMS_PER_PAGE)
    total = paginator.count
    try:
        mensagens = paginator.page(page)
    except InvalidPage:
        mensagens = paginator.page(1)
    return render(request, template_name, {'mensagens': mensagens})

@login_required(login_url='/login')
def editar_perfil(request, template_name="publico/aplicativo/editar_perfil.html"):
    usuario = get_object_or_404(Usuario, pk=request.user.usuario.pk)
    user = get_object_or_404(User, pk=usuario.user.pk)
    if request.method == 'POST':
        form = UserAdminForm(request.POST, instance=user)
        form2 = UsuarioForm(request.POST, instance=usuario)
        if form.is_valid() and form2.is_valid():
            user = form.save(commit=False)
            user.set_password(user.password)
            user.save()
            form2.save()
            messages.success(request, "Perfil atualizado com sucesso!")
            return redirect('meu_perfil')
    else:
        form = UserAdminForm(instance=user)
        form2 = UsuarioForm(instance=usuario)
    return render(request, template_name, {'form': form, 'form2':form2})

@login_required(login_url='/login')
def regras_mensagem(request, template_name="publico/aplicativo/regras_mensagem.html"):
    return render(request, template_name)

def registro_usuario(request, template_name="publico/registro.html"):
    try:
        form2 = UsuarioForm(request.POST or None)
        form = UserAdminForm(request.POST or None)
        if request.method == "POST":
            password_confirm = request.POST['password_confirm']
            password = request.POST['password']
            if password == password_confirm:
                if form.is_valid():
                    user = form.save(commit=False)
                    user.set_password(user.password)
                    user.is_staff = False
                    user.save()
                    user2 = User.objects.get(username=user.username)
                    usuario = form2.save(commit=False)
                    usuario.user = user2
                    usuario.ip_celular = get_client_ip(request)
                    usuario.save()
                    messages.success(request, "Cadastrado com sucesso!\nEfetue o login para continuar")
                    return redirect('login_usuario')
                else:
                    messages.error(request, "Apelido já em uso.")
            else:
                messages.error(request, "Senha não confere. Tente novamente")
    except Exception:
        messages.error(request, "Erro ao cadastrar usuário!")
    return render(request, template_name, {'form': form, 'form2': form2})

def login_usuario(request, template_name="publico/login.html"):
    next = request.GET.get('next', '/aplicativo/home')
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login realizado com sucesso!")
            return HttpResponseRedirect(next)
        else:
            messages.error(request, "Email e/ou Senha incorretos.")
            return HttpResponseRedirect(settings.LOGIN_SITE)
    return render(request, template_name, {'redirect_to':next})

def redefinir_senha(request, template_name="publico/redefinir_senha.html"):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password_confirm = request.POST['password_confirm']

        user = User.objects.get(username=username)
        if user.is_staff == False:
            if user.email == email:
                if password == password_confirm:
                    user.set_password(password)
                    user.save()
                    messages.success(request, "Senha alterada com sucesso! Efetue login para continuar!")
                    return redirect('login_usuario')
                else:
                    messages.error(request, "Nova senha não confere.")
            else:
                messages.error(request, "Usuário ou email não existem")
        else:
            messages.error(request, "Você não tem permissão para fazer isso!")
    return render(request, template_name)

def sair_usuario(request):
    logout(request)
    return HttpResponseRedirect(settings.LOGIN_SITE)

def index_site(request, template_name="publico/index.html"):
    return render(request, template_name)

def politicas_privacidade(request, template_name="publico/politicas_privacidade.html"):
    return render(request, template_name)

def termos_uso(request, template_name="publico/termos_uso.html"):
    return render(request, template_name)