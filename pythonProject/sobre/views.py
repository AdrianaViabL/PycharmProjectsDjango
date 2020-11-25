from django.shortcuts import render

def teste(request):
    return render(request, 'sobre/bla.html')