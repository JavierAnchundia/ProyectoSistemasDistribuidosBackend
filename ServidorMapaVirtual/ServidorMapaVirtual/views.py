from django.http import  HttpResponse
from django.shortcuts import render
from .config import config_backend

# 10/11/2020
def RecuperarContrasena(request, id_user, token):
    url_backend = config_backend.get('url_backend_image')
    namePage = config_backend.get('name_page')
    return render(request, 'recuperarContrasena.html', {
        "user": id_user,
        "token": token,
        "url_backend": url_backend,
        "namePage": namePage
    })

