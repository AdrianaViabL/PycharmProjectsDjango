from django.db import models
from categoria.models import Categoria
from django.contrib.auth.models import User
from django.utils import timezone
from PIL import Image
from django.conf import settings
import os


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

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # repassando e salvando qualquer alteração no template (quando chamado)
        self.resize_image(self.imagem_post.name, 800)

    @staticmethod  # é estatico pois nao vai alterar nada dentro da classe
    def resize_image(nome_imagem, nova_largura):
        img_path = os.path.join(settings.MEDIA_ROOT, nome_imagem)
        img = Image.open(img_path)
        width, height = img.size
        print(width, height, nova_largura)
        new_height = round((nova_largura * height) / width)

        if width <= nova_largura:
            img.close()
            return

        nova_img = img.resize((nova_largura, new_height), Image.ANTIALIAS)
        nova_img.save(
            img_path,
            optimize=True,
            quality=60
        )
        nova_img.close()
