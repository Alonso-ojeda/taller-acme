import modules.core as cr

def registrarContacto(datos_sistema):
    print('\n--- REGISTRAR NUEVO CONTACTO ---')
    
    # Validación de Teléfono Único
    while True:
        telefono = cr.leer_entero_obligatorio('Ingrese el número de teléfono: ')
        
        # Buscamos que este int no esté repetido en el JSON
        telefono_duplicado = False
        for con in datos_sistema['contactos']:
            if con['telefono'] == telefono:
                print(f"\n[ALERTA]: Este número ya lo tienes agendado con el nombre de: {con['nombre'].capitalize()} {con['apellido'].capitalize()}.")
                print('Por favor, intente con un número diferente.\n')
                telefono_duplicado = True
                break
        
        if not telefono_duplicado:
            break # Si no está duplicado, sale del bucle
            
    # Validación estricta de Cadenas de Texto
    nombre = cr.leer_texto_obligatorio('Ingrese el nombre: ').strip().lower()
    apellido = cr.leer_texto_obligatorio('Ingrese el apellido: ').strip().lower()
    
    # ESCUDO PREMIUM: Validación de formato estructurado de correo electrónico al registrar contacto
    while True:
        email = cr.leer_texto_obligatorio('Ingrese el correo electrónico: ').strip().lower()
        if "@" not in email or "." not in email or email.endswith("@") or email.endswith("."):
            print("[ERROR]: El formato del correo no es válido (ejemplo: contacto@correo.com).")
            continue
        break
    
    # GENERACIÓN AUTOMÁTICA DEL ID PARA CONTACTOS SEGURO
    if not datos_sistema['contactos']:
        id_automatico = 1 # Primer contacto en la agenda si está totalmente vacía
    else:
        # Tomamos el ID y sumamos 1 
        id_automatico = int(datos_sistema['contactos'][-1]['id']) + 1
    
    nuevo_contacto = {
        'id': id_automatico,
        'nombre': nombre,
        'apellido': apellido,
        'telefono': telefono,
        'email': email
    }
    
    datos_sistema['contactos'].append(nuevo_contacto)
    cr.guardar_datos(datos_sistema)
    
    # Le informamos al usuario el ID asignado automáticamente por debajo
    print(f'\nContacto {nombre.capitalize()} registrado con éxito con el ID automático: {id_automatico}')


def listarContactos(datos_sistema):
    print('\n================================================================================')
    print('                          LISTA DE CONTACTOS GUARDADOS                          ')
    print('================================================================================')
    
    if not datos_sistema['contactos']:
        print('La agenda de contactos está vacía.')

    else:
        for contacto in datos_sistema['contactos']:
            print(f"ID: {contacto['id']} | Nombre: {contacto['nombre'].capitalize()} {contacto['apellido'].capitalize()}")
            print(f"Teléfono: {contacto['telefono']} | Email: {contacto['email']}")
            print('--------------------------------------------------------------------------------')


def modificarContacto(datos_sistema):
    print('\n--- MODIFICAR / EDITAR CONTACTO ---')
    # Se busca obligatoriamente mediante el ID de tipo int
    id_buscar = cr.leer_entero_obligatorio('Ingrese el ID del contacto que desea editar: ')
    
    contacto_encontrado = None
    for contacto in datos_sistema['contactos']:
        if contacto['id'] == id_buscar:
            contacto_encontrado = contacto
            break
            
    if contacto_encontrado:
        print(f"\nContacto encontrado: {contacto_encontrado['nombre'].capitalize()} {contacto_encontrado['apellido'].capitalize()}")
        print('Ingrese los nuevos datos para actualizar. (El ID no se puede modificar).\n')
        
        # El ID se queda totalmente protegido e intacto, no permitimos que se altere
        contacto_encontrado['nombre'] = cr.leer_texto_obligatorio('Nuevo nombre: ').strip().lower()
        contacto_encontrado['apellido'] = cr.leer_texto_obligatorio('Nuevo apellido: ').strip().lower()
        
        # Validamos que el nuevo teléfono (int) tampoco choque con el de alguien más al editar
        while True:
            nuevo_tel = cr.leer_entero_obligatorio('Nuevo teléfono: ')
            if nuevo_tel == contacto_encontrado['telefono']: 
                break # Dejó el mismo número actual, es completamente válido
                
            duplicado = False
            for con in datos_sistema['contactos']:
                if con['telefono'] == nuevo_tel:
                    print(f"\n[ERROR]: Ese número ya le pertenece a {con['nombre'].capitalize()}. Intente otro.\n")
                    duplicado = True
                    break
            if not duplicado:
                contacto_encontrado['telefono'] = nuevo_tel
                break
                
        # ESCUDO PREMIUM: Agregada validación de formato de correo con '@' y '.' al modificar contacto
        while True:
            nuevo_email = cr.leer_texto_obligatorio('Nuevo correo electrónico: ').strip().lower()
            if "@" not in nuevo_email or "." not in nuevo_email or nuevo_email.endswith("@") or nuevo_email.endswith("."):
                print("[ERROR]: El formato del correo no es válido (debe incluir '@' y un dominio válido).")
                continue
            contacto_encontrado['email'] = nuevo_email
            break
        
        cr.guardar_datos(datos_sistema)
        print(f'\nContacto con ID {id_buscar} actualizado con éxito')
    else:
        print(f'\n[ERROR]: No se encontró ningún contacto con el ID {id_buscar}.')


def eliminarContacto(datos_sistema):
    print('\n--- ELIMINAR CONTACTO ---')
    # Se busca por ID de tipo int obligatorio
    id_buscar = cr.leer_entero_obligatorio('Ingrese el ID del contacto que desea eliminar: ')
    
    contacto_encontrado = None
    for contacto in datos_sistema['contactos']:
        if contacto['id'] == id_buscar:
            contacto_encontrado = contacto
            break
            
    if contacto_encontrado:
        datos_sistema['contactos'].remove(contacto_encontrado)
        cr.guardar_datos(datos_sistema)
        print(f"\nEl contacto {contacto_encontrado['nombre'].capitalize()} ha sido eliminado correctamente")

    else:
        print(f'\n[ERROR]: No se encontró ningún contacto con el ID {id_buscar}.')