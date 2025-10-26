from django.urls import path
from . import views

urlpatterns = [
path('credentials/', views.main_page, name='main_page'),
path('credendials/add/', views.add_credential, name='add_credential'),
path('credentials/register', views.register_credential, name='register_credential'),
path('credentials/edit/<int:id>/', views.edit_credential, name='edit_credential'),
path('credentials/update/<int:id>/', views.update_credential, name='update_credential'),
path('credentials/delete/<int:id>/', views.delete_credential, name='delete_credential'),
path('credentials/<int:credential_id>/otp/', views.get_otp, name='get_otp'),


# path('credit_card/', views.credit_card, name='credit_card'),
# path('credit_cards/add/', views.add_credit_card, name='add_credit_card'),
# path('credit_cards/register', views.register_credit_card, name='register_credit_card'),
# path('credit_cards/edit/<int:id>/', views.edit_credit_card, name='edit_credit_card'),
# path('credit_cards/update/<int:id>/', views.update_credit_card, name='update_credit_card'),

]