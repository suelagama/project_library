from django import template

register = template.Library()


@register.filter
def group_by(value, group_size):
    """Divide uma lista em grupos de tamanho especificado."""
    return [value[i:i + group_size] for i in range(0, len(value), group_size)]
