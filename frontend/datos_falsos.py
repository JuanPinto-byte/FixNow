"""
Datos de mentira para armar las pantallas antes de tener el backend.
Cuando exista el modelo real, se reemplaza cada constante por una consulta
(por ejemplo Solicitud.objects.filter(cliente=request.user)) y el HTML casi no cambia.
"""
import math

CATEGORIAS = [
    {"id": "plomeria", "nombre": "Plomería", "icono": "bi-droplet-half"},
    {"id": "electricidad", "nombre": "Electricidad", "icono": "bi-lightning-charge-fill"},
    {"id": "cerrajeria", "nombre": "Cerrajería", "icono": "bi-key-fill"},
    {"id": "electrodomesticos", "nombre": "Electrodomésticos", "icono": "bi-tv-fill"},
    {"id": "otro", "nombre": "Otro", "icono": "bi-tools"},
]
_ICONO = {c["id"]: c["icono"] for c in CATEGORIAS}
_NOMBRE = {c["id"]: c["nombre"] for c in CATEGORIAS}

# Punto de referencia del cliente (cámbialo por el de tu ciudad).
CLIENTE = {
    "nombre": "Laura Gómez",
    "direccion": "Cra 13 #52-40",
    "lat": 4.6486,
    "lng": -74.0628,
}


def haversine_km(lat1, lng1, lat2, lng2):
    """Distancia en km entre dos coordenadas (así se calculará en FN-4)."""
    r = 6371.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dphi = p2 - p1
    dl = math.radians(lng2 - lng1)
    a = math.sin(dphi / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * r * math.asin(math.sqrt(a))


def precio_txt(valor):
    return "a convenir" if valor is None else "$" + f"{valor:,}".replace(",", ".")


_TECNICOS_RAW = [
    (1, "Camilo Restrepo", "plomeria", 4.9, 128, 60000, 4.6560, -74.0590),
    (2, "Andrea Molina", "electricidad", 4.7, 86, 55000, 4.6420, -74.0700),
    (3, "Jhon Fredy Pardo", "cerrajeria", None, 0, None, 4.6690, -74.0520),
    (4, "Sergio Cáceres", "electrodomesticos", 4.5, 41, 45000, 4.6210, -74.0850),
    (5, "Diana Salcedo", "plomeria", 4.8, 203, 70000, 4.7300, -74.0300),
    (6, "Luis Ángel Rojas", "electricidad", 4.2, 12, None, 4.5700, -74.1300),
]


def _iniciales(nombre):
    partes = nombre.split()
    return (partes[0][0] + partes[1][0]).upper() if len(partes) > 1 else nombre[:2].upper()


def tecnicos():
    salida = []
    for id_, nombre, cat, rating, resenas, precio, lat, lng in _TECNICOS_RAW:
        salida.append({
            "id": id_,
            "nombre": nombre,
            "iniciales": _iniciales(nombre),
            "categoria": cat,
            "especialidad": _NOMBRE[cat],
            "icono": _ICONO[cat],
            "rating": rating,
            "rating_txt": f"{rating:.1f}".replace(".", ",") if rating else "Sin calificaciones",
            "resenas": resenas,
            "precio": precio,
            "precio_txt": precio_txt(precio),
            "lat": lat,
            "lng": lng,
            "km": round(haversine_km(CLIENTE["lat"], CLIENTE["lng"], lat, lng), 1),
        })
    return sorted(salida, key=lambda t: t["km"])


SOLICITUD_EN_CURSO = {
    "id": 214,
    "categoria": "Plomería",
    "icono": "bi-droplet-half",
    "tecnico": "Camilo Restrepo",
    "descripcion": "Fuga de agua bajo el lavaplatos de la cocina.",
    "estado": "en_curso",
}

HISTORIAL_CLIENTE = [
    {"id": 214, "fecha": "18 sep 2026", "categoria": "Plomería", "icono": "bi-droplet-half",
     "tecnico": "Camilo Restrepo", "estado": "en_curso", "calificada": False,
     "descripcion": "Fuga de agua bajo el lavaplatos de la cocina."},
    {"id": 209, "fecha": "12 sep 2026", "categoria": "Electricidad", "icono": "bi-lightning-charge-fill",
     "tecnico": "Andrea Molina", "estado": "finalizada", "calificada": False,
     "descripcion": "Tomacorriente de la sala hace chispa al conectar."},
    {"id": 198, "fecha": "29 ago 2026", "categoria": "Cerrajería", "icono": "bi-key-fill",
     "tecnico": "Jhon Fredy Pardo", "estado": "finalizada", "calificada": True,
     "descripcion": "Cambio de guardas de la puerta principal."},
    {"id": 190, "fecha": "20 ago 2026", "categoria": "Electrodomésticos", "icono": "bi-tv-fill",
     "tecnico": None, "estado": "pendiente", "calificada": False,
     "descripcion": "La lavadora no centrifuga."},
    {"id": 181, "fecha": "02 ago 2026", "categoria": "Plomería", "icono": "bi-droplet-half",
     "tecnico": None, "estado": "cancelada", "calificada": False,
     "descripcion": "Destape de lavamanos del baño."},
]

SOLICITUDES_TECNICO = [
    {"id": 301, "cliente": "Laura Gómez", "categoria": "Plomería", "icono": "bi-droplet-half",
     "descripcion": "Fuga de agua bajo el lavaplatos de la cocina. Gotea constante desde ayer.",
     "direccion": "Cra 13 #52-40, apto 302", "fecha": "Hoy, 8:42 a. m.", "urgente": True, "fotos": 2},
    {"id": 302, "cliente": "Mateo Herrera", "categoria": "Plomería", "icono": "bi-droplet-half",
     "descripcion": "Cambio de la grifería del baño principal, ya tengo el repuesto.",
     "direccion": "Cl 63 #9-15", "fecha": "Hoy, 7:10 a. m.", "urgente": False, "fotos": 0},
    {"id": 303, "cliente": "Paola Ortiz", "categoria": "Plomería", "icono": "bi-droplet-half",
     "descripcion": "El inodoro no llena bien el tanque y suena todo el tiempo.",
     "direccion": "Av. Caracas #45-20", "fecha": "Ayer, 6:30 p. m.", "urgente": False, "fotos": 1},
]

TECNICOS_PENDIENTES = [
    {"id": 41, "nombre": "Ricardo Suárez", "cedula": "1090456123", "correo": "ricardo.suarez@correo.com",
     "telefono": "300 123 4567", "especialidad": "Electricidad", "ciudad": "Bogotá",
     "registro": "10 sep 2026", "documento": "certificado_ricardo.pdf"},
    {"id": 42, "nombre": "Marcela Duarte", "cedula": "52874109", "correo": "marcela.duarte@correo.com",
     "telefono": "311 765 4321", "especialidad": "Electrodomésticos", "ciudad": "Bogotá",
     "registro": "14 sep 2026", "documento": "certificacion_sena_marcela.png"},
    {"id": 43, "nombre": "Óscar Ballesteros", "cedula": "80123456", "correo": "oscar.b@correo.com",
     "telefono": "320 555 0198", "especialidad": "Cerrajería", "ciudad": "Soacha",
     "registro": "17 sep 2026", "documento": "curso_cerrajeria_oscar.pdf"},
]
