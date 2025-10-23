from django.urls import path
from django.views.generic import RedirectView

from . import views

urlpatterns = [
    path("login/", views.login, name="login_page"),
    path("signup/", views.signup, name="signup_page"),
    path("", RedirectView.as_view(pattern_name="login_page"), name="home_page"),
    

]