# templatetags/breadcrumbs.py
from django import template

register = template.Library()


@register.inclusion_tag('components/breadcrumbs/breadcrumbs.html', takes_context=True)
def breadcrumb(context):
    request = context['request']
    breadcrumbs = request.META.get('breadcrumbs', [])
    return {'breadcrumbs': breadcrumbs}
