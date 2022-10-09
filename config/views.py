from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required(login_url="core:login")
def error_404(request, exception):
    return render(request, "core/404.html")


@login_required(login_url="core:login")
def error_400(request, exception):
    return render(request, "core/400.html")


@login_required(login_url="core:login")
def error_500(request):
    return render(request, "core/500.html")


@login_required(login_url="core:login")
def error_503(request):
    return render(request, "core/503.html")
