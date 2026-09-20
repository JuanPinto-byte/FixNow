from django.shortcuts import redirect, render

from . import datos_falsos as d


def _ctx(rol, **extra):
    base = {"rol": rol, "cliente": d.CLIENTE, "n_notif": 3}
    base.update(extra)
    return base


# ---------- Público ----------
def landing(request):
    return render(request, "publico/landing.html", _ctx("publico", categorias=d.CATEGORIAS))


def login_view(request):
    if request.method == "POST":
        # DEMO: mientras no hay autenticación real, el botón elegido decide el rol.
        destino = {
            "cliente": "cliente_inicio",
            "tecnico": "tecnico_solicitudes",
            "admin": "admin_tecnicos",
        }.get(request.POST.get("rol_demo"), "cliente_inicio")
        return redirect(destino)
    return render(request, "publico/login.html", _ctx("publico"))


def registro_cliente(request):
    if request.method == "POST":
        return redirect("cliente_inicio")  # FN-1: entra directo a su panel
    return render(request, "publico/registro_cliente.html", _ctx("publico"))


def registro_tecnico(request):
    if request.method == "POST":
        return render(request, "publico/registro_tecnico_ok.html", _ctx("publico"))  # FN-8
    return render(request, "publico/registro_tecnico.html", _ctx("publico", categorias=d.CATEGORIAS))


# ---------- Cliente ----------
def cliente_inicio(request):
    tecnicos = d.tecnicos()[:4]
    return render(request, "cliente/inicio.html", _ctx(
        "cliente", categorias=d.CATEGORIAS, en_curso=d.SOLICITUD_EN_CURSO, tecnicos=tecnicos))


def solicitud_nueva(request):
    if request.method == "POST":
        return redirect("tecnicos")  # FN-3: al crear, va a técnicos disponibles
    return render(request, "cliente/solicitud_nueva.html", _ctx(
        "cliente", categorias=d.CATEGORIAS, preseleccion=request.GET.get("categoria", "")))


def tecnicos(request):
    return render(request, "cliente/tecnicos.html", _ctx("cliente", tecnicos=d.tecnicos()))


def cliente_historial(request):
    return render(request, "cliente/historial.html", _ctx("cliente", solicitudes=d.HISTORIAL_CLIENTE))


# ---------- Técnico ----------
def tecnico_solicitudes(request):
    return render(request, "tecnico/solicitudes.html", _ctx("tecnico", solicitudes=d.SOLICITUDES_TECNICO))


# ---------- Administrador ----------
def admin_tecnicos(request):
    return render(request, "admin_panel/tecnicos.html", _ctx("admin", pendientes=d.TECNICOS_PENDIENTES))
