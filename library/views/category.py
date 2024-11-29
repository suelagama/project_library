from django.contrib import messages
from django.db.models import ProtectedError
from django.shortcuts import redirect
from django.urls import reverse
from django.views import View

from library.forms import CategoryForm
from library.models import Category

from .base import BaseCreateView, BaseDetailView, BaseListView, BaseUpdateView


class CategoryListView(BaseListView):
    model = Category
    search_fields = ['name']
    template_name = 'categories/pages/category_list.html'

    def get(self, request, *args, **kwargs):
        request.META['breadcrumbs'] = [
            {'name': 'Dashboard', 'url': reverse('library:dashboard')},
            {'name': 'Category list', 'url': ''}]
        return super().get(request, *args, **kwargs)


class CategoryCreateView(BaseCreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'categories/pages/category_create.html'

    def get(self, request, *args, **kwargs):
        request.META['breadcrumbs'] = [
            {'name': 'Dashboard', 'url': reverse('library:dashboard')},
            {'name': 'Category list', 'url': reverse('library:category_list')},
            {'name': 'Register category', 'url': ''}
        ]
        return super().get(request, *args, **kwargs)


class CategoryDetailView(BaseDetailView):
    model = Category
    template_name = 'categories/pages/category_detail.html'

    def get(self, request, *args, **kwargs):
        request.META['breadcrumbs'] = [
            {'name': 'Dashboard', 'url': reverse('library:dashboard')},
            {'name': 'Category list', 'url': reverse('library:category_list')},
            {'name': self.get_object().name, 'url': ''}]  # type: ignore
        return super().get(request, *args, **kwargs)


class CategoryUpdateView(BaseUpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'categories/pages/category_update.html'

    def get(self, request, *args, **kwargs):
        request.META['breadcrumbs'] = [
            {'name': 'Dashboard', 'url': reverse('library:dashboard')},
            {'name': 'Category list', 'url': reverse(
                'library:category_list')},
            {'name': 'Category detail', 'url': reverse(
                'library:category_detail',
                kwargs={'slug': self.get_object().slug})},  # type: ignore
            {'name': self.get_object().name, 'url': ''}]  # type: ignore
        return super().get(request, *args, **kwargs)


class CategoryDeleteView(View):
    def post(self, request, pk):
        try:
            category = Category.objects.filter(pk=pk)
            category.delete()
            messages.success(request, 'Deleted category')
        except ProtectedError:
            messages.error(
                request, f'There are books associated with this categoty: <b>{{ category.name }}</b>')
        finally:
            return redirect('library:category_list')
