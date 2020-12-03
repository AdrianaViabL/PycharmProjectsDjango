from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from .models import Contato
from django.core.paginator import Paginator
from django.db.models import Q, Value
from django.db.models.functions import Concat
from django.contrib import messages


def index(request):
    contatos = Contato.objects.order_by('-id').filter(
        mostrar=True
    )
    paginator = Paginator(contatos, 5)
    page = request.GET.get('p')
    contatos = paginator.get_page(page)

    return render(request, 'contatos/index.html', {
        'contatos': contatos
    })


def ver_contato(request, contato_id):
    # forma 1 de tratar o erro 404
    # try:
    #     contato = Contato.objects.get(id=contato_id)
    #     return render(request, 'contatos/ver_contato.html', {
    #         'contato': contato
    #     })
    # except Contato.DoesNotExist as e:
    #     raise Http404()
    contato = get_object_or_404(Contato, id=contato_id)
    if not contato.mostrar:
        raise Http404()
    return render(request, 'contatos/ver_contato.html', {
        'contato': contato
    })


def busca(request):
    termo = request.GET.get('termo')  # pegando o valor que esta sendo digitado no campo 'termo'

    if termo is None or not termo:
        messages.add_message(request, messages.ERROR,
                             'Campo termo não pode ficar vazio.')
        return redirect('index')  #nome da view que ele vai ser redirecionado

    campos = Concat('nome', Value(' '), 'sobrenome')

    # forma de pesquisa usando os campos 'nome' e 'sobrenome' de forma separada
    # contatos = Contato.objects.order_by('-id').filter(
    #     Q(nome__icontains=termo) | Q(sobrenome__icontains=termo),
    #     mostrar=True
    # )

    contatos = Contato.objects.annotate(
        nome_completo=campos
    ).filter(
        Q(nome_completo__icontains=termo) | Q(telefone__icontains=termo)
    )

    paginator = Paginator(contatos, 5)
    page = request.GET.get('p')
    contatos = paginator.get_page(page)

    return render(request, 'contatos/busca.html', {
        'contatos': contatos
    })
