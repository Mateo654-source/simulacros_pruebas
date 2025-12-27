from auth import login
from espacios import *
from reservas import *
from reportes import exportar_reservas

def menu():
    espacios = cargar_espacios()
    reservas = cargar_reservas()

    while True:
        print("""
1. Registrar espacio
2. Listar espacios
3. Solicitar reserva
4. Aprobar / Rechazar reserva
5. Finalizar reserva
6. Exportar reporte
0. Salir
""")
        op = input("Opción: ").strip()

        if op == "1": registrar_espacio(espacios)
        elif op == "2": listar_espacios(espacios)
        elif op == "3": solicitar_reserva(espacios, reservas)
        elif op == "4": aprobar_rechazar(espacios, reservas)
        elif op == "5": finalizar_reserva(espacios, reservas)
        elif op == "6": exportar_reservas(reservas)
        elif op == "0": break
        else: print("❌ Opción inválida")

def main():
    if login():
        menu()

if __name__ == "__main__":
    main()
