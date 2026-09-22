from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import (
    Calificacion, Comision, ConfiguracionComision, FotoSolicitud,
    Notificacion, Pago, PerfilTecnico, Solicitud, Usuario,
)


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    # UserAdmin trae fieldsets pensados para 'username'; como aquí no existe,
    # se sobreescriben para que el admin no reviente al abrir un usuario.
    ordering = ["-date_joined"]
    list_display = ["correo", "nombre_completo", "rol", "estado", "is_staff"]
    list_filter = ["rol", "estado"]
    search_fields = ["correo", "cedula", "nombre_completo"]
    fieldsets = (
        (None, {"fields": ("correo", "password")}),
        ("Datos personales", {"fields": ("nombre_completo", "cedula", "telefono",
                                          "direccion", "fecha_nacimiento", "latitud", "longitud")}),
        ("Estado", {"fields": ("rol", "estado", "motivo_rechazo",
                                "motivo_suspension", "fecha_suspension")}),
        ("Permisos", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {"classes": ("wide",), "fields": (
            "correo", "password1", "password2", "cedula", "nombre_completo", "telefono", "rol",
        )}),
    )


@admin.register(PerfilTecnico)
class PerfilTecnicoAdmin(admin.ModelAdmin):
    list_display = ["usuario", "especialidad", "ciudad", "disponible", "calificacion_promedio"]
    list_filter = ["especialidad", "disponible"]


class FotoSolicitudInline(admin.TabularInline):
    model = FotoSolicitud
    extra = 0


@admin.register(Solicitud)
class SolicitudAdmin(admin.ModelAdmin):
    list_display = ["id", "categoria", "estado", "cliente", "tecnico", "urgencia", "fecha_creacion"]
    list_filter = ["estado", "categoria", "urgencia"]
    inlines = [FotoSolicitudInline]


admin.site.register(Calificacion)
admin.site.register(Notificacion)
admin.site.register(Pago)
admin.site.register(Comision)
admin.site.register(ConfiguracionComision)
