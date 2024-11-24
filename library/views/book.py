
from django.contrib import messages
from django.db.models import ProtectedError
from django.http import Http404
from django.shortcuts import redirect
from django.views import View

from library.forms import BookForm
from library.models import Book

from .base import BaseCreateView, BaseDetailView, BaseListView, BaseUpdateView


class BookListView(BaseListView):
    model = Book
    search_fields = ['title', 'author__name',
                     'category__name', 'publisher__name', 'publication_year']
    template_name = 'books/pages/book_list.html'


class BookListViewCategory(BaseListView):
    model = Book
    template_name = 'books/pages/book_search.html'

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(
            categories__slug=self.kwargs.get('slug')
        )

        if not queryset:
            raise Http404()

        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['page_title'] = f'Livros por categoria: {
            context.get("objects")[0].categories.first().name}'
        return context


class BookListViewAuthor(BaseListView):
    allow_empty = False
    model = Book
    template_name = 'books/pages/book_search.html'

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(
            authors__slug=self.kwargs.get('slug')
        )

        if not queryset:
            raise Http404()

        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['page_title'] = f'Livros do autor: {
            context.get("objects")[0].authors.first().name}'
        return context


class BookListViewPublisher(BaseListView):
    model = Book
    template_name = 'books/pages/book_search.html'

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(
            publisher__slug=self.kwargs.get('slug')
        )

        if not queryset:
            raise Http404()

        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['page_title'] = f'Livros da Editora: {
            context.get("objects")[0].publisher.name}'
        return context


class BookCreateView(BaseCreateView):
    model = Book
    form_class = BookForm
    template_name = 'books/pages/book_create.html'


class BookDetailView(BaseDetailView):
    model = Book
    template_name = 'books/pages/book_detail.html'


class BookUpdateView(BaseUpdateView):
    model = Book
    form_class = BookForm
    template_name = 'books/pages/book_update.html'


class BookDeleteView(View):
    def post(self, request, book_pk):
        try:
            book = Book.objects.get(pk=book_pk)
            book.delete()
            messages.success(request, 'Deleted book')
        except ProtectedError:
            messages.error(
                request, f'There are loans associated with the book: <b>{book.title}</b>')
        finally:
            return redirect('library:book_list')
