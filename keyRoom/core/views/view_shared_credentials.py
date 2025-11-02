from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from core.models import SharedCredential


@login_required(login_url='home_page')
def list_shared_credentials(request):
    shared_credentials = SharedCredential.objects.filter(shared_with=request.user).select_related('credential', 'credential__tag', 'owner')
    return render(request, 'shared_credentials/list.html', {
        'shared_credentials': shared_credentials
    })