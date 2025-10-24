from django.urls import path
from . import views

urlpatterns = [
path('credendials/', views.main_page, name='main_page'),
path('add_credendial/', views.add_credendial, name='add_credendial'),

]