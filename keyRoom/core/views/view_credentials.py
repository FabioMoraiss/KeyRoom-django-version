from django.db import transaction
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from core.models import Credential
import pyotp

from core.models import *
from core.forms import *

# Create your views here.

@login_required(login_url='home_page')
def main_page(request):
    credentials_user = Credential.objects.filter(user=request.user)
    return render(request, 'credential/list.html', {
        'logins': credentials_user
    })

@login_required(login_url='home_page')
def add_credential(request):
    form = CredentialForm()
    return render(request, 'credential/add.html', {
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
            return render(request, 'credential/add.html', {
                'form': form
            })
    else:
        return redirect('add_credential')


@login_required(login_url='home_page')
def edit_credential(request,id):
    credential = get_object_or_404(Credential, id=id, user=request.user)
    form = CredentialForm(instance=credential)
    return render(request, 'credential/edit.html', {
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
            return render(request, 'credential/edit.html', {
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


@login_required
def get_otp(request, credential_id):
    try:
        cred = Credential.objects.get(id=credential_id, user=request.user)
    except Credential.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Credencial não encontrada.'
        }, status=404)

    if not cred.otpCode or cred.otpCode.strip() == '':
        return JsonResponse({
            'success': False,
            'error': 'Esta credencial não possui uma chave OTP configurada.'
        }, status=400)

    try:
        totp = pyotp.TOTP(cred.otpCode)
        code = totp.now()
        return JsonResponse({
            'success': True,
            'otp_code': code
        })
    except Exception as e:
        if e.args[0] == "Non-base32 digit found":
            return JsonResponse({
                'success': False,
                'error': 'Chave OTP inválida.'
            }, status=400)

        return JsonResponse({
            'success': False,
            'error': f'Erro ao gerar OTP: {str(e)}'
        }, status=500)



