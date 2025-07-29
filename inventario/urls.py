from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from inventario import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('lista_productos', views.lista_productos, name='lista_productos'),
    path('importar/', views.importar_excel, name='importar_excel'),
    path('exportar/', views.exportar_excel, name='exportar_excel'),
    path('editar/<int:pk>/', views.editar_producto, name='editar_producto'),
    path('eliminar/<int:pk>/', views.eliminar_producto, name='eliminar_producto'),
    #path('escaneo-ubicacion/', views.productos_por_ubicacion_codigo, name='productos_por_ubicacion_codigo'),
    #path('escaneo-ubicacion/', views.escaneo_ubicacion, name='escaneo_ubicacion'),
    path('registrar/', views.registrar_usuario, name='registrar_usuario'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    #path('escanear/', views.escanear_ubicacion, name='escanear_ubicacion'),
    path('escanear/', views.escaner_ubicacion, name='escanear'),
    path('buscar/', views.buscar_por_ubicacion, name='buscar_por_ubicacion'),


]
