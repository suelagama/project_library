from django.urls import path

from . import views

app_name = 'account'

urlpatterns = [
    path('user/create', views.SignUpView.as_view(), name='user_create'),
    path('user/login', views.SignInView.as_view(), name='user_login'),
    path('user/logout', views.SignOutView.as_view(), name='user_logout'),
]
