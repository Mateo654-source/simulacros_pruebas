import csv, json
from datetime import datetime
from espacios import actualizar_estado

RUTA = "reservas.csv"
CONF = "configuracion.json"

def cargar_config():
    with open(CONF, encoding="utf-8") as f:
        return json.load(f)["limites_por_tipo"]

def cargar_reservas():
    try:
        with open(RUTA, newline="", encoding="utf-8") as f:
            return list(csv.DictReader(f))
    except FileNotFoundError:
        return []

def guardar_reservas(reservas):
    with open(RUTA, "w", newline="", encoding="utf-8") as f:
        campos = reservas[0].keys() if reservas else [
            "reserva_id","espacio_id","nombre_espacio","usuario_reservante",
            "tipo_usuario","fecha_solicitud","fecha_reserva","horas_autorizadas",
            "horas_reales_usadas","exceso_tiempo","estado","mes","anio"
        ]
        writer = csv.DictWriter(f, fieldnames=campos)
        writer.writeheader()
        writer.writerows(reservas)

def solicitar_reserva(espacios, reservas):
    limites = cargar_config()
    eid = input("ID espacio: ").strip()

    espacio = next((e for e in espacios if e["espacio_id"] == eid), None)
    if not espacio or espacio["estado_actual"] != "DISPONIBLE":
        print("❌ Espacio no disponible")
        return

    tipo = input("Tipo usuario: ").upper().strip()
    if tipo not in limites:
        print("❌ Tipo inválido")
        return

    try:
        horas = float(input("Horas solicitadas: "))
    except ValueError:
        print("❌ Horas inválidas")
        return

    if horas > limites[tipo]:
        print("❌ Excede límite permitido")
        return

    fecha = input("Fecha reserva (YYYY-MM-DD): ").strip()
    try:
        datetime.strptime(fecha, "%Y-%m-%d")
    except ValueError:
        print("❌ Fecha inválida")
        return

    reserva = {
        "reserva_id": str(len(reservas) + 1),
        "espacio_id": eid,
        "nombre_espacio": espacio["nombre_espacio"],
        "usuario_reservante": input("Nombre usuario: ").strip(),
        "tipo_usuario": tipo,
        "fecha_solicitud": datetime.now().strftime("%Y-%m-%d"),
        "fecha_reserva": fecha,
        "horas_autorizadas": horas,
        "horas_reales_usadas": "",
        "exceso_tiempo": "",
        "estado": "PENDIENTE",
        "mes": fecha.split("-")[1],
        "anio": fecha.split("-")[0]
    }

    reservas.append(reserva)
    guardar_reservas(reservas)
    print("✅ Reserva registrada")

def aprobar_rechazar(espacios, reservas):
    pendientes = [r for r in reservas if r["estado"] == "PENDIENTE"]
    for r in pendientes:
        print(r["reserva_id"], r["nombre_espacio"])

    rid = input("ID reserva: ").strip()
    r = next((x for x in reservas if x["reserva_id"] == rid), None)
    if not r:
        return

    dec = input("Aprobar (A) / Rechazar (R): ").upper()
    if dec == "A":
        r["estado"] = "APROBADA"
        actualizar_estado(espacios, r["espacio_id"], "RESERVADO")
    else:
        r["estado"] = "RECHAZADA"

    guardar_reservas(reservas)

def finalizar_reserva(espacios, reservas):
    activas = [r for r in reservas if r["estado"] == "APROBADA"]
    for r in activas:
        print(r["reserva_id"], r["nombre_espacio"])

    rid = input("ID reserva: ").strip()
    r = next((x for x in reservas if x["reserva_id"] == rid), None)
    if not r:
        return

    try:
        inicio = float(input("Hora inicio real: "))
        fin = float(input("Hora fin real: "))
    except ValueError:
        print("❌ Horas inválidas")
        return

    horas = fin - inicio
    r["horas_reales_usadas"] = horas
    r["exceso_tiempo"] = "SI" if horas > float(r["horas_autorizadas"]) else "NO"
    r["estado"] = "FINALIZADA"

    actualizar_estado(espacios, r["espacio_id"], "DISPONIBLE")
    guardar_reservas(reservas)
