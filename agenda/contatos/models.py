from django.db import models
from django.utils import timezone


#  colocar o comando no terminal(dentro do pycharm ou do projeto)
#  para que as alterações feitas no banco de dados sejam migradas
#  = python manage.py makemigrations

class Categoria(models.Model):
    nome = models.CharField(max_length=255)

    def __str__(self):
        return self.nome  # para que o nome da categoria apareça no caminho do admin


class Contato(models.Model):
    nome = models.CharField(max_length=255)  # campo do tipo String
    sobrenome = models.CharField(max_length=255, blank=True)  # tornando um campo opcional
    telefone = models.CharField(max_length=100)
    email = models.CharField(max_length=255, blank=True)
    data_criacao = models.DateTimeField(default=timezone.now)
    descricao = models.TextField(blank=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.DO_NOTHING)
    mostrar = models.BooleanField(default=True)

    def __str__(self):
        return self.nome