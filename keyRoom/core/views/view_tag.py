from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404

from core.forms import TagForm
from core.models import CustomTag


@login_required(login_url='home_page')
def list_tags(request):
    tags = CustomTag.objects.filter(user=request.user)
    return render(request, 'tag/list.html',{
        'tags': tags
    })


@login_required(login_url='home_page')
def add_tag(request):
    form = TagForm(user=request.user)
    return render(request, 'tag/add.html', {
        'form': form
    })


@login_required(login_url='home_page')
@transaction.atomic
def register_tag(request):
    if request.method == 'POST':
        form = TagForm(request.POST, user=request.user)
        if form.is_valid():
            tag = form.save(commit=False)
            tag.user = request.user
            tag.save()

            messages.success(request, 'Tag cadastrada com sucesso!')
            return redirect('list_tags')
        else:
            messages.error(request, 'Erro ao cadastrar tag.')
            return render(request, 'tag/add.html', {
                'form': form
            })
    else:
        return redirect('add_tag')


@login_required(login_url='home_page')
def edit_tag(request, id):
    tag = get_object_or_404(CustomTag, id=id, user=request.user)
    form = TagForm(instance=tag, user=request.user)
    return render(request, 'tag/edit.html', {
        'form': form,
        'tag': tag
    })


@login_required(login_url='home_page')
def update_tag(request, id):
    tag = get_object_or_404(CustomTag, id=id, user=request.user)
    if request.method == 'POST':
        form = TagForm(request.POST, instance=tag, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tag atualizada com sucesso!')
            return redirect('list_tags')
        else:
            messages.error(request, 'Erro ao atualizar tag.')
            return render(request, 'tag/edit.html', {
                'form': form,
                'tag': tag
            })
    else:
        return redirect('edit_tag', id=id)

@login_required(login_url='home_page')
def delete_tag(request, id):
    tag = get_object_or_404(CustomTag, id=id, user=request.user)
    if request.method == 'POST':
        tag.delete()
        messages.success(request, 'Tag removida com sucesso!')
        return redirect('list_tags')
    else:
        messages.error(request, 'Erro ao remover tag.')
        return redirect('list_tags')
