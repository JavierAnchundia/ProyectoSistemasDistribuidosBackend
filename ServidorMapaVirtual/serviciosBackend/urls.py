from django.urls import path
from django.conf.urls import include
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import DefaultRouter
from serviciosBackend import views

urlpatterns = [
    path('camposantos/', views.CamposantoView.as_view()),
    path('camposanto/<str:pk>/', views.CamposantoViewSet.as_view()),
    path('red_social_post/', views.Red_socialPost.as_view()),
    path('redes_sociales_camp/<str:id_camp>/', views.Red_socialListGet.as_view()),
    path('red_social_put/<str:id_red>/', views.Red_socialPut.as_view()),
    path('geolocalizacion_post/', views.GeolocalizacionPost.as_view()),
    path('geolocalizacion_camp/<str:id_camp>/', views.GeolocalizacionListGet.as_view()),
    path('geolocalizacion_del/<str:id_punto>/', views.GeolocalizacionDelete.as_view()),
    path('sector_camp/<str:id_camp>/', views.SectorListGet.as_view()),
    path('tipo_sepultura_camp/<str:id_camp>/', views.Tipo_sepulturaListGet.as_view()),
    path('difunto_post/', views.DifuntoView.as_view()),
    path('difunto/<str:pk>/', views.DifuntoViewSet.as_view()),
    path('difuntos/<str:id_camp>/', views.DifuntoListGet.as_view()),
    path('difuntos/<str:id_camp>/<str:nombre>/<str:apellido>/<str:desde>/<str:hasta>/<str:lapida>/<str:sector>/<str:sepultura>/', views.DifuntoListFilteredGet.as_view()),
    path('responsable_difunto_post/', views.Responsable_difuntoView.as_view()),
    path('responsable_difunto_get/<str:id_difunto>/', views.Responsable_difuntoViewSet.as_view()),
    path('empresas/', views.EmpresasView.as_view()),
    path('empresa_get/<str:pk>/', views.EmpresaViewSet.as_view()),
    path('usuario/<str:username>/', views.UsuarioViewGet.as_view()),
    path('obtener_usuarios/', views.UsuarioGetAll.as_view()),
    path('usuarios_camp/<str:id_camp>/', views.UsuarioGetCamposanto.as_view()),
    path('listar_permisos_general/', views. PermisoView.as_view()),
    path('mis_user_permisos/<str:id>/', views.User_PermisosGet.as_view()),
    path('user_permisos_post/', views.User_PermisosPost.as_view()),
    path('homenajes/<str:id>/', views.Homenaje_Get.as_view()),
    path('homenajes_post/', views.Homenaje_Set.as_view()),
    path('hmensaje/<str:id>/', views.Htexto_Get.as_view()),
    path('himagen/<str:id>/', views.Himagen_Get.as_view()),
    path('hmensaje_post/', views.Htexto_Set.as_view()),
    path('himagen_post/', views.Himagen_Set.as_view()),
    path('hvideo_post/', views.Hvideo_Set.as_view()),
    path('haudio_post/', views.Haudio_Set.as_view()),
    path('hyoutube_post/', views.Hyoutube_Set.as_view()),
    path('difunto/update-partial/<str:pk>/<str:num_rosas>/',views.AmountPartialUpdateView.as_view()),
    path('historial_rosas/<str:id>/', views.Historial_rosasGet.as_view()),
    path('historial_rosas_post/', views.Historial_rosasSet.as_view()),
    path('hmensaje_del/<str:id_mensaje>/', views.HTexto_Delete.as_view()),
    path('himagen_del/<str:id_imagen>/', views.HImagen_Delete.as_view()),
    path('haudio_del/<str:id_audio>/', views.HAudio_Delete.as_view()),
    path('hvideo_del/<str:id_video>/', views.HVideo_Delete.as_view()),
    path('permiso/<str:pk>/', views.Permiso_Info.as_view()),

    # actualizar contasena del usuario  10/11/2020
    path('actualizar_contrasena/<str:id>/', views.ActualizarContrasena.as_view()),
    # api utilizada para escribir el correo en la aplicacion en web final o movil  10/11/2020
    path('enviar_email_password/<str:email>/<str:id_camp>/', views.EnviarCorreoContrasena.as_view()),
    # api utilizada para escribir el correo en la aplicacion en admin
    path('enviar_email_password_admin/<str:username>/', views.EnviarCorreoContrasenaAdmin.as_view()),

    # actualizar imagen movil
    path('update_image_profile/<str:id>/', views.ImageUserUpdate.as_view()),
    # obtener el token para usuario de facebook
    path('get_token_facebook/', views.Create_User_Facebook.as_view()),
    #get user by id
    path('get_user_by_id/<str:id>/', views.UsuarioGetById.as_view()),


    # Post para token device
    path('post_token_device/', views.TokenDevicePost.as_view()),
    # Get and put token device
    path('api_token_device/<str:id>/', views.TokenDeviceGetPut.as_view()),

    #Favoritos por agregar a PA
    path('favoritos/', views.FavoritosSet.as_view()),
    path('favoritos/<str:id>/', views.Favoritos_Get.as_view()),
    path('favoritos_list/<str:id>/', views.Favoritos_List.as_view()),
    path('favoritos_del/<str:id_usuario>/<str:id_difunto>/', views.FavoritosDelete.as_view()),


    path('info_permiso_user/<str:pk>/', views.Info_Permiso_User.as_view()),
    path('paquete_add/', views.PaquetesPost.as_view()),
    path('paquete_put_del/<str:id_paquete>/', views.PaqueteUpdateDelete.as_view()),
    path('paquetes_list/<str:id>/', views.PaquetesList.as_view()),
    path('paquetes_rec/<str:id>/', views.paquetesRecientes.as_view()),

    #Notificaciones agregar a PA
    path('notificacion_add/', views.NotidicacionPost.as_view()),
    path('notificacion_put_del/<str:id_notificacion>/', views.NotificacionUpdateDelete.as_view()),
    path('notificacion_list/<str:id>/', views.NotificacionList.as_view()),

    #Enviar push notificacion
    path('enviarNotificacionPush/<str:id_notificacion>/', views.SendPushNotificationDevice.as_view()),

    path('homenajesFree/<str:id>/', views.HomenajeFree_Get.as_view()),
    path('homenajesPaid/<str:id>/', views.HomenajePaid_Get.as_view()),


    path('contactoPost/', views.ContactoPost.as_view()),
    path('contactoCamposanto/<str:id_camposanto>/', views.ContactoCamposanto.as_view()),
    path('contacto/<str:id_contacto>/', views.ContactoView.as_view()),

    path('homenajesDel/<str:id_homenaje>/', views.Homenaje_Del.as_view()),
    path('hyoutube_del/<str:id_youtube>/', views.Hyoutube_Delete.as_view()),

]

urlpatterns = format_suffix_patterns(urlpatterns)
