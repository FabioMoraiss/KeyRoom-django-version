from django.urls import path
from . import views

urlpatterns = [
path("register/", views.submit_register, name="submit_register"),
path("postlogin/", views.submit_login, name="submit_login"),
path('logout/', views.logout_view, name='logout'),
]