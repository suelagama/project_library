from django.urls import reverse, reverse_lazy


def get_update_url(obj):
    model_name = obj.__class__.__name__.lower()
    return reverse_lazy(f'library:{model_name}_update', kwargs={'pk': obj.pk})


def get_delete_url(obj):
    model_name = obj.__class__.__name__.lower()
    return reverse(f'library:{model_name}_delete', kwargs={'pk': obj.pk})
