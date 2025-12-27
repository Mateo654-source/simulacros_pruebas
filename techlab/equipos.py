import csv
from datetime import datetime

RUTA_EQUIPOS = "data/equipos.csv"

def cargar_equipos():
    equipos = []
    with open(RUTA_EQUIPOS, newline="", encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo)
        for fila in lector:
            equipos.append(fila)
    return equipos

def guardar_equipos(equipos):
    with open(RUTA_EQUIPOS, "w", newline="", encoding="utf-8") as archivo:
        campos = equipos[0].keys() if equipos else [
            "equipo_id","nombre_equipo","categoria","estado_actual","fecha_registro","descripcion"
        ]
        escritor = csv.DictWriter(archivo, fieldnames=campos)
        escritor.writeheader()
        escritor.writerows(equipos)

def registrar_equipo(equipos):
    equipo = {
        "equipo_id": input("ID del equipo: "),
        "nombre_equipo": input("Nombre: "),
        "categoria": input("Categoría: "),
        "estado_actual": "DISPONIBLE",
        "fecha_registro": datetime.now().strftime("%Y-%m-%d"),
        "descripcion": input("Descripción (opcional): ")
    }
    equipos.append(equipo)
    guardar_equipos(equipos)
    print("✅ Equipo registrado")

def listar_equipos(equipos):
    for e in equipos:
        print(f"{e['equipo_id']} | {e['nombre_equipo']} | {e['categoria']} | {e['estado_actual']}")

def buscar_equipo(equipos, equipo_id):
    for e in equipos:
        if e["equipo_id"] == equipo_id:
            return e
    return None

def actualizar_estado_equipo(equipos, equipo_id, estado):
    for e in equipos:
        if e["equipo_id"] == equipo_id:
            e["estado_actual"] = estado
            guardar_equipos(equipos)
            return
