from django.http import HttpResponse, Http404
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.permissions import (AllowAny, IsAuthenticated)
from .permissions import IsLoggedInUserOrAdmin, IsAdminUser
from django.shortcuts import get_object_or_404
from rest_framework.renderers import (HTMLFormRenderer, JSONRenderer,BrowsableAPIRenderer,)
from .models import User, Empresa, Red_social, Camposanto, Punto_geolocalizacion, Sector, Tipo_sepultura, \
    Responsable_difunto, Difunto, Permiso, User_permisos, Homenajes, H_mensaje, H_imagen, H_video, H_audio, \
    Historial_rosas, TokenDevice, Favoritos, Paquetes, Notificaciones, Contacto, H_youtube
from .serializers import UserProfileSerializer, EmpresaSerializer, Red_socialSerializer, CamposantoSerializer, \
    Punto_geoSerializer, SectorSerializer, Tipo_sepulturaSerializer, Responsable_difuntoSerializer, DifuntoSerializer, \
    PermisoSerializer, User_permisosSerializer, Info_permisosSerializer, HomenajeSerializer, H_mensajeSerializer, \
    H_imagenSerializer, H_videoSerializer, H_audioSerializer, HomenajeSimpleSerializer, Historial_rosasSerializer, \
    Log_RosasSerializer, Token_DeviceSerializer, FavoritosSerializer, FavoritosFullSerializer, PaquetesSerializer, \
    NotificacionSerializer, H_youtubeSerializer, ContactoSerializer, Contacto_userSerializer
from .servicioFacebook import Facebook
from .get_jwt_user import Json_web_token
import base64
from django.core.files.base import ContentFile
from django.conf import settings
from django.core.mail import send_mail
from ServidorMapaVirtual.config import config_backend
from django.core.files.storage import default_storage
# para token reset password
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .sendEmail import enviarEmailToUserContrasena
# para enviar notificaciones
from .sendPushNotification import sendNotificaction
from threading import Thread
import datetime

