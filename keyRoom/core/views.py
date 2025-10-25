from django.db import transaction
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from.models import *
from .forms import *

# Create your views here.

@login_required(login_url='home_page')
def main_page(request):
    credentials_user = Credential.objects.filter(user=request.user)
    return render(request, 'login/list.html', {
        'logins': credentials_user
    })

@login_required(login_url='home_page')
def add_credential(request):
    form = CredentialForm()
    return render(request, 'login/add.html', {
        'form': form
    })


@login_required(login_url='home_page')
@transaction.atomic
def register_credential(request):
    if request.method == 'POST':
        form = CredentialForm(request.POST)
        if form.is_valid():
            credential = form.save(commit=False)
            credential.user = request.user
            credential.save()

            messages.success(request, 'Credencial cadastrada com sucesso!')
            return redirect('main_page')
        else:
            messages.error(request, 'Erro ao cadastrar credencial.')
            return render(request, 'login/add.html', {
                'form': form
            })
    else:
        return redirect('add_credential')


@login_required(login_url='home_page')
def edit_credential(request,id):
    credential = get_object_or_404(Credential, id=id, user=request.user)
    form = CredentialForm(instance=credential)
    return render(request, 'login/edit.html', {
        'form': form,
        'credential': credential
    })

def update_credential(request,id):
    credential = get_object_or_404(Credential, id=id, user=request.user)
    if request.method == 'POST':
        form = CredentialForm(request.POST, instance=credential)
        if form.is_valid():
            form.save()
            messages.success(request, 'Credencial atualizada com sucesso!')
            return redirect('main_page')
        else:
            messages.error(request, 'Erro ao atualizar credencial.')
            return render(request, 'login/edit.html', {
                'form': form,
                'credential': credential
            })
    else:
        return redirect('edit_credential', id=id)


def delete_credential(request,id):
    credential = get_object_or_404(Credential, id=id, user=request.user)
    if request.method == 'POST':
        credential.delete()
        messages.success(request, 'Credencial removida com sucesso!')
        return redirect('main_page')
    else:
        messages.error(request, 'Erro ao remover credencial.')
        return redirect('main_page')



