# python
import hashlib
from collections import defaultdict

import requests
import pyotp

from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse

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
    form = CredentialForm(user=request.user)
    return render(request, 'credential/add.html', {
        'form': form
    })


@login_required(login_url='home_page')
@transaction.atomic
def register_credential(request):
    if request.method == 'POST':
        form = CredentialForm(request.POST, user=request.user)
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
    form = CredentialForm(instance=credential, user=request.user)
    return render(request, 'credential/edit.html', {
        'form': form,
        'credential': credential
    })

@login_required(login_url='home_page')
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

@login_required(login_url='home_page')
def delete_credential(request,id):
    credential = get_object_or_404(Credential, id=id, user=request.user)
    if request.method == 'POST':
        credential.delete()
        messages.success(request, 'Credencial removida com sucesso!')
        return redirect('main_page')
    else:
        messages.error(request, 'Erro ao remover credencial.')
        return redirect('main_page')


@login_required(login_url='home_page')
def get_otp(request, credential_id):
    try:
        # Tenta pegar credencial do usuário logado
        cred = Credential.objects.get(id=credential_id, user=request.user)
    except Credential.DoesNotExist:
        # Se não for dono, tenta ver se está compartilhada com ele
        shared = SharedCredential.objects.filter(credential_id=credential_id, shared_with=request.user).first()
        if not shared:
            return JsonResponse({
                'success': False,
                'error': 'Credencial não encontrada ou não compartilhada com você.'
            }, status=404)
        cred = shared.credential

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


@login_required(login_url='home_page')
def pwned_credentials_view(request):
    credentials = Credential.objects.filter(user=request.user)

    prefix_map = defaultdict(lambda: defaultdict(list))
    for cred in credentials:
        pwd = getattr(cred, 'password', None) or getattr(cred, 'secret', None) or getattr(cred, 'login_password', None)
        if not pwd:
            continue
        sha1 = hashlib.sha1(pwd.encode('utf-8')).hexdigest().upper()
        prefix = sha1[:5]
        suffix = sha1[5:]
        prefix_map[prefix][suffix].append(cred)

    pwned = []
    session = requests.Session()
    session.headers.update({'User-Agent': 'keyRoom-App'})

    for prefix, suffixes in prefix_map.items():
        try:
            resp = session.get(f'https://api.pwnedpasswords.com/range/{prefix}', timeout=5)
            if resp.status_code != 200:
                continue
            lines = resp.text.splitlines()
            returned_suffixes = {line.split(':', 1)[0].strip().upper() for line in lines if line}
            for suffix, creds in suffixes.items():
                if suffix.upper() in returned_suffixes:
                    pwned.extend(creds)
        except requests.RequestException:
            continue

    if pwned:
        messages.warning(request, f'{len(pwned)} credenciais tiveram suas senhas vazadas na internet.')
    else:
        messages.success(request, 'Nenhuma senha de credencial foi vazada na internet.')

    return render(request, 'credential/list.html', {
        'logins': pwned
    })

