import modules.core as cr

def login(datos_sistema):
    print('\n---- INICIO DE SESION')

    # Bucle infinito hasta que los datos sean correctos
    while True:
        correo = cr.leer_texto_obligatorio('ingreasa tu correo corporativo: ').strip().lower()
        # ESCUDO: Se agregó .strip() para limpiar espacios invisibles accidentales al final de la contraseña
        contrasenia = cr.leer_texto_obligatorio('ingresa tu contraseña: ').strip()

        for usuario in datos_sistema['usuarios']:
            if correo == usuario['email'] and contrasenia == usuario['password']:
                print('¡Inicio de sesión exitoso!') 
                return usuario # Devolvemos el diccionario del usuario.
            
        print('ERROR EL CORREO O LA CONTRASEÑA SON INCORECTOS. INTENTE NUEVAMENTE.\n')


def registrarUsuarios(datos_sistema):
    print('\n--- REGISTRAR NUEVO OPERARIO ---')

    # ESCUDO: Añadidos métodos .strip() para eliminar barras espaciadoras accidentales
    nombre = cr.leer_texto_obligatorio('Ingrese el nombre: ').strip().lower()
    apellido = cr.leer_texto_obligatorio('Ingrese el apellido: ').strip().lower()
    telefono = cr.leer_entero_obligatorio('Ingrese el telefono: ')

    while True:#obligamos al administador que ingrese el coreo con el @ y el .com
        email = cr.leer_texto_obligatorio('Ingrese el email: ').strip().lower()
        # ESCUDO PREMIUM: Valida que contenga '@', un '.' y que no termine en caracteres basura
        if "@" not in email or "." not in email or email.endswith("@") or email.endswith("."):
            print("[ERROR]: El formato del correo no es válido (ejemplo: usuario@correo.com).")
            continue
            
        correo_repetido = False
        for usr_existente in datos_sistema['usuarios']:
            if usr_existente['email'] == email:
                print(f"\n[ALERTA]: El correo '{email}' ya está registrado con otro usuario.")
                print("Por favor, ingrese un correo diferente.\n")
                correo_repetido = True
                break
        
        if not correo_repetido:
            break

    password = cr.leer_texto_obligatorio('Ingrese la contraseña: ').strip()
    
    while True: # Aquí hacemos esto para que el rol solo pueda ser admin u operario.
        rol = input('Ingrese el rol (administrador o operario): ').strip().lower()
        
        if rol == 'administrador' or rol == 'operario':
            break # Si es correcto, rompe el bucle y continúa
        else:
            print('\n[ERROR]: Rol no válido. Solo se permite "administrador" o "operario". Intente de nuevo.\n')

    
    # GENERACIÓN AUTOMÁTICA DEL ID SEGURO
    if not datos_sistema['usuarios']:
        id_automatico = 1 # ESCUDO: Si la lista llegara a quedar vacía por completo
    else:
        # Tomamos el ID del último usuario registrado en la lista y le sumamos 1
        id_automatico = datos_sistema['usuarios'][-1]['id'] + 1

    nuevoUsuario = {
        'id': id_automatico,
        'nombre': nombre,
        'apellido': apellido,
        'telefono': telefono,
        'email': email,
        'password': password,
        'rol': rol
    }

    datos_sistema['usuarios'].append(nuevoUsuario)
    cr.guardar_datos(datos_sistema)
    
    #Le mostramos el ID asignado automáticamente al usuario
    print(f'\nUsuario {nombre.capitalize()} registrado con éxito en el sistema con el ID: {id_automatico}')


def listarUsuarios(datos_sistema):
    print('\n================================================================================')
    print('                          LISTA DE USUARIOS REGISTRADOS                          ')
    print('================================================================================')
    
    # Verificamos si la lista de usuarios está vacía
    if not datos_sistema['usuarios']:
        print('No hay usuarios registrados en el sistema.')
    else:
        for usuario in datos_sistema['usuarios']: # Recorremos la lista de usuarios con este for.
            print(f"ID: {usuario['id']} | Nombre: {usuario['nombre'].capitalize()} {usuario['apellido'].capitalize()}")
            print(f"Rol: {usuario['rol']} | Email: {usuario['email']} | Teléfono: {usuario['telefono']}")
            print('--------------------------------------------------------------------------------')


