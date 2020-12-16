from django.db import models
from contatos.models import Contato
from django import forms


class FormContato(forms.ModelForm):
    class Meta:
        model = Contato  # qual modelo esse formulario esta representando
        exclude = () # se irao ter campos que nao devem aparecer no template renderizado
