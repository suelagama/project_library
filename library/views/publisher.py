from django.contrib import messages
from django.db.models import ProtectedError
from django.shortcuts import redirect
from django.views import View

from library.forms import PublisherForm
from library.models import Publisher

from .base import BaseCreateView, BaseDetailView, BaseListView, BaseUpdateView


class PublisherListView(BaseListView):
    model = Publisher
    search_fields = ['name']
    template_name = 'publishers/pages/publisher_list.html'


class PublisherCreateView(BaseCreateView):
    model = Publisher
    form_class = PublisherForm
    template_name = 'publishers/pages/publisher_create.html'


class PublisherDetailView(BaseDetailView):
    model = Publisher
    template_name = 'publishers/pages/publisher_detail.html'


class PublisherUpdateView(BaseUpdateView):
    model = Publisher
    form_class = PublisherForm
    template_name = 'Publishers/pages/publisher_update.html'


class PublisherDeleteView(View):
    def post(self, request, publisher_pk):
        try:
            publisher = Publisher.objects.get(pk=publisher_pk)
            publisher.delete()
            messages.success(request, 'Deleted publisher')
        except ProtectedError:
            messages.error(
                request, f'There are books associated with this publisher: <b>{publisher.name}</b>')
        finally:
            return redirect('library:publisher_list')
