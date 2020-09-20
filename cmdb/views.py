from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


@login_required
def index(request):
    if request.user.is_staff:
        return redirect(settings.URL_PATH_PREFIX + 'admin/')
    return render(request, 'cmdb/index.html')
