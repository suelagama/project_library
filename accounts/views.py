from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.http.response import HttpResponse as HttpResponse
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, RedirectView

from accounts.forms import SignUpForm


class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = 'accounts/pages/account_create.html'
    success_url = reverse_lazy('account:user_login')

    def get(self, request, *args, **kwargs):
        request.META['breadcrumbs'] = [
            {'name': 'Dashboard', 'url': reverse('library:dashboard')},
            {'name': 'User register', 'url': ''}]
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'User register'
        context['button_icon'] = 'bi bi-plus'
        context['button_name'] = 'Register'
        context['url_back'] = reverse('library:dashboard')
        return context

    def form_valid(self, form):
        messages.success(self.request, 'User registered successfully!')
        return super().form_valid(form)


class SignInView(LoginView):
    form_class = AuthenticationForm
    template_name = 'accounts/pages/account_login.html'
    redirect_authenticated_user = True
    success_url = reverse_lazy('library:dashboard')

    def get(self, request, *args, **kwargs):
        request.META['breadcrumbs'] = [
            {'name': 'Dashboard', 'url': reverse('library:dashboard')},
            {'name': 'User login', 'url': ''}]
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Login'
        context['button_icon'] = 'bi bi-box-arrow-in-left'
        context['button_name'] = 'Login'
        context['url_back'] = reverse('library:dashboard')

        return context


class SignOutView(RedirectView):
    pattern_name = 'account:user_login'

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(SignOutView, self).get(request, *args, **kwargs)
