#!/usr/bin/python3.8
import sys, os, django
BASE_DIR = os.path.dirname(sys.executable)
sys.path.append("/home/carmsanc/MapaVirtual/BACKEND/ServidorMapaVirtual/")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'ServidorMapaVirtual.settings')

sys.path.append("/home/carmsanc/MapaVirtual/BACKEND/ServidorMapaVirtual/")
django.setup()

import datetime
import schedule
import time
from django.http import HttpResponse
from pyfcm import FCMNotification
from serviciosBackend.models import Favoritos, TokenDevice
from serviciosBackend.serializers import FavoritosFullSerializer
from dotenv import load_dotenv

load_dotenv()
def enviarPush(reg_id,title,message, difunto):
    push_service = FCMNotification(api_key=os.getenv("FCM_KEY"))
    data_message={
        "title": title,
        "message": message,
        "difunto": difunto
    }
    result = push_service.notify_single_device(
                                    registration_id=reg_id,
                                    message_title=title,
                                    message_body=message,
                                    data_message = data_message
                                )
    print(result)
    return result

def notificacion_cumpleanos():
    print("cumple")
    today_day = datetime.date.today().day
    today_month = datetime.date.today().month
    qs = Favoritos.objects.filter(id_difunto__fecha_nacimiento__day = today_day, id_difunto__fecha_nacimiento__month= today_month)
    for i in list(qs):
        i=FavoritosFullSerializer(i)
        title = "Recordatorio de cumpleanos de " + i.data['id_difunto']['nombre'] +' '+ i.data['id_difunto']['apellido']
        message = "Recuerda a tu ser querido en este dia. Dejale un mensaje."
        user = TokenDevice.objects.filter(id_user= i.data['id_usuario']).values('token_device')
        enviarPush(user[0]['token_device'], title, message, i.data['id_difunto'])
        print(user[0]['token_device'])
        print(i.data['id_difunto'])
        print(title)
    return HttpResponse(list(qs))

def aniversario_defuncion():
    print("muerte")

    today_day = datetime.date.today().day
    today_month = datetime.date.today().month

    qs = Favoritos.objects.filter(id_difunto__fecha_difuncion__day = today_day, id_difunto__fecha_difuncion__month= today_month)
    for i in list(qs):
        i = FavoritosFullSerializer(i)
        title = "Aniversario de defuncion de " + i.data['id_difunto']['nombre'] + ' ' + i.data['id_difunto'][
            'apellido']
        message = "Recuerda a tu ser querido en este dia. Dejale un mensaje."
        user = TokenDevice.objects.filter(id_user=i.data['id_usuario']).values('token_device')
        enviarPush(user[0]['token_device'], title, message, i.data['id_difunto'])
        print(user[0]['token_device'])
        print(title)

    return HttpResponse(list(qs))

schedule.every().day.at("01:56").do(notificacion_cumpleanos)
schedule.every().day.at("01:56").do(aniversario_defuncion)

while True:
    schedule.run_pending()
    time.sleep(1)
