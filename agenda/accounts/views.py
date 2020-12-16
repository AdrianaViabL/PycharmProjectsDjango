from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.core.validators import validate_email
from django.contrib.auth.models import User  # para verificar se existe no sistema um usuario ja cadastrado
from django.contrib.auth.decorators import login_required
from .models import FormContato  # puxando o formulario


def login(request):
    if request.method != 'POST':
        return render(request, 'accounts/login.html')
    usuario = request.POST.get('usuario')
    senha = request.POST.get('senha')

    user = auth.authenticate(request, username=usuario, password=senha)  # se incorreto retorna NONE

    if not user:
        messages.error(request, 'usuario ou senha invalidos')
        return render(request, 'accounts/login.html')
    else:
        auth.login(request, user)
        messages.success(request, 'login efetuaco com sucesso')
        return redirect('dashboard')


def logout(request):
    auth.logout(request)
    return redirect()


def cadastro(request):
    if request.method != 'POST':
        return render(request, 'accounts/cadastro.html')
    # pegando os dados da tela para validação
    nome = request.POST.get('nome')
    sobrenome = request.POST.get('sobrenome')
    email = request.POST.get('email')
    usuario = request.POST.get('usuario')
    senha = request.POST.get('senha')
    Rsenha = request.POST.get('Rsenha')

    if not nome or not sobrenome or not email or not senha or not Rsenha or not usuario:
        messages.error(request, 'nenhum campo pode estar vazio.')
        return render(request, 'accounts/cadastro.html')

    try:
        validate_email(email)
    except:
        messages.error(request, 'Email invalido')
        return render(request, 'accounts/cadastro.html')

    if len(usuario) < 6:
        messages.error(request, 'usuario deve ter mais de 6 caracteres')
        return render(request, 'accounts/cadastro.html')

    if len(senha) < 6:
        messages.error(request, 'senha deve ter mais de 6 caracteres')
        return render(request, 'accounts/cadastro.html')

    if senha != Rsenha:
        messages.error(request, 'senha nao bate')
        return render(request, 'accounts/cadastro.html')
    print(usuario)
    if User.objects.filter(username=usuario).exists():
        messages.error(request, 'usuario ja existe')
        return render(request, 'accounts/cadastro.html')

    if User.objects.filter(email=email).exists():
        messages.error(request, 'email ja cadastrado')
        return render(request, 'accounts/cadastro.html')

    messages.success(request, 'usuario registrado com sucesso')
    user = User.objects.create_user(username=usuario, email=email, password=senha, first_name=nome,
                                    last_name=sobrenome)
    user.save()
    return redirect('login')


@login_required(redirect_field_name='login')  # caso a pessoa nao esteja logada manda para a pagina de login
def dashboard(request):
    if request.method != 'POST':  # se nao for enviado POST, recarrega o formulario
        form = FormContato()
        return render(request, 'accounts/dashboard.html', {'form': form})
    form = FormContato(request.POST, request.FILES)
    if not form.is_valid():
        messages.error(request, 'erro ao enviar o formulário')
        form = FormContato(request.POST)
        return render(request, 'accounts/dashboard.html', {'form': form})

    descricao = request.POST.get('descricao')

    if len(descricao) < 5:
        messages.error(request, 'descrição deve ter mais de 5 caracteres')
        form = FormContato(request.POST)
        return render(request, 'accounts/dashboard.html', {'form': form})

    form.save()
    messages.success(request, f'contato {request.POST.get("nome")} salvo com sucesso')
    return redirect('dashboard')
