from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from django.contrib.auth import views as auth_views

from . import views


urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),


    path('', views.home, name='home'),
    path('subir_documento/', views.subir_documento, name='subir_documento'),
    path('lista_documentos/', views.lista_documentos, name='lista_documentos'),
    path('editar:documento/<int:documento_id>/', views.editar_documento, name='editar_documento'),
    #path('documento/<int:documento_id>/', views.ver_documento, name='ver_documento'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)