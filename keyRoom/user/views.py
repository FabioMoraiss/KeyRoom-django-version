
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import redirect
from django.contrib import messages
import secrets
import string
from core.models import CustomUser

# Create your views here.

def submit_register(request):
    if request.method == 'POST':
        email = request.POST.get('registerEmail')
        password = request.POST.get('registerPassword')


        if password and email:
            # Verifica se já existe um usuário com o mesmo e-mail
            if CustomUser.objects.filter(username=email).exists():
                messages.error(request, "Email já cadastrado. Escolha outro ou tente fazer o login.")
                return redirect('signup_page')
            try:
                # Cria o novo usuário
                novo_usuario = CustomUser.objects.create_user(
                    username=email,
                    email=email,
                    password=password,
                    uniquiCode=generate_uniqui_code(email)
                )

                # Autentica e faz login
                user = authenticate(username=email, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('main_page')

                else:
                    messages.error(request, "Usuário criado, mas falha ao autenticar.")
                    return redirect('signup_page')
            except Exception as e:
                messages.error(request, f"Erro ao criar usuário: {e}")
                return redirect('signup_page')

        else:
            messages.error(request, "Algum campo está vazio.")
            return redirect('signup_page')

    else:

        messages.error(request, "Erro ao processar.")
        return redirect('signup_page')


def submit_login(request):
    if request.method == 'POST':
        email = request.POST.get('loginEmail')
        password = request.POST.get('loginPassword')

        if email and password:
            user = authenticate(username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('main_page')
            else:
                messages.error(request, "Credenciais inválidas. Verifique e tente novamente.")
        else:
            messages.error(request, "Preencha todos os campos.")
        return redirect('login_page')
    else:
        messages.error(request, "Erro ao processar requisição.")
        return redirect('login_page')

def logout_view(request):
    logout(request)
    messages.success(request, "Você saiu da sua conta com sucesso.")
    return redirect('home_page')

def generate_uniqui_code(email):
    return email + '+' + generate_random_code()


def generate_random_code(length: int = 12) -> str:
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))
