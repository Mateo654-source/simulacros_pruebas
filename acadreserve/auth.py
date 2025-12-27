import csv

RUTA_USUARIOS = "usuarios.csv"

def login():
    try:
        with open(RUTA_USUARIOS, newline="", encoding="utf-8") as f:
            usuarios = list(csv.DictReader(f))
    except FileNotFoundError:
        print("usuarios.csv no encontrado")
        return False

    intentos = 0
    while intentos < 3:
        user = input("Usuario: ").strip()
        pwd = input("Contraseña: ").strip()

        for u in usuarios:
            if u["usuario"] == user and u["contrasena"] == pwd:
                print("Login exitoso\n")
                return True

        intentos += 1
        print(f"Credenciales incorrectas ({intentos}/3)")

    print("Demasiados intentos")
    return False
