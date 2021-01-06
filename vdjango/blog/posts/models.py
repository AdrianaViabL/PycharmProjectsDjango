from django.db import models
from categoria.models import Categoria
from django.contrib.auth.models import User
from django.utils import timezone


class Post(models.Model):
    titulo_post = models.CharField(max_length=255, verbose_name='Títilo')
    autor_post = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name='Autor')
    data_post = models.DateTimeField(default=timezone.now, verbose_name='data')
    conteudo_post = models.TextField(verbose_name='Conteúdo')
    excerto_post = models.TextField(verbose_name='excerto')
    categoria_post = models.ForeignKey(Categoria, on_delete=models.DO_NOTHING,
                                       blank=True, null=True, verbose_name='categoria')
    imagem_post = models.ImageField(upload_to='post_img/%Y/%m', blank=True, null=True, verbose_name='Imagem')
    publicado_post = models.BooleanField(default=False, verbose_name='publicado')

    def __str__(self):
        return self.titulo_post
