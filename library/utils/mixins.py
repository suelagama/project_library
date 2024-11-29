# type: ignore
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.urls import reverse, reverse_lazy
from django.utils.html import format_html
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


class BaseCrudView(LoginRequiredMixin):
    model = None
    forms_class = None
    success_url = None
    login_url = 'account:user_login'

    def get_success_url(self):
        if self.success_url:
            return self.success_url
        return reverse_lazy(f'library:{self.model._meta.model_name}_detail', kwargs={'slug': self.object.slug})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['url_back'] = reverse(
            f'library:{self.model._meta.verbose_name}_list')  # type: ignore
        return context


class UserDisplayMixin:
    def get_user_display(self, updated_by_field='updated_by', registered_by_field='registered_by'):
        updated_by = getattr(self, updated_by_field, None)
        registered_by = getattr(self, registered_by_field, None)

        if updated_by:
            user = updated_by
            action = 'Updated by'
        elif registered_by:
            user = registered_by
            action = 'Registered by'
        else:
            return format_html('<span class="fw-bold">Registered by: </span>&nbsp;Desconhecido')

        if user.first_name:
            return format_html(f'<span class="fw-bold">{action}</span>&nbsp;{user.first_name} {user.last_name}')
        else:
            return format_html(f'<span class="fw-bold">{action}</span>&nbsp;{user.username}')
