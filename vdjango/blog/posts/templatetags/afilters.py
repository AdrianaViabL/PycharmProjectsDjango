from django import template

register = template.Library()
@register.filter()
def plural_comentarios(num_coment):
    try:
        num_coment = int(num_coment)
        if num_coment == 0:
            return f'Nenhum comentario'
        elif num_coment == 1:
            return f'{num_coment} comentario'
        else:
            return f'{num_coment} comentarios'
    except:
        return f'{num_coment} comentario(s)'
