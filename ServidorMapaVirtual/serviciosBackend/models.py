from django.db import models
from django.contrib.auth.models import AbstractBaseUser, AbstractUser, BaseUserManager
from django.utils.translation import ugettext_lazy as _

class Empresa(models.Model):
    id_empresa = models.AutoField(primary_key=True, unique=True)
    nombre = models.CharField (max_length=50, unique=True)
    correo = models.CharField (max_length=70, unique=True)
    ruc = models.CharField (max_length=13, unique=True)
    web = models.CharField (max_length = 100, unique = True)
    estado = models.BooleanField(default=True)
    direccion_matriz = models.CharField (max_length=100, unique=True)

class Camposanto(models.Model):
    id_camposanto = models.AutoField(primary_key=True, unique=True)
    nombre = models.CharField (max_length=100, unique=True)
    direccion = models.CharField (max_length=100)
    telefono = models.CharField(max_length=15)
    estado = models.BooleanField(default=True)
    logo = models.ImageField(upload_to='logos', max_length=200, null=True, blank=True)
    id_empresa = models.ForeignKey(Empresa, on_delete=models.PROTECT, null=True, blank=True)

class Red_social(models.Model):
    id_red_social = models.AutoField(primary_key=True, unique=True)
    nombre = models.CharField (max_length=15)
    link = models.CharField (max_length=100)
    estado = models.BooleanField(default=True)
    id_camposanto = models.ForeignKey(Camposanto, on_delete=models.PROTECT, null=True, blank=True)

class Punto_geolocalizacion(models.Model):
    id_punto = models.AutoField(primary_key=True, unique=True)
    latitud = models.FloatField()
    longitud = models.FloatField()
    estado = models.BooleanField(default=True)
    id_camposanto = models.ForeignKey(Camposanto, on_delete=models.CASCADE)

class Sector(models.Model):
    id_sector = models.AutoField(primary_key=True, unique=True)
    nombre = models.CharField (max_length=50)
    estado = models.BooleanField(default=True)
    id_camposanto = models.ForeignKey(Camposanto, on_delete=models.PROTECT)

class Tipo_sepultura(models.Model):
    id_tip_sepultura = models.AutoField(primary_key=True, unique=True)
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=100)
    estado = models.BooleanField(default=True)
    id_camposanto = models.ForeignKey(Camposanto, on_delete=models.PROTECT)

class Difunto(models.Model):
    id_difunto = models.AutoField(primary_key=True, unique=True)
    nombre = models.CharField(max_length=30)
    apellido = models.CharField(max_length=30)
    genero = models.CharField(max_length=10)
    cedula = models.CharField(max_length =10)
    lugar_nacimiento = models.CharField(max_length=60)
    fecha_nacimiento = models.DateField()
    lugar_difuncion = models.CharField(max_length=60)
    fecha_difuncion = models.DateField()
    no_lapida = models.CharField(max_length=20)
    latitud = models.FloatField()
    longitud = models.FloatField()
    num_rosas = models.IntegerField(default=0)
    estado = models.BooleanField(default=True)
    id_camposanto = models.ForeignKey(Camposanto, on_delete=models.PROTECT)
    id_tip_sepultura = models.ForeignKey(Tipo_sepultura, on_delete=models.PROTECT)
    id_sector = models.ForeignKey(Sector, on_delete=models.PROTECT)

class Responsable_difunto(models.Model):
    id_responsable = models.AutoField(primary_key=True, unique=True)
    nombre = models.CharField(max_length=30)
    apellido = models.CharField(max_length=30)
    telefono = models.CharField(max_length=10, default=None, null=True, blank=True)
    celular = models.CharField(max_length=10, default=None, null=True, blank=True)
    direccion = models.CharField(max_length=100, default=None, null=True, blank=True)
    correo = models.EmailField(max_length=100, default=None, null=True, blank=True)
    parentezco = models.CharField(max_length=25)
    id_difunto = models.ForeignKey(Difunto, models.SET_NULL, null=True, blank=True)

