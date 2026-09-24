import re

from django import forms
from django.core.exceptions import ValidationError
from django.db import transaction

from .models import Categoria, PerfilTecnico, Usuario
from .validators import validar_certificacion

ATRS_TEXTO = "form-control"
ATRS_CHECK = "form-check-input"


def _campo_password(id_campo):
    """Comparte el widget entre FN-1 y FN-8 sin repetir el bloque completo."""
    return forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={
            "class": ATRS_TEXTO, "id": id_campo, "autocomplete": "new-password",
        }),
    )


def _campo_password2(id_campo):
    return forms.CharField(
        label="Confirmar contraseña",
        widget=forms.PasswordInput(attrs={
            "class": ATRS_TEXTO, "id": id_campo, "autocomplete": "new-password",
        }),
    )


def _campo_terminos(id_campo):
    return forms.BooleanField(
        label="Acepto los términos y condiciones",
        error_messages={"required": "Debes aceptar los términos para continuar."},
        widget=forms.CheckboxInput(attrs={"class": ATRS_CHECK, "id": id_campo}),
    )


def _validar_politica_password(password):
    """FN-1/FN-8: mínimo 8 caracteres, una mayúscula, un número y un símbolo."""
    errores = []
    if len(password) < 8:
        errores.append("Debe tener al menos 8 caracteres.")
    if not re.search(r"[A-Z]", password):
        errores.append("Debe incluir al menos una mayúscula.")
    if not re.search(r"\d", password):
        errores.append("Debe incluir al menos un número.")
    if not re.search(r"[^A-Za-z0-9]", password):
        errores.append("Debe incluir al menos un símbolo (por ejemplo ! # $ %).")
    if errores:
        raise ValidationError(errores)


class RegistroClienteForm(forms.ModelForm):
    """
    FN-1: registro de cliente. Los campos de Meta.fields ya traen su
    validación desde el modelo (cedula con regex de 6-10 dígitos, correo
    único, etc.) porque ModelForm llama a full_clean() del modelo solo.
    Contraseña y términos no son campos del modelo, así que se agregan
    aparte y se validan aquí.
    """

    password = _campo_password("password")
    password2 = _campo_password2("password2")
    terminos = _campo_terminos("terminos")

    class Meta:
        model = Usuario
        fields = ["cedula", "nombre_completo", "correo", "telefono"]
        widgets = {
            "cedula": forms.TextInput(attrs={
                "class": ATRS_TEXTO, "id": "cedula", "inputmode": "numeric",
                "maxlength": "10", "autocomplete": "off",
            }),
            "nombre_completo": forms.TextInput(attrs={
                "class": ATRS_TEXTO, "id": "nombre_completo", "autocomplete": "name",
            }),
            "correo": forms.EmailInput(attrs={
                "class": ATRS_TEXTO, "id": "correo", "autocomplete": "email",
            }),
            "telefono": forms.TextInput(attrs={
                "class": ATRS_TEXTO, "id": "telefono", "autocomplete": "tel",
            }),
        }
        error_messages = {
            "cedula": {"unique": "Ya existe una cuenta registrada con esta cédula."},
            "correo": {"unique": "Ya existe una cuenta registrada con este correo."},
        }

    def clean_password(self):
        password = self.cleaned_data["password"]
        _validar_politica_password(password)
        return password

    def clean(self):
        cleaned = super().clean()
        p1, p2 = cleaned.get("password"), cleaned.get("password2")
        if p1 and p2 and p1 != p2:
            self.add_error("password2", "Las contraseñas no coinciden.")
        return cleaned

    def save(self, commit=True):
        usuario = super().save(commit=False)
        usuario.rol = Usuario.Rol.CLIENTE
        usuario.estado = Usuario.Estado.ACTIVO
        usuario.set_password(self.cleaned_data["password"])
        if commit:
            usuario.save()
        return usuario


class RegistroTecnicoForm(forms.ModelForm):
    """
    FN-8: a diferencia de FN-1, junta datos de dos modelos (Usuario y
    PerfilTecnico) en un solo formulario, y el usuario queda con estado
    'pendiente_aprobacion' en vez de quedar activo de una vez (ver FN-14).
    """

    especialidad = forms.ChoiceField(
        label="Especialidad",
        choices=[("", "Elige una")] + list(Categoria.choices),
        widget=forms.Select(attrs={"class": "form-select", "id": "especialidad"}),
    )
    ciudad = forms.CharField(
        label="Ciudad",
        widget=forms.TextInput(attrs={"class": ATRS_TEXTO, "id": "ciudad"}),
    )
    documento_certificacion = forms.FileField(
        label="Documento de certificación",
        validators=[validar_certificacion],
        error_messages={"required": "Adjunta tu certificación para poder registrarte."},
        widget=forms.ClearableFileInput(attrs={
            "class": ATRS_TEXTO, "id": "certificacion", "accept": "application/pdf,image/*",
        }),
    )
    password = _campo_password("password")
    password2 = _campo_password2("password2")
    terminos = _campo_terminos("terminos")

    class Meta:
        model = Usuario
        fields = ["cedula", "nombre_completo", "correo", "telefono"]
        widgets = {
            "cedula": forms.TextInput(attrs={
                "class": ATRS_TEXTO, "id": "cedula", "inputmode": "numeric",
                "maxlength": "10", "autocomplete": "off",
            }),
            "nombre_completo": forms.TextInput(attrs={
                "class": ATRS_TEXTO, "id": "nombre_completo", "autocomplete": "name",
            }),
            "correo": forms.EmailInput(attrs={
                "class": ATRS_TEXTO, "id": "correo", "autocomplete": "email",
            }),
            "telefono": forms.TextInput(attrs={
                "class": ATRS_TEXTO, "id": "telefono", "autocomplete": "tel",
            }),
        }
        error_messages = {
            "cedula": {"unique": "Ya existe una cuenta registrada con esta cédula."},
            "correo": {"unique": "Ya existe una cuenta registrada con este correo."},
        }

    def clean_password(self):
        password = self.cleaned_data["password"]
        _validar_politica_password(password)
        return password

    def clean(self):
        cleaned = super().clean()
        p1, p2 = cleaned.get("password"), cleaned.get("password2")
        if p1 and p2 and p1 != p2:
            self.add_error("password2", "Las contraseñas no coinciden.")
        return cleaned

    def save(self, commit=True):
        usuario = super().save(commit=False)
        usuario.rol = Usuario.Rol.TECNICO
        usuario.estado = Usuario.Estado.PENDIENTE_APROBACION
        usuario.set_password(self.cleaned_data["password"])
        if commit:
            # Si falla la creación del perfil, no debe quedar un Usuario
            # huérfano sin PerfilTecnico asociado.
            with transaction.atomic():
                usuario.save()
                PerfilTecnico.objects.create(
                    usuario=usuario,
                    especialidad=self.cleaned_data["especialidad"],
                    ciudad=self.cleaned_data["ciudad"],
                    documento_certificacion=self.cleaned_data["documento_certificacion"],
                )
        return usuario
