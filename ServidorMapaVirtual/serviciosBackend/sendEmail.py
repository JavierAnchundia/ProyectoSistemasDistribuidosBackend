from django.conf import settings
from django.core.mail import send_mail
from ServidorMapaVirtual.config import config_backend
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .serializers import UserProfileSerializer
from smtplib import SMTP

def enviarEmailToUserContrasena(usuarioObj):
    token_generator = PasswordResetTokenGenerator()
    token = token_generator.make_token(usuarioObj)
    usuario = UserProfileSerializer(usuarioObj)
    subject = '¡Recuperar Contraseña!'
    message = 'Para cambiar su contraseña seguir el siguiente link: \n' + config_backend.get(
        'url_change_password') + str(usuario['id'].value) + "/" + str(token) + "/"
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [usuario['email'].value, ]
    try:
        send_mail(subject, message, email_from, recipient_list)
    except SMTPException:
        return 0
    return 1