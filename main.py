import re
import sys  # Para manejar argumentos de línea de comandos

# Diccionario para almacenar variables
variables = {}

def ejecutar_comando(linea):
    linea = linea.strip()

    # Ignorar líneas vacías
    if not linea:
        return

    # Ignorar comentarios
    if linea.startswith("->") or linea.startswith("-/") or linea.endswith("/->"):
        return

    # Manejar print
    match = re.match(r'print\((.*)\);', linea)
    if match:
        contenido = match.group(1).strip()

        # Si es una cadena entre comillas
        if contenido.startswith('"') and contenido.endswith('"'):
            print(contenido[1:-1])
        # Si es una variable
        elif contenido.startswith("$"):
            var_name = contenido[1:]
            print(variables.get(var_name, f"[Error] La variable {var_name} no existe"))
        # Si es una expresión matemática
        else:
            try:
                print(eval(contenido))
            except Exception as e:
                print(f"[Error] Expresión matemática inválida: {e}")
        return

    # Manejar definición de variables (let y const)
    match = re.match(r'(let|const) (\w+)\((int|str|float|bool)\) = (.+);', linea)
    if match:
        tipo = match.group(3)
        nombre = match.group(2)
        valor = match.group(4)

        # Convertir el valor según el tipo
        if tipo == "int":
            valor = int(valor)
        elif tipo == "float":
            valor = float(valor)
        elif tipo == "bool":
            if valor.lower() == "true":
                valor = True
            elif valor.lower() == "false":
                valor = False
            else:
                print(f"[Error] La variable {nombre} debe ser 'true' o 'false'")
                return
        elif tipo == "str":
            if valor.startswith('"') and valor.endswith('"'):
                valor = valor[1:-1]
            else:
                print(f"[Error] La variable {nombre} debe tener un valor de tipo str entre comillas")
                return

        # Guardar la variable
        variables[nombre] = valor
        return

    # Manejar 'mut' para modificar variables
    match = re.match(r'mut (\w+) = (.+);', linea)
    if match:
        nombre = match.group(1)
        valor = match.group(2)

        if nombre in variables:
            # Evaluar expresión matemática
            try:
                variables[nombre] = eval(valor)
            except Exception as e:
                print(f"[Error] Error al modificar la variable {nombre}: {e}")
            return
        else:
            print(f"[Error] La variable {nombre} no está definida.")
            return

    # Manejar `.read()`
    match = re.match(r'print\((.*)\).read\((let \w+\((str|int|float|bool)\))\);', linea)
    if match:
        mensaje = match.group(1).strip()
        tipo = match.group(2)
        nombre = match.group(3).split()[1]

        print(mensaje)
        valor = input()

        # Convertir el input según el tipo
        if tipo == "int":
            valor = int(valor)
        elif tipo == "float":
            valor = float(valor)
        elif tipo == "bool":
            valor = valor.lower() == "true"
        elif tipo == "str":
            valor = valor

        variables[nombre] = valor
        return

    print(f"[Error] Comando no reconocido: {linea}")

# Leer código de Kat-lang desde un archivo
def interpretar_archivo(nombre_archivo):
    try:
        with open(nombre_archivo, 'r') as archivo:
            codigo = archivo.read()
            interpretar(codigo)
    except FileNotFoundError:
        print(f"[Error] El archivo {nombre_archivo} no se encontró.")
    except Exception as e:
        print(f"[Error] Ocurrió un error: {e}")

# Función de interpretación de código
def interpretar(codigo):
    lineas = codigo.split("\n")
    for linea in lineas:
        ejecutar_comando(linea)

# Comprobar si se pasó un archivo como argumento
if len(sys.argv) != 2:
    print("[Error] Debes pasar el nombre del archivo .kat como argumento.")
    sys.exit(1)

# Obtener el nombre del archivo desde los argumentos de línea de comandos
nombre_archivo = sys.argv[1]

# Ejecutar el intérprete para el archivo proporcionado
interpretar_archivo(nombre_archivo)
