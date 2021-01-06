from rest_framework import serializers
from .models import User, Empresa, Red_social, Camposanto, Punto_geolocalizacion, Sector, Tipo_sepultura, \
    Responsable_difunto, Difunto, Permiso, User_permisos, Homenajes, H_mensaje, H_imagen, H_video, H_audio, \
    Historial_rosas, TokenDevice, Favoritos, Paquetes, Notificaciones, H_youtube, Contacto
from django.conf import settings
from django.core.mail import send_mail

class EmpresaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empresa
        fields = '__all__'

class Red_socialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Red_social
        fields = '__all__'

class CamposantoSerializer(serializers.ModelSerializer):
    # id_empresa = EmpresaSerializer(read_only=True)
    class Meta:
        model = Camposanto
        fields = '__all__'

class Punto_geoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Punto_geolocalizacion
        fields = '__all__'

class SectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sector
        fields = '__all__'

class Tipo_sepulturaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tipo_sepultura
        fields = '__all__'

# class UsuarioSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Usuario
#         fields = '__all__'

class Responsable_difuntoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Responsable_difunto
        fields = '__all__'

class DifuntoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Difunto
        fields = '__all__'


class PermisoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permiso
        fields = '__all__'

class User_permisosSerializer(serializers.ModelSerializer):
    class Meta:
        model = User_permisos
        fields = '__all__'

class Info_permisosSerializer(serializers.ModelSerializer):
    permiso_name = serializers.CharField(source='id_permiso.nombre')

    class Meta:
        model = User_permisos
        fields = ('id_user_permiso', 'id_user', 'id_permiso', 'permiso_name')



#PENDIENTE DE AGREGAR A PYTHON ANYWHERE

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'last_name',
            'email',
            'username',
            'password',
            'telefono',
            'image_perfil',
            'is_facebook',
            'genero',
            'direccion',
            'id_camposanto',
            'staff',
            'tipo_usuario',
            'is_active',
        )
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        print('imagen' in validated_data)
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.username = validated_data.get('username')
        user.set_password(password)
        validar = user.save()
        if(validar == None):
            camposanto = self.obtener_camposanto(user)
            self.send_email(user, camposanto)
        return user

    def obtener_camposanto(self, usuario):
        retorno = ''
        camposanto = usuario.id_camposanto
        if(camposanto):
            nombreCamposanto = camposanto.nombre
            retorno = nombreCamposanto
        return retorno

    def send_email(self, usuario, camposanto):
        subject = '¡Bienvenido a Mapa Virtual!'
        if(camposanto and usuario.first_name and usuario.last_name):
            message = '¡Te damos la bienvenida a mapa virtual! \n'\
                      'Hola ' + usuario.first_name + ' ' + usuario.last_name+',\n'\
                      'Gracias por unirte a '+ camposanto +'.\n' \
                      '\nExplora nuestra página y conoce más novedades. '
        else:
            message = 'Bienvenido '+ usuario.email +', gracias por registrarse !!'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [usuario.email, ]
        send_mail(subject, message, email_from, recipient_list)
        
class H_mensajeSerializer(serializers.ModelSerializer):
    class Meta:
        model = H_mensaje
        fields = '__all__'

class H_imagenSerializer(serializers.ModelSerializer):
    class Meta:
        model = H_imagen
        fields = '__all__'

class H_videoSerializer(serializers.ModelSerializer):
    class Meta:
        model = H_video
        fields = '__all__'

class H_audioSerializer(serializers.ModelSerializer):
    class Meta:
        model = H_audio
        fields = '__all__'

class H_youtubeSerializer(serializers.ModelSerializer):
    class Meta:
        model = H_youtube
        fields = '__all__'

class HomenajeSerializer(serializers.ModelSerializer):
    id_usuario = UserProfileSerializer()
    id_difunto = DifuntoSerializer(required=False)
    id_textcontent = H_mensajeSerializer(required=False)
    id_imagecontent = H_imagenSerializer(required=False)
    id_videocontent = H_videoSerializer(required=False)
    id_audiocontent = H_audioSerializer(required=False)
    id_youtube = H_youtubeSerializer(required=False)
    class Meta:
        model = Homenajes
        fields = '__all__'

class HomenajeSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Homenajes
        fields = '__all__'

class Historial_rosasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Historial_rosas
        fields = '__all__'

class Log_RosasSerializer(serializers.ModelSerializer):
    id_usuario = UserProfileSerializer()
    class Meta:
        model = Historial_rosas
        fields = '__all__'

class Token_DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = TokenDevice
        fields = '__all__'

#CAMBIOS POR ANADIR A PA PARA LA PARTE DE FAVORITOS

class FavoritosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favoritos
        fields = '__all__'

class FavoritosFullSerializer(serializers.ModelSerializer):
    id_difunto = DifuntoSerializer(required=False)
    class Meta:
        model = Favoritos
        fields = '__all__'

class PaquetesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paquetes
        fields = '__all__'

class NotificacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notificaciones
        fields = '__all__'

class ContactoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contacto
        fields = '__all__'

class Contacto_userSerializer(serializers.ModelSerializer):

    user_username = serializers.CharField(source='id_usuario.username')
    class Meta:
        model = Contacto
        fields = ('id_contacto', 'imagen', 'mensaje', 'fecha_emision', 'id_camposanto', 'id_usuario', 'user_username')