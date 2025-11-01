from django.contrib.auth.decorators import login_required

@login_required(login_url='home_page')
def list_shared_credentials(request):
    return None