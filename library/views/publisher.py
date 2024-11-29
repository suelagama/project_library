from django.contrib import messages
from django.db.models import ProtectedError
from django.shortcuts import redirect
from django.urls import reverse
from django.views import View

from library.forms import PublisherForm
from library.models import Publisher

from .base import BaseCreateView, BaseDetailView, BaseListView, BaseUpdateView


class PublisherListView(BaseListView):
    model = Publisher
    search_fields = ['name']
    template_name = 'publishers/pages/publisher_list.html'

    def get(self, request, *args, **kwargs):
        request.META['breadcrumbs'] = [
            {'name': 'Dashboard', 'url': reverse('library:dashboard')},
            {'name': 'Publisher list', 'url': ''}]
        return super().get(request, *args, **kwargs)


class PublisherCreateView(BaseCreateView):
    model = Publisher
    form_class = PublisherForm
    template_name = 'publishers/pages/publisher_create.html'

    def get(self, request, *args, **kwargs):
        request.META['breadcrumbs'] = [
            {'name': 'Dashboard', 'url': reverse('library:dashboard')},
            {'name': 'Publisher list', 'url': reverse(
                'library:publisher_list')},
            {'name': 'Register publisher', 'url': ''}
        ]
        return super().get(request, *args, **kwargs)


class PublisherDetailView(BaseDetailView):
    model = Publisher
    template_name = 'publishers/pages/publisher_detail.html'

    def get(self, request, *args, **kwargs):
        request.META['breadcrumbs'] = [
            {'name': 'Dashboard', 'url': reverse('library:dashboard')},
            {'name': 'Publisher list', 'url': reverse(
                'library:publisher_list')},
            {'name': self.get_object().name, 'url': ''}]  # type: ignore
        return super().get(request, *args, **kwargs)


class PublisherUpdateView(BaseUpdateView):
    model = Publisher
    form_class = PublisherForm
    template_name = 'publishers/pages/publisher_update.html'

    def get(self, request, *args, **kwargs):
        request.META['breadcrumbs'] = [
            {'name': 'Dashboard', 'url': reverse('library:dashboard')},
            {'name': 'Publisher list', 'url': reverse(
                'library:publisher_list')},
            {'name': 'Publisher detail', 'url': reverse(
                'library:publisher_detail',
                kwargs={'slug': self.get_object().slug})},  # type: ignore
            {'name': self.get_object().name, 'url': ''}]  # type: ignore
        return super().get(request, *args, **kwargs)


class PublisherDeleteView(View):
    def post(self, request, pk):
        try:
            publisher = Publisher.objects.get(pk=pk)
            publisher.delete()
            messages.success(request, 'Deleted publisher')
        except ProtectedError:
            messages.error(
                request, f'There are books associated with this publisher: <b>{publisher.name}</b>')
        finally:
            return redirect('library:publisher_list')
