from usuarios import login
from equipos import *
from prestamos import *
from reportes import exportar_reporte

def menu():
    equipos = cargar_equipos()
    prestamos = cargar_prestamos()

    while True:
        print("""
1. Registrar equipo
2. Listar equipos
3. Solicitar préstamo
4. Aprobar / Rechazar préstamo
5. Registrar devolución
6. Exportar reporte
0. Salir
""")
        op = input("Opción: ")

        if op == "1":
            registrar_equipo(equipos)
        elif op == "2":
            listar_equipos(equipos)
        elif op == "3":
            registrar_solicitud(equipos, prestamos)
        elif op == "4":
            aprobar_rechazar(equipos, prestamos)
        elif op == "5":
            registrar_devolucion(equipos, prestamos)
        elif op == "6":
            exportar_reporte(prestamos)
        elif op == "0":
            break

def main():
    if login():
        menu()

if __name__ == "__main__":
    main()
