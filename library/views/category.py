from django.contrib import messages
from django.db.models import ProtectedError
from django.shortcuts import redirect
from django.views import View

from library.forms import CategoryForm
from library.models import Category

from .base import BaseCreateView, BaseDetailView, BaseListView, BaseUpdateView


class CategoryListView(BaseListView):
    model = Category
    search_fields = ['name']
    template_name = 'categories/pages/category_list.html'


class CategoryCreateView(BaseCreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'categories/pages/category_create.html'


class CategoryDetailView(BaseDetailView):
    model = Category
    template_name = 'categories/pages/category_detail.html'


class CategoryUpdateView(BaseUpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'categories/pages/category_update.html'


class CategoryDeleteView(View):
    def post(self, request, category_pk):
        try:
            category = Category.objects.filter(pk=category_pk)
            category.delete()
            messages.success(request, 'Deleted category')
        except ProtectedError:
            messages.error(
                request, f'There are books associated with this categoty: <b>{{ category.name }}</b>')
        finally:
            return redirect('library:category_list')