'''API Rest get unico, get list, post y put para Camposanto'''
class CamposantoView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request, format=None):
        camposantoObj = Camposanto.objects.all()
        serializer = CamposantoSerializer(camposantoObj, many=True)
        return Response(serializer.data)
    def post(self, request, format=None):
        serializer = CamposantoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CamposantoViewSet(APIView):
    def get_object(self, pk):
        try:
            return Camposanto.objects.get(id_camposanto=pk)
        except Camposanto.DoesNotExist:
            raise Http404
    def get(self, request, pk, format=None):
        camposantoObj = self.get_object(pk)
        serializer = CamposantoSerializer(camposantoObj)
        return Response(serializer.data)
    def put(self, request, pk, format=None):
        camposantoObj = self.get_object(pk)
        serializer = CamposantoSerializer(camposantoObj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

'''API Rest getList, post y put para Red_social'''
class Red_socialPost(APIView):
    def post(self, request, format=None):
        serializer = Red_socialSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Red_socialListGet(APIView):
    def get(self, request, id_camp, format=None):
        red_socialObj = Red_social.objects.filter(id_camposanto=id_camp)
        serializer = Red_socialSerializer(red_socialObj, many=True)
        return Response(serializer.data)

class Red_socialPut(APIView):
    def get_objects(self, id_red):
        try:
            return Red_social.objects.get(id_camposanto=id_red)
        except Red_social.DoesNotExist:
            raise Http404
    def put(self, request, id_red, format=None):
        red_socialObj  = self.get_object(id_red)
        serializer = Red_socialSerializer(red_socialObj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

'''API Rest post y getList para Geolocalizacion'''
class GeolocalizacionPost(APIView):
    def post(self, request, format=None):
        serializer = Punto_geoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GeolocalizacionListGet(APIView):
    def get(self, request, id_camp, format=None):
        geolocalizacionObj = Punto_geolocalizacion.objects.filter(id_camposanto=id_camp)
        serializer = Punto_geoSerializer(geolocalizacionObj, many=True)
        return Response(serializer.data)

class GeolocalizacionDelete(APIView):
    def get_object(self, id_punto):
        try:
            return Punto_geolocalizacion.objects.get(id_punto=id_punto)
        except Punto_geolocalizacion.DoesNotExist:
            raise Http404
    def delete(self, request, id_punto, format=None):
        geolocalizacionObj = self.get_object(id_punto)
        geolocalizacionObj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

'''API Rest get para Sector'''
class SectorListGet(APIView):
    def get(self, request, id_camp, format=None):
        sectorObj = Sector.objects.filter(id_camposanto=id_camp)
        serializer = SectorSerializer(sectorObj, many=True)
        return Response(serializer.data)

'''API Rest get para Tipo Sepultura'''
class Tipo_sepulturaListGet(APIView):
    def get(self, request, id_camp, format=None):
        tiposObj = Tipo_sepultura.objects.filter(id_camposanto=id_camp)
        serializer = Tipo_sepulturaSerializer(tiposObj, many=True)
        return Response(serializer.data)

'''API Rest get unico, get list, post y put para Difunto'''
class DifuntoView(APIView):
    def post(self, request, format=None):
        serializer = DifuntoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#API para obtener la informacion de un difunto y actualizarla
class DifuntoViewSet(APIView):
    def get_object(self, pk):
        try:
            return Difunto.objects.get(id_difunto=pk)
        except Difunto.DoesNotExist:
            raise Http404
    def get(self, request, pk, format=None):
        difuntoObj = self.get_object(pk)
        serializer = DifuntoSerializer(difuntoObj)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        difuntoObj = self.get_object(pk)
        serializer = DifuntoSerializer(difuntoObj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DifuntoListGet(APIView):
    def get(self, request, id_camp, format=None):
        difuntosObj = Difunto.objects.filter(Q(id_camposanto=id_camp))
        serializer = DifuntoSerializer(difuntosObj, many=True)
        return Response(serializer.data)

class DifuntoListFilteredGet(APIView):
    def get(self, request, id_camp, nombre, apellido, desde, hasta, lapida, sector, sepultura, format=None):
        difuntosObj = Difunto.objects.filter(id_camposanto=id_camp)
        if (nombre != 'null'):
            difuntosObj = Difunto.objects.filter(nombre=nombre)
        if (apellido != 'null'):
            difuntosObj = Difunto.objects.filter(apellido=apellido)
        if ((desde != 'null') & (hasta != 'null')):
            # date_1 = datetime.datetime.strptime((hasta), "%Y-%m-%d")
            # end_date = date_1 + datetime.timedelta(days=1)
            difuntosObj = difuntosObj.filter(fecha_difuncion__range=(desde, hasta))
        if (lapida != 'null'):
            difuntosObj = difuntosObj.filter(no_lapida=lapida)
        if (sector != 'null'):
            difuntosObj = difuntosObj.filter(id_sector=sector)
        if (sepultura != 'null'):
            difuntosObj = difuntosObj.filter(id_tip_sepultura=sepultura)
        serializer = DifuntoSerializer(difuntosObj, many=True)
        return Response(serializer.data)


'''API Rest get unico, post para Responsable'''
class Responsable_difuntoView(APIView):
    def post(self, request, format=None):
        serializer = Responsable_difuntoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Responsable_difuntoViewSet(APIView):
    def get_object(self, id_difunto):
        try:
            return Responsable_difunto.objects.get(id_difunto=id_difunto)
        except Responsable_difunto.DoesNotExist:
            raise Http404
    def get(self, request, id_difunto, format=None):
        responsableObj = self.get_object(id_difunto)
        serializer = Responsable_difuntoSerializer(responsableObj)
        return Response(serializer.data)

    def put(self, request, id_difunto, format=None):
        responsableObj = self.get_object(id_difunto)
        serializer = Responsable_difuntoSerializer(responsableObj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

'''API Rest get list y get id para empresa'''
class EmpresasView(APIView):
    def get(self, request, format=None):
        empresaObj = Empresa.objects.all()
        serializer = EmpresaSerializer(empresaObj, many=True)
        return Response(serializer.data)

class EmpresaViewSet(APIView):
    def get_object(self, pk):
        try:
            return Empresa.objects.get(id_empresa=pk)
        except Empresa.DoesNotExist:
            raise Http404
    def get(self, request, pk, format=None):
        empresaObj = self.get_object(pk)
        serializer = EmpresaSerializer(empresaObj)
        return Response(serializer.data)
    def put(self, request, pk, format=None):
        empresaObj = self.get_object(pk)
        serializer = EmpresaSerializer(empresaObj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    # permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer

    def get_permissions(self):
        permission_classes = []
        if self.request.method == 'GET':
            permission_classes = [AllowAny ]
        if self.action == 'create':
            permission_classes = [AllowAny]
        elif self.action == 'retrieve' or self.action == 'update' or self.action == 'partial_update':
            permission_classes = [IsLoggedInUserOrAdmin]
        elif self.action == 'list' or self.action == 'destroy':
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

#Para poder obtener informacion de un usuario y poder actualizarlo
class UsuarioViewGet(APIView):
    permission_classes = (IsAuthenticated,)
    def get_object(self, username):
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            raise Http404
    def get(self, request, username, format=None):
        usuarioObj = self.get_object(username)
        serializer = UserProfileSerializer(usuarioObj)
        return Response(serializer.data)

    def put(self, request, username, format = None):
        usuarioObj = self.get_object(username)
        serializer = UserProfileSerializer(usuarioObj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()

            if 'password' in request.data:
                usuarioObj.set_password(request.data['password'])
                usuarioObj.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# obtener lista de usuarios por camposanto
class UsuarioGetCamposanto(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request, id_camp, format=None):
        usuariosObj = User.objects.filter(id_camposanto=id_camp)
        serializer = UserProfileSerializer(usuariosObj, many=True)
        return Response(serializer.data)

# para validar en el registro de usuarios si un username o email por camposanto ya esta usado
class UsuarioGetAll(APIView):
    def get(self, request, format=None):
        usuarioObj = User.objects.all()
        for userO in usuarioObj:
            userO.first_name = ''
            userO.last_name = ''
            userO.telefono = ''
            userO.genero = ''
            userO.direccion = ''
            userO.staff = ''
            userO.tipo_usuario = ''
        serializer = UserProfileSerializer(usuarioObj, many=True)
        return Response(serializer.data)

# Api para obtener permisos
class PermisoView(APIView):
    def get(self, request, format=None):
        permisoObj = Permiso.objects.all()
        serializer = PermisoSerializer(permisoObj, many=True)
        return Response(serializer.data)

# Obtener la informacion de un Permiso usando su id
class Permiso_Info(APIView):
    def get_object(self,pk):
        try:
            return Permiso.objects.get(id_permiso=pk)
        except Permiso.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        permisoObj = self.get_object(pk)
        serializer = PermisoSerializer(permisoObj)
        return Response(serializer.data)
class Info_Permiso_User(APIView):
    def get_object(self,pk):
        try:
            return User_permisos.objects.filter(Q(id_user=pk))
        except Permiso.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        permisoObj = self.get_object(pk)
        serializer = Info_permisosSerializer(permisoObj, many=True)
        return Response(serializer.data)

# Obtener permisos de un usuario o eliminar los permisos de un usuario
class User_PermisosGet(APIView):

    def get_object(self, pk):
        try:
            return User_permisos.objects.get(id_difunto=pk)
        except Difunto.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        user_permisosObj = User_permisos.objects.filter(Q(id_user=id))
        serializer = User_permisosSerializer(user_permisosObj, many=True)
        return Response(serializer.data)

    def delete(self, request, id, format=None):
        user_permisosObj = (User_permisos.objects.filter(Q(id_user=id))).delete()
        return Response(user_permisosObj)

# Crear usuarios con sus respectivos permisos
class User_PermisosPost(APIView):
    # permission_classes = (IsAuthenticated,)
    def post(self, request, format=None):
        serializer = User_permisosSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Api para crear usuario de facebook o validar que existe para enviar el token
class Create_User_Facebook(APIView):
    def post(self, request, format=None):
        access_token = request.data['access_token']
        # instancia de la clase facebook
        f = Facebook()
        # se obtienen los datos a traves de la api de facebook
        data = f.get_info_facebook(access_token)
        # instancia de la clase Json_web_token
        jwt = Json_web_token()
        # validar que no existe dicho usuarios guardado
        usuario_validate = self.obtener_User(data['username'])

        if usuario_validate:
            token = jwt.get_token_user(usuario_validate)
            return Response(token, status=status.HTTP_201_CREATED)
        else:
            user_serializer = UserProfileSerializer(data= data)
            if user_serializer.is_valid():
                user_save = user_serializer.save()
                if user_save :
                    # instancia de la clase Json_web_token
                    jwt = Json_web_token()
                    token = jwt.get_token_user(user_save)
                return Response(token, status=status.HTTP_201_CREATED)
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def obtener_User(self, username):
        try:
            return User.objects.get(username = username)
        except User.DoesNotExist:
            return None

# Obtener homenajes por id de difunto
class Homenaje_Get(APIView):
    def get(self, request, id, format=None):
        user_homenajesObj = Homenajes.objects.filter(id_difunto=id, estado=True)
        serializer = HomenajeSerializer(user_homenajesObj, many=True)
        return Response(serializer.data)

# Crear Homenaje
class Homenaje_Set(APIView):
    permission_classes = (IsAuthenticated,)

    serializer_class = HomenajeSimpleSerializer
    renderer_classes = (BrowsableAPIRenderer, JSONRenderer, HTMLFormRenderer)
    def post(self, request, format=None):
        serializer = HomenajeSimpleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Obtener contenido de imagen para homenaje
class Himagen_Get(APIView):
    def get(self, request, id, format=None):
        user_HimagenObj = H_imagen.objects.filter(Q(id_homenaje=id))
        serializer = H_imagenSerializer(user_HimagenObj, many=True)
        return Response(serializer.data)

#Borrado de homenaje imagen
class HImagen_Delete(APIView):
    def get_object(self, id):
        try:
            return H_imagen.objects.get(id_imagen=id)
        except H_imagen.DoesNotExist:
            raise Http404
    def delete(self, request, id_imagen, format=None):
        imgObj = self.get_object(id_imagen)
        seri = H_imagenSerializer(imgObj)
        path = seri['imagen'].value[7:]
        imgObj.delete()
        default_storage.delete(path)
        return Response(status=status.HTTP_200_OK)

# Obtener contenido de texto para homenaje
class Htexto_Get(APIView):
    def get(self, request, id, format=None):
        user_HtextoObj = H_mensaje.objects.filter(Q(id_homenaje=id))
        serializer = H_mensajeSerializer(user_HtextoObj, many=True)
        return Response(serializer.data)

#Borrado de homenaje texto
class HTexto_Delete(APIView):
    def get_object(self, id):
        try:
            return H_mensaje.objects.get(id_mensaje=id)
        except H_mensaje.DoesNotExist:
            raise Http404
    def delete(self, request, id_mensaje, format=None):
        mensajeObj = self.get_object(id_mensaje)
        mensajeObj.delete()
        return Response(status=status.HTTP_200_OK)

# Crear contenido de texto para homenaje
class Htexto_Set(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        serializer = H_mensajeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Crear contenido de imagen para homenaje
class Himagen_Set(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        # base_img = 'data:image/png;base64'
        if(request.data['img_base64'] != "none"):
            format, imgstr = request.data['img_base64'].split(';base64,')
            ext = format.split('/')[-1]
            imag = ContentFile(base64.b64decode(imgstr), name='h_img_' + request.data['nombre_file'])
            data = {
                'mensaje': request.data['mensaje'],
                'imagen': imag
            }
            serializer = H_imagenSerializer(data=data)
        else:
            serializer = H_imagenSerializer(data=request.data)
        # serializer = H_imagenSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Crear contenido de video para homenaje
class Hvideo_Set(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        serializer = H_videoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Crear contenido pagado de video
class Hyoutube_Set(APIView):
    #permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        serializer = H_youtubeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Obtener contenido de audio para homenaje
class Haudio_Get(APIView):
    def get(self, request, id, format=None):
        Haudio_obj = H_audio.objects.filter(Q(id_homenaje=id))
        serializer = H_audioSerializer(Haudio_obj, many=True)
        return Response(serializer.data)

#Borrado de homenaje AUDIO
class HAudio_Delete(APIView):
    def get_object(self, id):
        try:
            return H_audio.objects.get(id_audio=id)
        except H_audio.DoesNotExist:
            raise Http404
    def delete(self, request, id_audio, format=None):
        audioObj = self.get_object(id_audio)
        seri = H_audioSerializer(audioObj)
        path = seri['audio'].value[7:]
        audioObj.delete()
        default_storage.delete(path)
        return Response(status=status.HTTP_200_OK)

# Crear contenido de audio para homenaje
class Haudio_Set(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        serializer = H_audioSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Borrado de homenaje VIDEO
class HVideo_Delete(APIView):
    def get_object(self, id):
        try:
            return H_video.objects.get(id_video=id)
        except H_video.DoesNotExist:
            raise Http404
    def delete(self, request, id_video, format=None):
        videoObj = self.get_object(id_video)
        seri = H_videoSerializer(videoObj)
        path = seri['video'].value[7:]
        videoObj.delete()
        default_storage.delete(path)
        return Response(status=status.HTTP_200_OK)

# Actualizar contador de rosas
class AmountPartialUpdateView(APIView):

    def patch(self, request, pk, num_rosas):
        model = get_object_or_404(Difunto, pk=pk)
        data = {"num_rosas": model.num_rosas + int(num_rosas)}
        serializer = DifuntoSerializer(model, data=data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Obtener registro en hitorial de rosas
class Historial_rosasGet(APIView):
    def get(self, request, id, format=None):
        historial_Obj = Historial_rosas.objects.filter(Q(id_difunto=id))
        serializer = Log_RosasSerializer(historial_Obj, many=True)
        return Response(serializer.data)

# Guardar registro de rosa
class Historial_rosasSet(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        serializer = Historial_rosasSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# actualizar imagen de perfil desde movil
class ImageUserUpdate(APIView):
    def get_object(self, id):
        try:
            return User.objects.get(id=id)
        except User.DoesNotExist:
            raise Http404
    def put(self, request, id, format=None):
        usuarioObj = self.get_object(id)
        if ('img_base64' in request.data):
            format, imgstr = request.data['img_base64'].split(';base64,')
            ext = format.split('/')[-1]
            nameFile = UserProfileSerializer(usuarioObj)['username'].value + "-" + request.data['nombre_file']
            imag = ContentFile(base64.b64decode(imgstr), name=nameFile)
            request.data._mutable = True

            del request.data['img_base64']
            del request.data['nombre_file']
            if 'delete_img' in request.data:
                pathImgDel = request.data['delete_img']
                path = pathImgDel[7:]
                default_storage.delete(path)
                del request.data['delete_img']

            request.data['image_perfil'] = imag
            request.data._mutable = False
            serializer = UserProfileSerializer(usuarioObj, data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors,  status=status.HTTP_400_BAD_REQUEST)

#obtener usuario por id
class UsuarioGetById(APIView):
    permission_classes = (IsAuthenticated,)
    def get_object(self, id):
        try:
            return User.objects.get(id=id)
        except User.DoesNotExist:
            raise Http404
    def get(self, request, id, format=None):
        usuarioObj = self.get_object(id)
        serializer = UserProfileSerializer(usuarioObj)
        return Response(serializer.data)

# Para recuperar la contraseña 10/11/2020
class EnviarCorreoContrasena(APIView):
    def get(self, request, email, id_camp, format=None):
        usuariosObj = User.objects.filter(Q(id_camposanto=id_camp) & Q(email=email))
        if(usuariosObj.exists()):
            retorno = enviarEmailToUserContrasena(usuariosObj[0])
            if retorno == 1:
                return Response(data={'status': "success"}, status=status.HTTP_200_OK)
            else:
                return Response(
                    data={'status': "SMTPException", "message": "No se ha podido enviar el mensaje"},
                    status=status.HTTP_400_BAD_REQUEST)
        return Response(data={'status': "error"}, status=status.HTTP_404_NOT_FOUND)

# Enviar correo para usuarios admin
class EnviarCorreoContrasenaAdmin(APIView):
    def get_object(self, username):
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            raise Http404
    def get(self, request, username, format=None):
        usuarioObj = self.get_object(username)
        if usuarioObj:
            serializerUser = UserProfileSerializer(usuarioObj)
            tipo_user = serializerUser['tipo_usuario'].value
            if(tipo_user == "ha" or tipo_user == "ad" or tipo_user == "su"):
                retorno = enviarEmailToUserContrasena(usuarioObj)
                if retorno == 1 :
                    return Response(data={'status': "success"}, status=status.HTTP_200_OK)
                else:
                    return Response(
                        data={'status': "SMTPException", "message": "No se ha podido enviar el mensaje"},
                        status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(
                    data={'status': "Not Found", "message": "Tipo de usuario no válido"},
                    status=status.HTTP_404_NOT_FOUND)
        return Response(data={'status': "error"}, status=status.HTTP_404_NOT_FOUND)

# Para recuperar la contraseña 10/11/2020
class ActualizarContrasena(APIView):
    def get_object(self, id):
        try:
            return User.objects.get(id=id)
        except User.DoesNotExist:
            raise Http404
    def put(self, request, id, format=None):
        usuarioObj = self.get_object(id)
        token = request.data['token']
        token_generator = PasswordResetTokenGenerator()
        is_valid_token = token_generator.check_token(usuarioObj, token)
        if(is_valid_token):
            if 'password' in request.data:
                usuarioObj.set_password(request.data['password'])
                usuarioObj.save()
                return Response(data={'status': "success"}, status=status.HTTP_200_OK)
        return Response(data={'status': "error"}, status=status.HTTP_400_BAD_REQUEST)


class TokenDevicePost(APIView):
    def post(self, request, format=None):
        tokenList = TokenDevice.objects.filter(Q(token_device=request.data['token_device']) & Q(plataform=request.data['plataform']))
        if len(tokenList) >0:
            serializer = Token_DeviceSerializer(tokenList[0])
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            serializer = Token_DeviceSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TokenDeviceGetPut(APIView):
    def get_object(self, id):
        try:
            return TokenDevice.objects.get(id_token_device=id)
        except TokenDevice.DoesNotExist:
            raise Http404
    def get(self, request, id, format=None):
        tokenDeviceObj = self.get_object(id)
        serializer = Token_DeviceSerializer(tokenDeviceObj)
        return Response(serializer.data)
    def put(self, request, id, format=None):
        #begin
        listaTokensUser = TokenDevice.objects.filter(id_user=request.data['id_user'])
        if(len(listaTokensUser) > 0):
            serializer = Token_DeviceSerializer(listaTokensUser[0], data=request.data)
            tokenDelete = TokenDevice.objects.filter(Q(token_device=request.data['token_device'])& Q(id_user=None))
            if(len(tokenDelete) > 0):
                tokenDelete[0].delete()
        else:
            tokenDeviceObj = self.get_object(id)
            serializer = Token_DeviceSerializer(tokenDeviceObj, data=request.data)
        #end
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FavoritosSet(APIView):
    permission_classes =  (IsAuthenticated,)

    def post(self, request, format=None):
        serializer = FavoritosSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Favoritos_Get(APIView):
    permission_classes =  (IsAuthenticated,)

    def get(self, request, id, format=None):
        user_favoritosObj = Favoritos.objects.filter(Q(id_usuario=id))
        serializer = FavoritosFullSerializer(user_favoritosObj, many=True)
        return Response(serializer.data)

class Favoritos_List(APIView):
    permission_classes =  (IsAuthenticated,)

    def get(self, request, id, format=None):
        user_favoritosObj = Favoritos.objects.filter(Q(id_usuario=id))
        serializer = FavoritosSerializer(user_favoritosObj, many=True)
        return Response(serializer.data)

class FavoritosDelete(APIView):
    permission_classes =  (IsAuthenticated,)

    def delete(self, request, id_usuario, id_difunto, format=None):
        favoritoObj = Favoritos.objects.filter(Q(id_usuario=id_usuario) & (Q(id_difunto=id_difunto)))
        favoritoObj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# begin Paquetes
class PaquetesPost(APIView):
    # permission_classes = (IsAuthenticated,)
    def post(self, request, format=None):
        serializer = PaquetesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PaquetesList(APIView):
    def get(self, request, id, format=None):
        paquetesList = Paquetes.objects.filter(Q(id_camposanto=id))
        serializer = PaquetesSerializer(paquetesList, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class PaqueteUpdateDelete(APIView):
    def get_object(self, id_paquete):
        try:
            return Paquetes.objects.get(id_paquete=id_paquete)
        except Paquetes.DoesNotExist:
            raise Http404
    def put(self, request, id_paquete, format=None):
        paquetObj = self.get_object(id_paquete)
        if('imagen' in request.data):
            seri = PaquetesSerializer(paquetObj)
            path = seri['imagen'].value[7:]
            default_storage.delete(path)
        serializer = PaquetesSerializer(paquetObj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, id_paquete, format=None):
        paquetObj = self.get_object(id_paquete)
        seri = PaquetesSerializer(paquetObj)
        path = seri['imagen'].value[7:]
        paquetObj.delete()
        default_storage.delete(path)
        return Response(status=status.HTTP_204_NO_CONTENT)

class paquetesRecientes(APIView):
    def get(self, request, id, format=None):
        paquetesList = Paquetes.objects.filter(Q(id_camposanto=id)).order_by('-id_paquete')[:6]
        serializer = PaquetesSerializer(paquetesList, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
# end Paquetes

# begin Notificacion
class NotidicacionPost(APIView):
    # permission_classes = (IsAuthenticated,)
    def post(self, request, format=None):
        serializer = NotificacionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class NotificacionList(APIView):
    def get(self, request, id, format=None):
        notificacionList = Notificaciones.objects.filter(Q(id_camposanto=id))
        serializer = NotificacionSerializer(notificacionList, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class NotificacionUpdateDelete(APIView):
    def get_object(self, id_notificacion):
        try:
            return Notificaciones.objects.get(id_notificacion=id_notificacion)
        except Notificaciones.DoesNotExist:
            raise Http404
    def put(self, request, id_notificacion, format=None):
        notificacionObj = self.get_object(id_notificacion)
        serializer = NotificacionSerializer(notificacionObj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, id_notificacion, format=None):
        notificacionObj = self.get_object(id_notificacion)
        notificacionObj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# end notificacion

class SendPushNotificationDevice(APIView):
    def get_object(self, id_notificacion):
        try:
            return Notificaciones.objects.get(id_notificacion=id_notificacion)
        except Notificaciones.DoesNotExist:
            raise Http404
    def get(self, request, id_notificacion, format=None):
        notificacionObj = self.get_object(id_notificacion)
        if notificacionObj:
            serializer = NotificacionSerializer(notificacionObj)
            retorno = sendNotificaction(
                serializer['id_camposanto'].value,
                serializer['titulo'].value,
                serializer['mensaje'].value,
                serializer['tipo'].value
            )
            if(retorno == 1):
                notificacionObj.estado = "enviada"
                notificacionObj.save()
                return Response(data={'status': "success"}, status=status.HTTP_200_OK)
            else:
                return Response(data={'status': "error"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        return Response(data={'status': "error"}, status=status.HTTP_404_NOT_FOUND)



# Obtener homenajes GRATUITOS por id de difunto
class HomenajeFree_Get(APIView):
    def get(self, request, id, format=None):
        user_homenajesObj = Homenajes.objects.filter(id_difunto=id, gratuito=True)
        serializer = HomenajeSerializer(user_homenajesObj, many=True)
        return Response(serializer.data)

# Obtener homenajes PAGADOS por id de difunto
class HomenajePaid_Get(APIView):
    def get(self, request, id, format=None):
        user_homenajesObj = Homenajes.objects.filter(id_difunto=id, gratuito=False)
        serializer = HomenajeSerializer(user_homenajesObj, many=True)
        return Response(serializer.data)

class ContactoPost(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        contactoObj = Contacto.objects.all()
        serializer = ContactoSerializer(contactoObj, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        if ('img_base64' in request.data):
            format, imgstr = request.data['img_base64'].split(';base64,')
            ext = format.split('/')[-1]
            nameFile = request.data['nombre_file']
            imag = ContentFile(base64.b64decode(imgstr), name=nameFile)
            request.data._mutable = True
            del request.data['img_base64']
            del request.data['nombre_file']
            request.data['imagen'] = imag
            request.data._mutable = False
        serializer = ContactoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ContactoCamposanto(APIView):

    def get_object(self, id_camposanto):
        try:
            return Contacto.objects.filter(id_camposanto=id_camposanto)
        except Responsable_difunto.DoesNotExist:
            raise Http404

    def get(self, request, id_camposanto, format=None):
        contactoObj = self.get_object(id_camposanto)
        serializer = Contacto_userSerializer(contactoObj, many=True)
        return Response(serializer.data)

class ContactoView(APIView):

    def get_object(self, id_contacto):
        try:
            return Contacto.objects.get(id_contacto=id_contacto)
        except Contacto.DoesNotExist:
            raise Http404

    def delete(self, request, id_contacto, format=None):
        contactoObj = self.get_object(id_contacto)
        seri = ContactoSerializer(contactoObj)
        if(seri['imagen'].value != None):
            path = seri['imagen'].value[7:]
            default_storage.delete(path)
        contactoObj.delete()
        return Response(status=status.HTTP_200_OK)

class Homenaje_Del(APIView):

    def get_object(self, id_homenaje):
        try:
            return Homenajes.objects.get(id_homenaje=id_homenaje)
        except Homenajes.DoesNotExist:
            raise Http404

    def put(self, request, id_homenaje, format = None):
        homenajeObj = self.get_object(id_homenaje)
        serializer = HomenajeSerializer(homenajeObj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class Hyoutube_Delete(APIView):
    def get_object(self, id_youtube):
        try:
            return H_youtube.objects.get(id_youtube=id_youtube)
        except H_youtube.DoesNotExist:
            raise Http404
    def delete(self, request, id_youtube, format=None):
        youtubeObj = self.get_object(id_youtube)
        youtubeObj.delete()
        return Response(status=status.HTTP_200_OK)

