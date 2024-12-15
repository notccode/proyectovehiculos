from django.urls import path
from . import views


urlpatterns = [
    path('index', views.index, name='index'),
    path('vehiculo/add', views.add_vehiculo, name='add_vehiculo'),
    path('vehiculo/<int:vehiculo_id>/', views.ver_vehiculo, name='ver_vehiculo'),
    path('listar_vehiculos', views.listar_vehiculos, name='listar_vehiculos'),
    path('login_user/', views.login_user, name='login'),
    path('registrar_usuario/', views.registrar_usuario, name='registrar_usuario'),
    path('logout/', views.logout_view, name='logout'), 
]