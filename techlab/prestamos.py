import csv
from datetime import datetime
from equipos import actualizar_estado_equipo

RUTA_PRESTAMOS = "data/prestamos.csv"

LIMITES = {
    "ESTUDIANTE": 3,
    "INSTRUCTOR": 7,
    "ADMINISTRATIVO": 10
}

def cargar_prestamos():
    prestamos = []
    with open(RUTA_PRESTAMOS, newline="", encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo)
        for fila in lector:
            prestamos.append(fila)
    return prestamos

def guardar_prestamos(prestamos):
    with open(RUTA_PRESTAMOS, "w", newline="", encoding="utf-8") as archivo:
        campos = prestamos[0].keys() if prestamos else [
            "prestamo_id","equipo_id","nombre_equipo","usuario_prestatario",
            "tipo_usuario","fecha_solicitud","fecha_prestamo","fecha_devolucion",
            "dias_autorizados","dias_reales_usados","retraso","estado","mes","anio"
        ]
        escritor = csv.DictWriter(archivo, fieldnames=campos)
        escritor.writeheader()
        escritor.writerows(prestamos)

def registrar_solicitud(equipos, prestamos):
    equipo_id = input("ID del equipo: ")
    equipo = next((e for e in equipos if e["equipo_id"] == equipo_id), None)

    if not equipo or equipo["estado_actual"] != "DISPONIBLE":
        print("❌ Equipo no disponible")
        return

    tipo = input("Tipo usuario (ESTUDIANTE/INSTRUCTOR/ADMINISTRATIVO): ").upper()
    dias = int(input("Días solicitados: "))

    if tipo not in LIMITES or dias > LIMITES[tipo]:
        print("❌ Días exceden el límite")
        return

    fecha = input("Fecha préstamo (YYYY-MM-DD): ")
    datetime.strptime(fecha, "%Y-%m-%d")

    prestamo = {
        "prestamo_id": str(len(prestamos) + 1),
        "equipo_id": equipo_id,
        "nombre_equipo": equipo["nombre_equipo"],
        "usuario_prestatario": input("Nombre solicitante: "),
        "tipo_usuario": tipo,
        "fecha_solicitud": datetime.now().strftime("%Y-%m-%d"),
        "fecha_prestamo": fecha,
        "fecha_devolucion": "",
        "dias_autorizados": dias,
        "dias_reales_usados": "",
        "retraso": "",
        "estado": "PENDIENTE",
        "mes": fecha.split("-")[1],
        "anio": fecha.split("-")[0]
    }

    prestamos.append(prestamo)
    guardar_prestamos(prestamos)
    print("✅ Solicitud registrada")

def aprobar_rechazar(equipos, prestamos):
    pendientes = [p for p in prestamos if p["estado"] == "PENDIENTE"]

    for p in pendientes:
        print(p["prestamo_id"], p["nombre_equipo"])

    pid = input("ID préstamo: ")
    decision = input("Aprobar (A) / Rechazar (R): ").upper()

    for p in prestamos:
        if p["prestamo_id"] == pid:
            if decision == "A":
                p["estado"] = "APROBADO"
                actualizar_estado_equipo(equipos, p["equipo_id"], "PRESTADO")
            else:
                p["estado"] = "RECHAZADO"

    guardar_prestamos(prestamos)

def registrar_devolucion(equipos, prestamos):
    activos = [p for p in prestamos if p["estado"] == "APROBADO"]

    for p in activos:
        print(p["prestamo_id"], p["nombre_equipo"])

    pid = input("ID préstamo: ")
    fecha_dev = input("Fecha devolución (YYYY-MM-DD): ")

    for p in prestamos:
        if p["prestamo_id"] == pid:
            f1 = datetime.strptime(p["fecha_prestamo"], "%Y-%m-%d")
            f2 = datetime.strptime(fecha_dev, "%Y-%m-%d")
            dias = (f2 - f1).days

            p["fecha_devolucion"] = fecha_dev
            p["dias_reales_usados"] = dias
            p["retraso"] = "SI" if dias > int(p["dias_autorizados"]) else "NO"
            p["estado"] = "DEVUELTO"

            actualizar_estado_equipo(equipos, p["equipo_id"], "DISPONIBLE")

    guardar_prestamos(prestamos)
