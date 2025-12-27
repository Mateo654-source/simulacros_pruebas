import csv

RUTA_USUARIOS = "data/usuarios.csv"

def cargar_usuarios():
    try:
        with open(RUTA_USUARIOS, newline="", encoding="utf-8") as archivo:
            return list(csv.DictReader(archivo))
    except FileNotFoundError:
        print(" Error: usuarios.csv no encontrado")
        return []

def login():
    usuarios = cargar_usuarios()
    if not usuarios:
        return False
    intentos = 0
    while intentos < 3:
        usuario = input("Usuario: ").strip()
        contrasena = input("Contraseña: ").strip()
        for u in usuarios:
            if u["usuario"] == usuario and u["contrasena"] == contrasena:
                print("Login exitoso\n")
                return True
        intentos += 1
        print(f"Credenciales incorrectas ({intentos}/3)")
    print("Demasiados intentos. Programa finalizado.")
    return False
