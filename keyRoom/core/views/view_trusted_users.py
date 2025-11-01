from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from ..models import CustomUser, ListOfTrusedUers

@login_required(login_url='home_page')
def list_trusted_users(request):
    # Recupera ou cria a lista de confiáveis do usuário logado
    trusted_list, _ = ListOfTrusedUers.objects.get_or_create(owner=request.user)
    trusted_users = trusted_list.trusted_users.all()
    # Passa os usuários confiáveis para o template
    return render(request, 'trusted_list/list.html', {'trusted_users': trusted_users})


@login_required(login_url='home_page')
def add_trusted_user(request):
    if request.method == "POST":
        code = request.POST.get('trusted_code', '').strip()

        if not code:
            messages.error(request, "Por favor, digite um código de usuário.")
            return redirect('list_trusted_users')

        # Não pode adicionar ele mesmo!
        if code == request.user.uniquiCode:
            messages.warning(request, "Você não pode adicionar a si mesmo como usuário confiável.")
            return redirect('list_trusted_users')

        try:
            user_to_add = CustomUser.objects.get(uniquiCode=code)
        except CustomUser.DoesNotExist:
            messages.error(request, "Nenhum usuário encontrado com esse código.")
            return redirect('list_trusted_users')

        # Recupera ou cria a lista do usuário logado
        trusted_list, created = ListOfTrusedUers.objects.get_or_create(owner=request.user)

        # Verifica se já está na lista
        if trusted_list.trusted_users.filter(id=user_to_add.id).exists():
            messages.warning(request, "Este usuário já está na sua lista de usuários confiáveis.")
            return redirect('list_trusted_users')

        trusted_list.trusted_users.add(user_to_add)
        messages.success(request, "Usuário confiável adicionado com sucesso!")
        return redirect('list_trusted_users')
    #else
    return redirect('list_trusted_users')

@login_required(login_url='home_page')
def delete_trusted_user(request, user_id):
    if request.method == "POST":
        try:
            user_to_remove = CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            messages.error(request, "Usuário não encontrado.")
            return redirect('list_trusted_users')

        trusted_list, _ = ListOfTrusedUers.objects.get_or_create(owner=request.user)

        if trusted_list.trusted_users.filter(id=user_to_remove.id).exists():
            trusted_list.trusted_users.remove(user_to_remove)
            messages.success(request, "Usuário removido da sua lista de confiáveis.")
        else:
            messages.warning(request, "Esse usuário não está na sua lista de confiáveis.")

        return redirect('list_trusted_users')
    #else
    return redirect('list_trusted_users')