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
    # Pedimos el ID para buscarlo
    id_buscar = cr.leer_entero_obligatorio('Ingrese el ID del operario que desea modificar: ')
    
    usuario_encontrado = None
    for usuario in datos_sistema['usuarios']:
        if usuario['id'] == id_buscar:
            usuario_encontrado = usuario
            break
            
    if usuario_encontrado:
        print(f"\nUsuario encontrado: {usuario_encontrado['nombre'].capitalize()} {usuario_encontrado['apellido'].capitalize()}")
        print("Ingrese los nuevos datos para actualizar la información. (El ID no se puede modificar).\n")
        
        usuario_encontrado['nombre'] = cr.leer_texto_obligatorio('Nuevo nombre: ').strip().lower()
        usuario_encontrado['apellido'] = cr.leer_texto_obligatorio('Nuevo apellido: ').strip().lower()
        usuario_encontrado['telefono'] = cr.leer_entero_obligatorio('Nuevo teléfono: ')
        
        # para evitar correos duplicados o sin '@' al modificar
        while True:
            nuevo_email = cr.leer_texto_obligatorio('Nuevo correo electrónico: ').strip().lower()
            # ESCUDO PREMIUM: Estructura real de correo al modificar
            if "@" not in nuevo_email or "." not in nuevo_email or nuevo_email.endswith("@") or nuevo_email.endswith("."):
                print("[ERROR]: El formato del correo no es válido (ejemplo: usuario@correo.com).")
                continue
                
            if nuevo_email == usuario_encontrado['email']:
                break # Dejó su mismo correo actual, es completamente válido
                
            # Verificamos que este nuevo correo no le pertenezca a otra persona
            correo_repetido = False
            for usr in datos_sistema['usuarios']:
                if usr['email'] == nuevo_email:
                    print(f"\n[ERROR]: El correo '{nuevo_email}' ya le pertenece a otro operario. Intente otro.\n")
                    correo_repetido = True
                    break
            if not correo_repetido:
                usuario_encontrado['email'] = nuevo_email
                break

        usuario_encontrado['password'] = cr.leer_texto_obligatorio('Nueva contraseña: ').strip()
        
        while True:
            rol = input('Nuevo rol (administrador o operario): ').strip().lower()
            if rol == 'administrador' or rol == 'operario':
                usuario_encontrado['rol'] = rol
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