class UsuarioManager(BaseUserManager):
    def create_user(self,email=None,first_name=None,last_name=None,password=None,tipo_usuario=None,username=None):

        usuario = self.model(
             username = username,
             email=self.normalize_email(email),
             first_name = first_name,
             last_name = last_name,
             password = password,
             tipo_usuario = "uf"
        )
        usuario.set_password(password)
        usuario.save()
        return usuario

    def create_superuser(self,email=None, username=None, first_name =None, last_name =None, password=None, tipo_usuario = "ha"):
        usuario = self.create_user(
            email=self.normalize_email(email),
            username = username,
            first_name=first_name,
            last_name=last_name,
            password=password,
            tipo_usuario=tipo_usuario
        )
        usuario.staff = True
        usuario.save()
        return usuario

class User(AbstractBaseUser):
    super_admin = 'su'
    admin = 'ad'
    usuario_final = 'uf'
    hiper_admin = 'ha'
    tipo_usuario_choice= [
        (super_admin, 'super_admin'),
        (admin, 'admin'),
        (usuario_final, 'usuario_final'),
        (hiper_admin, 'hiper_admin')
    ]
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    # se pordria agregar que el email no sea requerido
    email = models.EmailField(_('email address'), max_length=200, default=None, null=True, blank=True)
    # se debe cambiar que el username es requerido
    username = models.CharField(max_length=50, unique=True, default=None, null=True, blank=True)
    password = models.CharField(max_length=100, default=None, null=True, blank=True)
    telefono = models.CharField(max_length=10, default=None, null=True, blank=True)
    image_perfil = models.ImageField(upload_to='perfil', max_length=500, default=None, null=True, blank=True)
    is_facebook = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    genero = models.CharField(max_length=15, default=None, null=True, blank=True)
    direccion = models.CharField(max_length=100, default=None, null=True, blank=True)
    id_camposanto = models.ForeignKey(Camposanto, models.SET_NULL, null=True, blank=True)
    staff = models.BooleanField(default=False)
    tipo_usuario = models.CharField(max_length=40, choices= tipo_usuario_choice, default=admin)

    objects = UsuarioManager()

    USERNAME_FIELD = 'username'

    def __str__(self):
        return "{}".format(self.username)

    def has_perm(self, perm, obj = None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.staff

class Permiso(models.Model):
    id_permiso = models.AutoField(primary_key=True, unique=True)
    nombre = models.CharField(unique=True, max_length=50)
    descripcion = models.CharField(max_length=150)

    def __str__(self):
        return self.nombre + str(self.id_permiso)


class User_permisos(models.Model):
    id_user_permiso = models.AutoField(primary_key=True, unique=True)
    id_user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_permiso = models.ForeignKey(Permiso, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id_permiso) + str(self.id_user)

class H_mensaje(models.Model):
    id_mensaje = models.AutoField(primary_key = True, unique = True)
    mensaje = models.CharField(max_length=1500)
    #id_homenaje = models.ForeignKey(Homenajes, on_delete= models.CASCADE)

class H_imagen(models.Model):
    id_imagen = models.AutoField(primary_key = True, unique = True)
    mensaje = models.CharField(max_length=200)
    #id_homenaje = models.ForeignKey(Homenajes, on_delete= models.CASCADE)
    imagen = models.ImageField(upload_to='h_imagen', max_length=200, null=True, blank=True)

class H_video(models.Model):
    id_video = models.AutoField(primary_key = True, unique = True)
    mensaje = models.CharField(max_length=200)
    #id_homenaje = models.ForeignKey(Homenajes, on_delete= models.CASCADE)
    video = models.FileField(upload_to='h_video', max_length=200, null=True, blank=True)

class H_audio(models.Model):
    id_audio = models.AutoField(primary_key = True, unique = True)
    mensaje = models.CharField(max_length=200)
    audio = models.FileField(upload_to='h_audio', max_length=200, null=True, blank=True)

class H_youtube(models.Model):
    id_youtube = models.AutoField(primary_key = True, unique = True)
    mensaje = models.CharField(max_length=200)
    video = models.CharField(max_length=300)

class Homenajes(models.Model):
    id_homenaje = models.AutoField(primary_key = True, unique = True)
    id_usuario = models.ForeignKey(User,on_delete=models.CASCADE )
    id_difunto = models.ForeignKey(Difunto, on_delete= models.CASCADE)
    fecha_publicacion = models.DateTimeField()
    estado = models.BooleanField(default=True)
    gratuito = models.BooleanField(default=True)
    id_textcontent = models.ForeignKey(H_mensaje, on_delete= models.CASCADE, blank=True, null=True)
    id_imagecontent = models.ForeignKey(H_imagen, on_delete= models.CASCADE, blank=True,null=True)
    id_videocontent = models.ForeignKey(H_video, on_delete= models.CASCADE, blank=True, null=True)
    id_audiocontent = models.ForeignKey(H_audio, on_delete= models.CASCADE, blank=True, null=True)
    id_youtube = models.ForeignKey(H_youtube, on_delete= models.CASCADE, blank=True, null=True)

class Historial_rosas(models.Model):
    id_rosa = models.AutoField(primary_key = True, unique = True)
    rosa = models.BooleanField(default= True)
    id_usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    id_difunto = models.ForeignKey(Difunto, on_delete=models.CASCADE)
    fecha_publicacion = models.DateTimeField()

class TokenDevice(models.Model):
    id_token_device = models.AutoField(primary_key = True, unique = True)
    token_device = models.CharField(max_length=1500)
    plataform = models.CharField(max_length=25, default=None, null=True, blank=True)
    id_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    id_camposanto = models.ForeignKey(Camposanto, on_delete=models.CASCADE, null=True, blank=True )

class Favoritos(models.Model):
    id_favorito = models.AutoField(primary_key = True, unique = True)
    id_usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    id_difunto = models.ForeignKey(Difunto, on_delete=models.CASCADE)

class Paquetes(models.Model):
    id_paquete = models.AutoField(primary_key = True, unique = True)
    nombre = models.CharField(max_length=70)
    descripcion = models.CharField(max_length=500)
    precio = models.FloatField()
    imagen = models.ImageField(upload_to='paquetes', max_length=200, null=True, blank=True)
    fecha_created = models.DateField()
    id_camposanto = models.ForeignKey(Camposanto, on_delete=models.CASCADE)

class Notificaciones(models.Model):
    enviada = 'enviada'
    no_enviada = 'no_enviada'
    estado_choice = [
        (enviada, 'enviada'),
        (no_enviada, 'no_enviada')
    ]
    paquete = 'paquete'
    tip = 'tip'
    tipo_choice = [
        (paquete, 'paquete'),
        (tip, 'tip')
    ]
    id_notificacion = models.AutoField(primary_key = True, unique = True)
    titulo = models.CharField(max_length=70)
    mensaje = models.CharField(max_length=500)
    fecha_created = models.DateField()
    estado = models.CharField(max_length=40, choices=estado_choice, default=no_enviada)
    tipo = models.CharField(max_length=40, choices=tipo_choice, default=tip)
    id_camposanto = models.ForeignKey(Camposanto, on_delete=models.CASCADE)

class Contacto(models.Model):
    id_contacto = models.AutoField(primary_key = True, unique = True)
    imagen = models.ImageField(upload_to = 'sugerencias', max_length = 500, null = True, blank = True)
    mensaje = models.CharField(max_length=500)
    fecha_emision = models.DateField()
    id_camposanto = models.ForeignKey(Camposanto, on_delete=models.CASCADE)
    id_usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id_contacto) + str(self.id_usuario) + str(self.fecha_emision)

    class Meta:
        verbose_name = "Sugerencia"
        verbose_name_plural = "Sugerencias"

