from django.urls import path
from . import views

urlpatterns = [
path('credenditial/', views.main_page, name='main_page'),
path('credendials/add/', views.add_credential, name='add_credential'),
path('credentials/register', views.register_credential, name='register_credential'),
path('credentials/edit/<int:id>/', views.edit_credential, name='edit_credential'),
path('credentials/update/<int:id>/', views.update_credential, name='update_credential'),

]