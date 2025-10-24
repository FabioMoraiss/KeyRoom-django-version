from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from.models import *
from .forms import *

# Create your views here.

@login_required(login_url='home_page')
def main_page(request):
    credendials_user = Credential.objects.filter(user=request.user)
    return render(request, 'login/list.html', {
        'logins': credendials_user
    })

@login_required
def add_credendial(request):
    form = CredentialForm(user=request.user)
    return render(request, 'login/add.html', {
        'form': form
    })

