from django.contrib import messages
from django.db.models import ProtectedError
from django.shortcuts import redirect
from django.views import View

from library.forms import AuthorForm
from library.models import Author

from .base import BaseCreateView, BaseDetailView, BaseListView, BaseUpdateView


class AuthorListView(BaseListView):
    model = Author
    search_fields = ['name', 'about']
    template_name = 'authors/pages/author_list.html'


class AuthorCreateView(BaseCreateView):
    model = Author
    form_class = AuthorForm
    template_name = 'authors/pages/author_create.html'


class AuthorDetailView(BaseDetailView):
    model = Author
    template_name = 'authors/pages/author_detail.html'


class AuthorUpdateView(BaseUpdateView):
    model = Author
    form_class = AuthorForm
    template_name = 'authors/pages/author_update.html'


class AuthorDeleteView(View):
    def post(self, request, author_pk):
        try:
            author = Author.objects.get(pk=author_pk)
            author.delete()
            messages.success(request, 'Deleted author')
        except ProtectedError:
            messages.error(
                request, f'There are books associated with this author: <b>{author.name}</b>')
        finally:
            return redirect('library:author_list')
