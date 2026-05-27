import json
import os

RUTA_DATOS = 'data/agenda.json'
RUTA_REPORTE = 'data/reporte_auditoria_datos.json'

def auditar_datos():
    print('\n==================================================')
    print('          INICIANDO AUDITORÍA DE DATOS ACME       ')
    print('==================================================')

    if not os.path.exists(RUTA_DATOS):
        print(f"[ERROR]: No se encontró el archivo de datos en '{RUTA_DATOS}'.")
        return

    with open(RUTA_DATOS, 'r', encoding='utf-8') as archivo:
        try:
            datos_sistema = json.load(archivo)
        except json.JSONDecodeError:
            print("[ERROR]: El archivo JSON original tiene un error de sintaxis y no se puede leer.")
            return

    usuarios_con_errores = []
    contactos_con_errores = []
    
    emails_usuarios_vistos = set()
    emails_usuarios_duplicados = set()
    
    ids_contactos_vistos = set()
    ids_contactos_duplicados = set()

    # --- VALIDACIÓN DE USUARIOS ACME ---
    campos_usuarios = ['id', 'nombre', 'apellido', 'telefono', 'email', 'password', 'rol']
    roles_permitidos = ['administrador', 'operario']

    for usr in datos_sistema.get('usuarios', []):
        errores_usr = []
        usr_id = usr.get('id', 'Desconocido')
        usr_email = usr.get('email', '')

        for campo in campos_usuarios:
            if campo not in usr or str(usr[campo]).strip() == '':
                errores_usr.append(f"Falta el campo obligatorio o está vacío: {campo}")

        if 'telefono' in usr and str(usr['telefono']).strip() != '':
            try:
                int(str(usr['telefono']).strip())
            except ValueError:
                errores_usr.append(f"El teléfono '{usr['telefono']}' no es un número válido.")

        if 'email' in usr and str(usr['email']).strip() != '':
            email_str = str(usr['email']).strip()
            if "@" not in email_str or "." not in email_str or email_str.endswith("@") or email_str.endswith("."):
                errores_usr.append(f"El email '{email_str}' tiene un formato inválido.")
            
            if email_str in emails_usuarios_vistos:
                emails_usuarios_duplicados.add(email_str)
                errores_usr.append(f"El email '{email_str}' está duplicado.")
            else:
                emails_usuarios_vistos.add(email_str)

        if 'rol' in usr and str(usr['rol']).strip() not in roles_permitidos:
            errores_usr.append(f"El rol '{usr['rol']}' no está permitido (solo: {', '.join(roles_permitidos)}).")

        if errores_usr:
            identificador = usr_email if usr_email else f"ID-{usr_id}"
            usuarios_con_errores.append({
                "email_o_id": identificador,
                "errores": errores_usr
            })

    # --- VALIDACIÓN DE CONTACTOS ACME ---
    # Nota: Agregamos tipo_contacto por requerimiento del examen
    campos_contactos = ['id', 'nombre', 'apellido', 'telefono', 'email', 'tipo_contacto']
    tipos_contacto_permitidos = ['cliente', 'proveedor', 'aliado', 'personal']

    for con in datos_sistema.get('contactos', []):
        errores_con = []
        con_id = con.get('id', 'Desconocido')

        # ESCUDO: Si tus contactos viejos no tienen tipo_contacto, les asignamos 'personal' temporalmente para que no fallen por defecto
        if 'tipo_contacto' not in con:
            con['tipo_contacto'] = 'personal'

        for campo in campos_contactos:
            if campo not in con or str(con[campo]).strip() == '':
                errores_con.append(f"Falta el campo obligatorio o está vacío: {campo}")

        if 'telefono' in con and str(con['telefono']).strip() != '':
            try:
                int(str(con['telefono']).strip())
            except ValueError:
                errores_con.append(f"El teléfono '{con['telefono']}' no es un número válido.")

        if 'email' in con and str(con['email']).strip() != '':
            email_str = str(con['email']).strip()
            if "@" not in email_str or "." not in email_str or email_str.endswith("@") or email_str.endswith("."):
                errores_con.append(f"El email '{email_str}' tiene un formato inválido.")

        if 'tipo_contacto' in con and str(con['tipo_contacto']).strip() not in tipos_contacto_permitidos:
            errores_con.append(f"El tipo de contacto '{con['tipo_contacto']}' no es válido (Permitidos: {', '.join(tipos_contacto_permitidos)}).")

        if 'id' in con and str(con['id']).strip() != '':
            if con_id in ids_contactos_vistos:
                ids_contactos_duplicados.add(con_id)
                errores_con.append(f"El ID de contacto '{con_id}' está duplicado.")
            else:
                ids_contactos_vistos.add(con_id)

        if errores_con:
            contactos_con_errores.append({
                "id": con_id,
                "errores": errores_con
            })

    # --- GENERAR RESUMEN Y REPORTE ---
    resumen = {
        "total_usuarios": len(datos_sistema.get('usuarios', [])),
        "total_contactos": len(datos_sistema.get('contactos', [])),
        "usuarios_con_errores": len(usuarios_con_errores),
        "contactos_con_errores": len(contactos_con_errores),
        "usuarios_con_email_duplicado": len(emails_usuarios_duplicados),
        "contactos_con_id_duplicado": len(ids_contactos_duplicados)
    }

    reporte_final = {
        "mensaje_global": "No se encontraron errores en la base de datos.",
        "usuarios_con_errores": usuarios_con_errores,
        "contactos_con_errores": contactos_con_errores,
        "resumen": resumen
    }
    
    if usuarios_con_errores or contactos_con_errores:
        reporte_final["mensaje_global"] = "Inconsistencias de datos detectadas."

    with open(RUTA_REPORTE, 'w', encoding='utf-8') as archivo_reporte:
        json.dump(reporte_final, archivo_reporte, indent=4, ensure_ascii=False)

    print(f"[ÉXITO]: Auditoría completada. Reporte generado en '{RUTA_REPORTE}'.")