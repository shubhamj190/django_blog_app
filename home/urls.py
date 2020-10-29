from django.contrib import admin
from django.urls import path, include
from .import views

urlpatterns = [
    path('', views.home),
    path('contact', views.contact),
    path('about', views.about),
    path('search', views.search),
    path('signup', views.signup),
    path('login', views.handleLogin),
    path('logout', views.handleLogout),

]