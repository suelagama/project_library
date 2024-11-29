# type: ignore
from django.contrib import messages
from django.urls import reverse
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from library.utils.mixins import BaseCrudView, SearchMixin


class BaseListView(SearchMixin, ListView):
    context_object_name = 'objects'
    paginate_by = 6
    ordering = '-pk'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f'{self.model._meta.verbose_name} \
            list'.capitalize()
        context['page_obj'] = context.get('page_obj')
        context['url_create'] = reverse(
            f'library:{self.model._meta.verbose_name}_create')

        return context


class BaseCreateView(BaseCrudView, CreateView):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f'Register {self.model._meta.verbose_name}'
        context['button_icon'] = 'bi bi-plus'
        context['button_name'] = 'Register'
        return context

    def form_valid(self, form):
        form.instance.registered_by = self.request.user
        messages.success(self.request,
                         f'{self.model._meta.verbose_name} registered successfully!'.capitalize())
        return super().form_valid(form)


class BaseDetailView(BaseCrudView, DetailView):
    context_object_name = 'object'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_display'] = self.object.get_user_display()  # type: ignore

        context['page_title'] = f'{self.model._meta.verbose_name} \
            detail'.capitalize()
        context['button_icon'] = 'bi bi-pencil'
        context['button_name'] = 'Edit'

        return context


class BaseUpdateView(BaseCrudView, UpdateView):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f'Edit {self.model._meta.verbose_name}'
        context['button_icon'] = 'bi bi-hdd'
        context['button_name'] = 'Save'
        return context

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        messages.success(self.request,
                         f'{self.model._meta.verbose_name} updated successfully!'.capitalize())
        return super().form_valid(form)
