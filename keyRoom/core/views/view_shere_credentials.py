from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.shortcuts import render, get_object_or_404
from ..models import Credential, CustomUser, SharedCredential, ListOfTrustedUsers


@login_required(login_url='home_page')
@csrf_exempt
def share_credential(request, id):
    if request.method != 'POST':
        return JsonResponse({'error': 'Método não suportado'}, status=405)

    user = request.user
    try:
        credential = Credential.objects.get(id=id, user=user)
    except Credential.DoesNotExist:
        return JsonResponse({'error': 'Credencial não encontrada ou não pertence ao usuário'}, status=403)

    # Carrega lista de ids do body
    try:
        body = json.loads(request.body)
        user_ids = body.get('user_ids', [])
        if not isinstance(user_ids, list):
            return JsonResponse({'error': 'user_ids deve ser uma lista'}, status=400)
    except Exception:
        return JsonResponse({'error': 'Body inválido'}, status=400)

    # Pega lista de confiáveis do usuário logado
    try:
        trusted_list = user.trusted_list
        trusted_users_ids = set(trusted_list.trusted_users.values_list('id', flat=True))
    except ListOfTrustedUsers.DoesNotExist:
        trusted_users_ids = set()

    # Filtra somente ids confiáveis
    valid_user_ids = [uid for uid in user_ids if uid in trusted_users_ids]

    # Atualiza compartilhamentos
    # 1. Remove os que não estão mais na lista
    SharedCredential.objects.filter(owner=user, credential=credential).exclude(
        shared_with_id__in=valid_user_ids).delete()

    # 2. Adiciona os que faltam
    for uid in valid_user_ids:
        SharedCredential.objects.get_or_create(
            owner=user,
            credential=credential,
            shared_with_id=uid
        )

    return JsonResponse({
        'success': True,
        'shared_with': valid_user_ids,
        'not_shared': [uid for uid in user_ids if uid not in trusted_users_ids],
    })

@login_required(login_url='home_page')
def list_share_credentials(request):
    credentials = Credential.objects.filter(user=request.user).select_related('tag').prefetch_related('shared_with__shared_with')
    return render(request, 'share_credentials/list.html', {'credentials': credentials})

@login_required(login_url='home_page')
def edit_share_credential(request, id):
    user = request.user
    credential = get_object_or_404(Credential, id=id, user=user)
    trusted_users = user.trusted_list.trusted_users.all() if hasattr(user, 'trusted_list') else []
    shared_with_ids = list(SharedCredential.objects.filter(owner=user, credential=credential).values_list('shared_with_id', flat=True))
    return render(request, 'share_credentials/edit.html', {
        'credential': credential,
        'trusted_users': trusted_users,
        'shared_with_ids': shared_with_ids,
    })