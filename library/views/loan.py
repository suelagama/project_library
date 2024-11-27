from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views import View

from library.forms import LoanForm
from library.models import Loan

from .base import BaseCreateView, BaseListView, BaseUpdateView


class LoanListView(BaseListView):
    model = Loan
    # ordering = '-loan_date'
    search_fields = ['student__name', 'book__title']
    template_name = 'loans/pages/loan_list.html'

    def get(self, request, *args, **kwargs):
        request.META['breadcrumbs'] = [
            {'name': 'Dashboard', 'url': reverse('library:dashboard')},
            {'name': 'Loan list', 'url': ''}]
        return super().get(request, *args, **kwargs)


class LoanCreateView(BaseCreateView):
    model = Loan
    form_class = LoanForm
    template_name = 'loans/pages/loan_create.html'
    success_url = reverse_lazy('library:loan_list')

    def get(self, request, *args, **kwargs):
        request.META['breadcrumbs'] = [
            {'name': 'Dashboard', 'url': reverse('library:dashboard')},
            {'name': 'Loan list', 'url': reverse('library:loan_list')},
            {'name': 'Register loan', 'url': ''}
        ]

        return super().get(request, *args, **kwargs)


class LoanUpdateView(BaseUpdateView):
    model = Loan
    form_class = LoanForm
    template_name = 'loans/pages/loan_update.html'
    success_url = reverse_lazy('library:loan_list')

    def get(self, request, *args, **kwargs):
        request.META['breadcrumbs'] = [
            {'name': 'Dashboard', 'url': reverse('library:dashboard')},
            {'name': 'Loan list', 'url': reverse(
                'library:loan_list')},
            {'name': 'Loan detail', 'url': reverse_lazy(
                'library:loan_detail',
                kwargs={'pk': self.get_object().pk})}
        ]
        return super().get(request, *args, **kwargs)


class LoanBookReturnView(View, LoginRequiredMixin):

    def post(self, request, loan_pk):
        loan = get_object_or_404(Loan, pk=loan_pk)
        loan.actual_return_date = timezone.now()
        loan.returned = True
        loan.save()
        messages.success(request, f'Livro <b>{loan.book.title}</b> Devolvido')
        return redirect('library:loan_list')


class LoanDeleteView(View, LoginRequiredMixin):
    def post(self, request, loan_pk):
        loan = Loan.objects.get(pk=loan_pk)
        loan.delete()
        return redirect('library:loan_list')
