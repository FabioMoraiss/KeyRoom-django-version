from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_GET
import json
import secrets
import string
from typing import Optional


@login_required(login_url='home_page')
def password_generator(request):
    return render(request, 'password_generator/password_generator.html')


@require_GET
@login_required(login_url='home_page')
def generate_password(request):
    try:
        #Coleta e converte os parâmetros da Query String (GET)
        length = int(request.GET.get('length', 20))
        use_uppercase = request.GET.get('uppercase') == 'true'
        use_lowercase = request.GET.get('lowercase') == 'true'
        use_numbers = request.GET.get('numbers') == 'true'
        use_specials = request.GET.get('special_characters') == 'true'

        password = new_password(
            length=length,
            use_uppercase=use_uppercase,
            use_lowercase=use_lowercase,
            use_numbers=use_numbers,
            use_specials=use_specials
        )
        return JsonResponse({'success': True, 'password': password})
    except ValueError as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)

    except Exception as e:
        return JsonResponse({'success': False, 'error': 'Erro interno do servidor: ' + str(e)}, status=500)


def new_password(
    length: int = 20,
    use_uppercase: bool = True,
    use_lowercase: bool = True,
    use_numbers: bool = True,
    use_specials: bool = True,
    special_characters: Optional[str] = "!@#$%^&*"
) -> str:
    if length < 5:
        raise ValueError("length must be >= 5")

    categories = []
    if use_lowercase:
        categories.append(string.ascii_lowercase)
    if use_uppercase:
        categories.append(string.ascii_uppercase)
    if use_numbers:
        categories.append(string.digits)
    if use_specials:
        categories.append(special_characters if special_characters is not None else string.punctuation)

    if not categories:
        raise ValueError("At least one character category must be True")


    password_chars = [secrets.choice(cat) for cat in categories]

    all_chars = "".join(categories)
    remaining = length - len(password_chars)
    password_chars += [secrets.choice(all_chars) for _ in range(max(0, remaining))]

    secrets.SystemRandom().shuffle(password_chars)

    return "".join(password_chars)

