from django.urls import path
from . import views

urlpatterns = [
    path('', views.logreg),
    path('login', views.login),
    path('registration', views.reg),
    path('logout', views.logout)
]