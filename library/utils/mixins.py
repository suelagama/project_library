# type: ignore

from django.db.models import Q
from django.urls import reverse, reverse_lazy
from django.utils.text import slugify


class UniqueSlugMixin:
    def generate_unique_slug(self, field):
        value = getattr(self, field)
        unique_slug = slugify(value)
        num = 1

        model_class = self.__class__

        while model_class.objects.filter(slug=unique_slug).exists():
            unique_slug = f'{unique_slug}-{num}'
            num += 1

        return unique_slug


class SearchMixin:
    search_fields = []

    def get_queryset(self):
        queryset = super().get_queryset()
        search_term = self.request.GET.get('q', '')

        if search_term:
            q_objects = Q()
            for field in self.search_fields:
                q_objects |= Q(**{f'{field}__icontains': search_term})
            queryset = queryset.filter(q_objects)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_term'] = self.request.GET.get('q', '')
        context['url_back'] = reverse(
            f'library:{self.model._meta.verbose_name}_list')  # type: ignore

        return context


class BaseCrudView:
    model = None
    forms_class = None
    success_url = None

    def get_success_url(self):
        if self.success_url:
            return self.success_url
        return reverse_lazy(f'library:{self.model._meta.model_name}_detail', kwargs={'slug': self.object.slug})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['url_back'] = reverse(
            f'library:{self.model._meta.verbose_name}_list')  # type: ignore
        return context
