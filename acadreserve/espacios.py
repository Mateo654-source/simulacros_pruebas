import csv
from datetime import datetime

RUTA = "espacios.csv"

def cargar_espacios():
    try:
        with open(RUTA, newline="", encoding="utf-8") as f:
            return list(csv.DictReader(f))
    except FileNotFoundError:
        return []

def guardar_espacios(espacios):
    with open(RUTA, "w", newline="", encoding="utf-8") as f:
        campos = ["espacio_id","nombre_espacio","tipo","capacidad","estado_actual","fecha_registro"]
        writer = csv.DictWriter(f, fieldnames=campos)
        writer.writeheader()
        writer.writerows(espacios)

def registrar_espacio(espacios):
    eid = input("ID espacio: ").strip()
    if any(e["espacio_id"] == eid for e in espacios):
        print("❌ ID duplicado")
        return

    try:
        capacidad = int(input("Capacidad: "))
    except ValueError:
        print("❌ Capacidad inválida")
        return

    espacio = {
        "espacio_id": eid,
        "nombre_espacio": input("Nombre: ").strip(),
        "tipo": input("Tipo (AULA/LABORATORIO/SALA_ESPECIAL): ").strip(),
        "capacidad": capacidad,
        "estado_actual": "DISPONIBLE",
        "fecha_registro": datetime.now().strftime("%Y-%m-%d")
    }

    espacios.append(espacio)
    guardar_espacios(espacios)
    print("✅ Espacio registrado")

def listar_espacios(espacios):
    for e in espacios:
        print(f"{e['espacio_id']} | {e['nombre_espacio']} | {e['tipo']} | {e['capacidad']} | {e['estado_actual']}")

def actualizar_estado(espacios, espacio_id, estado):
    for e in espacios:
        if e["espacio_id"] == espacio_id:
            e["estado_actual"] = estado
            guardar_espacios(espacios)
            return