def modificarUsuario(datos_sistema):
    print('\n--- EDITAR DATOS DE OPERARIO ---')
    # Pedimos el ID para buscarlo (este sí es obligatorio)
    id_buscar = cr.leer_entero_obligatorio('Ingrese el ID del operario que desea modificar: ')
    
    usuario_encontrado = None
    for usuario in datos_sistema['usuarios']:
        if usuario['id'] == id_buscar:
            usuario_encontrado = usuario
            break
            
    if usuario_encontrado:
        print(f"\nUsuario encontrado: {usuario_encontrado['nombre'].capitalize()} {usuario_encontrado['apellido'].capitalize()}")
        print("Presione [ENTER] para conservar el valor actual si no desea modificarlo.\n")
        
        # REQUERIMIENTO PROFESOR: Modificar Nombre de forma opcional
        cambio = input(f"Nuevo nombre ({usuario_encontrado['nombre']}): ").strip().lower()
        if cambio != '':
            usuario_encontrado['nombre'] = cambio

        # REQUERIMIENTO PROFESOR: Modificar Apellido de forma opcional
        cambio = input(f"Nuevo apellido ({usuario_encontrado['apellido']}): ").strip().lower()
        if cambio != '':
            usuario_encontrado['apellido'] = cambio

        # REQUERIMIENTO PROFESOR: Modificar Teléfono de forma opcional
        while True:
            cambio = input(f"Nuevo teléfono ({usuario_encontrado['telefono']}): ").strip()
            if cambio == '':
                break # Conserva el actual
            try:
                usuario_encontrado['telefono'] = int(cambio)
                break
            except ValueError:
                print('[ERROR]: Entrada no válida. Debe ingresar un número entero o presionar [ENTER].')
        
        # REQUERIMIENTO PROFESOR: Modificar Correo electrónico de forma opcional
        while True:
            cambio = input(f"Nuevo correo electrónico ({usuario_encontrado['email']}): ").strip().lower()
            if cambio == '':
                break # Conserva el actual
                
            if "@" not in cambio or "." not in cambio or cambio.endswith("@") or cambio.endswith("."):
                print("[ERROR]: El formato del correo no es válido (ejemplo: usuario@correo.com).")
                continue
                
            if cambio == usuario_encontrado['email']:
                break
                
            # Verificar duplicados con otros usuarios
            correo_repetido = False
            for usr in datos_sistema['usuarios']:
                if usr['email'] == cambio:
                    print(f"\n[ERROR]: El correo '{cambio}' ya le pertenece a otro operario. Intente otro.\n")
                    correo_repetido = True
                    break
            if not correo_repetido:
                usuario_encontrado['email'] = cambio
                break

        # REQUERIMIENTO PROFESOR: Modificar Contraseña de forma opcional
        cambio = input(f"Nueva contraseña ({usuario_encontrado['password']}): ").strip()
        if cambio != '':
            usuario_encontrado['password'] = cambio
        
        # REQUERIMIENTO PROFESOR: Modificar Rol de forma opcional
        while True:
            cambio = input(f"Nuevo rol ({usuario_encontrado['rol']} - administrador/operario): ").strip().lower()
            if cambio == '':
                break # Conserva el actual
            if cambio == 'administrador' or cambio == 'operario':
                usuario_encontrado['rol'] = cambio
                break
            else:
                print('\n[ERROR]: Rol no válido. Intente de nuevo.\n')
                
        cr.guardar_datos(datos_sistema)
        print(f"\nEl operario con ID {id_buscar} ha sido actualizado con éxito")
    else:
        print(f'\n[ERROR]: No se encontró ningún usuario con el ID {id_buscar}.')


def eliminarUsuario(datos_sistema):
    print('\n--- DAR DE BAJA / ELIMINAR OPERARIO ---')
    id_buscar = cr.leer_entero_obligatorio('Ingrese el ID del operario que desea eliminar: ')
    
    usuario_encontrado = None
    for usuario in datos_sistema['usuarios']:
        if usuario['id'] == id_buscar:
            usuario_encontrado = usuario
            break
            
    if usuario_encontrado:
        # Protección para que no se borre el admin por defecto
        if usuario_encontrado['id'] == 0: 
            print('\n[ERROR]: No se puede eliminar al Administrador principal del sistema.')
        else:
            datos_sistema['usuarios'].remove(usuario_encontrado)
            cr.guardar_datos(datos_sistema)
            print(f"\nEl usuario {usuario_encontrado['nombre'].capitalize()} ha sido eliminado correctamente")
    else:
        print(f'\n[ERROR]: No se encontró ningún operario con el ID {id_buscar}.')