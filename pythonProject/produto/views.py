from django.shortcuts import render


def metodo(request):
    return render(request, 'produto/index.html')
