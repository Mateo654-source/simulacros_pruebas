import csv

def exportar_reporte(prestamos):
    mes = input("Mes (MM): ")
    anio = input("Año (YYYY): ")

    filtrados = [
        p for p in prestamos
        if p["estado"] == "DEVUELTO" and p["mes"] == mes and p["anio"] == anio
    ]

    if not filtrados:
        print("❌ No hay datos")
        return

    nombre = f"reporte_prestamos_{anio}_{mes}.csv"
    with open(nombre, "w", newline="", encoding="utf-8") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=filtrados[0].keys())
        escritor.writeheader()
        escritor.writerows(filtrados)

    print(f"✅ Reporte generado: {nombre}")
