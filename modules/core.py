import json
import os

# Definición de ruta donde almacena la información
RUTA_DATA = 'data/agenda.json'

# Verifica si existe el json
def carga_datos():
    if not os.path.exists('data'):
        os.makedirs('data')

    if not os.path.exists(RUTA_DATA):
        # Estructura para la base de datos
        estructuraInicial = {
            'usuarios': [ 
                {
                    'id': 0, # ID numérico base
                    'nombre': 'admin',
                    'apellido': 'administrador',
                    'telefono': '555000111',
                    'email': 'admin@acmesolutions.com',
                    'direccion': 'Cl 185 # 26 - 85',
                    'password': 'admin123',
                    'rol': 'administrador'
                }
            ],
            'contactos': []
        }
        # Comprobamos que el archivo existe, si es así lo abre en modo escritura (w)
        with open(RUTA_DATA, 'w', encoding='utf-8') as archivo:
            json.dump(estructuraInicial, archivo, indent=4, ensure_ascii=False) # .dump convierte el diccionario en texto con formato json
        
        return estructuraInicial
    
    else:
        # Abrimos el archivo en modo lectura ('r')
        with open(RUTA_DATA, 'r', encoding='utf8') as archivo:
            datos = json.load(archivo) # .load transforma el json devuelta a diccionario de python
        
        return datos
    
def guardar_datos(datos):
    with open(RUTA_DATA, 'w', encoding='utf-8') as archivo:
        # Guardamos el diccionario actualizado
        json.dump(datos, archivo, indent=4, ensure_ascii=False)

def leer_texto_obligatorio(mensaje_input):
    '''Obliga al usuario a ingresar un texto y no lo deja pasar si está vacío.'''
    while True:
        valor = input(mensaje_input).strip()
        if valor != '':
            return valor
        print('[ERROR]: Este campo es obligatorio. No puede dejarlo vacío.')

def leer_entero_obligatorio(mensaje_input):
    #Obliga al usuario a ingresar un número entero obligatorio sin romper el programa.
    while True:
        try:
            valor = input(mensaje_input).strip()
            if valor == '':
                print('[ERROR]: Este campo es obligatorio. Intente de nuevo.')
                continue
            # ESCUDO: Evita números absurdamente largos que congelen la terminal (máximo 15 dígitos)
            if len(valor) > 15:
                print('[ERROR]: El número ingresado es demasiado largo. Intente de nuevo.')
                continue
            return int(valor)
        except ValueError:
            print('[ERROR]: Entrada no válida. Debe ingresar un número entero obligatorio.')