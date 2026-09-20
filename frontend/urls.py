from django.urls import path

from . import views

urlpatterns = [
    # Público
    path("", views.landing, name="landing"),
    path("ingresar/", views.login_view, name="login"),
    path("registro/", views.registro_cliente, name="registro_cliente"),
    path("registro/tecnico/", views.registro_tecnico, name="registro_tecnico"),
    # Cliente
    path("cliente/", views.cliente_inicio, name="cliente_inicio"),
    path("cliente/solicitud/nueva/", views.solicitud_nueva, name="solicitud_nueva"),
    path("cliente/tecnicos/", views.tecnicos, name="tecnicos"),
    path("cliente/historial/", views.cliente_historial, name="cliente_historial"),
    # Técnico
    path("tecnico/solicitudes/", views.tecnico_solicitudes, name="tecnico_solicitudes"),
    # Administrador
    path("panel/tecnicos/", views.admin_tecnicos, name="admin_tecnicos"),
]
