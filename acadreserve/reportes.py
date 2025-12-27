import csv

def exportar_reservas(reservas):
    mes = input("Mes (MM): ").zfill(2)
    anio = input("Año (YYYY): ").strip()

    datos = [r for r in reservas if r["estado"] == "FINALIZADA" and r["mes"] == mes and r["anio"] == anio]
    if not datos:
        print("❌ No hay datos")
        return

    nombre = f"reporte_reservas_{anio}_{mes}.csv"
    with open(nombre, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=datos[0].keys())
        writer.writeheader()
        writer.writerows(datos)

    print(f"✅ Reporte generado: {nombre}")
