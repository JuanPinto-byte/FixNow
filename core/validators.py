"""Validadores compartidos por los modelos de core."""
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

# FN-1 / FN-8: cédula solo números, de 6 a 10 dígitos.
validar_cedula = RegexValidator(
    regex=r"^\d{6,10}$",
    message="La cédula debe tener solo números, entre 6 y 10 dígitos.",
)

EXTENSIONES_CERTIFICACION = ("pdf", "jpg", "jpeg", "png")
EXTENSIONES_FOTO = ("jpg", "jpeg", "png")
TAMANO_MAX_MB = 5


def _validar_archivo(archivo, extensiones):
    ext = archivo.name.rsplit(".", 1)[-1].lower()
    if ext not in extensiones:
        raise ValidationError(f"Formato no permitido. Debe ser: {', '.join(extensiones)}.")
    if archivo.size > TAMANO_MAX_MB * 1024 * 1024:
        raise ValidationError(f"El archivo no puede pesar más de {TAMANO_MAX_MB} MB.")


def validar_certificacion(archivo):
    """FN-8: documento de certificación, PDF o imagen, máx. 5MB."""
    _validar_archivo(archivo, EXTENSIONES_CERTIFICACION)


def validar_foto(archivo):
    """FN-3 / FN-12: fotos jpg/png, máx. 5MB."""
    _validar_archivo(archivo, EXTENSIONES_FOTO)
