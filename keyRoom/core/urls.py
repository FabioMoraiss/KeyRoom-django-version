from django.urls import path
from .views import *
from .views import view_credentials, view_password_generator, view_tag, view_shared_credentials, view_trusted_users

urlpatterns = [
# CREDENTIALS URLS
path('credentials/', view_credentials.main_page, name='main_page'),
path('credendials/add/', view_credentials.add_credential, name='add_credential'),
path('credentials/register', view_credentials.register_credential, name='register_credential'),
path('credentials/edit/<int:id>/', view_credentials.edit_credential, name='edit_credential'),
path('credentials/update/<int:id>/', view_credentials.update_credential, name='update_credential'),
path('credentials/delete/<int:id>/', view_credentials.delete_credential, name='delete_credential'),
path('credentials/<int:credential_id>/otp/', view_credentials.get_otp, name='get_otp'),
path('credentials/pwned/', view_credentials.pwned_credentials_view, name='pwned_credentials'),

#PASSWORD GENERATOR URLS
path('password_generator/', view_password_generator.password_generator, name='password_generator'),
path('generate_password/', view_password_generator.generate_password, name='generate_password'),

#TAGS
path('tags/', view_tag.list_tags, name='list_tags'),
path('tags/add/', view_tag.add_tag, name='add_tag'),
path('tags/register/', view_tag.register_tag, name='register_tag'),
path('tags/edit/<int:id>/', view_tag.edit_tag, name='edit_tag'),
path('tags/update/<int:id>/', view_tag.update_tag, name='update_tag'),
path('tags/delete/<int:id>/', view_tag.delete_tag, name='delete_tag'),

#SHERED CREDENTIALS
path('shared_credentials/', view_shared_credentials.list_shared_credentials, name='list_shared_credentials'),


#TRUSTED USERS
path('trusted_users/', view_trusted_users.list_trusted_users, name='list_trusted_users'),
path('trusted_users/add/', view_trusted_users.add_trusted_user, name='add_trusted_user'),
path('trusted_users/delete/', view_trusted_users.delete_trusted_user, name='delete_trusted_user'),


# path('credit_card/', views.credit_card, name='credit_card'),
# path('credit_cards/add/', views.add_credit_card, name='add_credit_card'),
# path('credit_cards/register', views.register_credit_card, name='register_credit_card'),
# path('credit_cards/edit/<int:id>/', views.edit_credit_card, name='edit_credit_card'),
# path('credit_cards/update/<int:id>/', views.update_credit_card, name='update_credit_card'),

]