from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required(login_url='home_page')
def list_trusted_users(request):
    return render(request, 'trusted_list/list.html')


def add_trusted_user(request):
    return None


def delete_trusted_user(request):
    return None