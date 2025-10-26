from django.urls import path
from .views import *
from .views import view_credentials, view_password_generator

urlpatterns = [
# CREDENTIALS URLS
path('credentials/', view_credentials.main_page, name='main_page'),
path('credendials/add/', view_credentials.add_credential, name='add_credential'),
path('credentials/register', view_credentials.register_credential, name='register_credential'),
path('credentials/edit/<int:id>/', view_credentials.edit_credential, name='edit_credential'),
path('credentials/update/<int:id>/', view_credentials.update_credential, name='update_credential'),
path('credentials/delete/<int:id>/', view_credentials.delete_credential, name='delete_credential'),
path('credentials/<int:credential_id>/otp/', view_credentials.get_otp, name='get_otp'),

#PASSWORD GENERATOR URLS
path('password_generator/', view_password_generator.password_generator, name='password_generator'),
path('generate_password/', view_password_generator.generate_password, name='generate_password'),


# path('credit_card/', views.credit_card, name='credit_card'),
# path('credit_cards/add/', views.add_credit_card, name='add_credit_card'),
# path('credit_cards/register', views.register_credit_card, name='register_credit_card'),
# path('credit_cards/edit/<int:id>/', views.edit_credit_card, name='edit_credit_card'),
# path('credit_cards/update/<int:id>/', views.update_credit_card, name='update_credit_card'),

]