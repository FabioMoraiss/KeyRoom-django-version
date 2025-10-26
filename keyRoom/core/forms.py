from django import forms
from django.forms import modelformset_factory
from .models import *


class CredentialForm(forms.ModelForm):
    class Meta:
        model = Credential
        fields = ['title', 'username', 'password', 'url', 'otpCode', 'notes', 'tag']
    widgets = {
        'title': forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Título da credencial...'
        }),
        'username': forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nome de usuário...'
        }),
        'password': forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Senha...'
        }),
        'url': forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'URL da credencial...'
        }),
        'otpCode': forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Código OTP...'
        }),
        'notes': forms.Textarea(attrs={
            'rows': 3,
            'class': 'form-control',
            'placeholder': 'Notas adicionais...'
        }),
        'tag': forms.Select(attrs={
            'class': 'form-control',
            'placeholder': 'Selecione uma Tag'
        }),
    }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(CredentialForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['tag'].queryset = CustomTag.objects.filter(user=user)
            self.fields['tag'].empty_label = "Nenhuma tag"
