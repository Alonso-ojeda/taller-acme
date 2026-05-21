import modules.core as cr
import modules.crudUsers as usr
import modules.messages as msg
import modules.crudContacts as con

if __name__ == '__main__': # para que se ejecute solo desde esta pantalla 
    print('bienvenido al programa de acme para una mejor gestion')

    datosSistema = cr.carga_datos() # carga lo que tenemos almacenado en el json
    print('datos cargados correctamente')

    usuarioConectado = usr.login(datosSistema)
    # ESCUDO: Comillas exteriores dobles para evitar SyntaxError con llaves de diccionarios
    print(f"Aceceso concedido. Bienvenido al sistema: {usuarioConectado['nombre']}")

    # Control de menú principal
    while True:
        if usuarioConectado['rol'] == 'administrador': # este menu es para el administrador
            msg.menuAdministrador() # llama la funcion estetica
            opcion = input('Seleccione una opcion: ')

            if opcion == '1':
                while True:
                    msg.sub_menu_usuarios()
                    opcionUsuario = input('Seleccione una opcion de gestion: ')
                    
                    if opcionUsuario == '1':
                        usr.registrarUsuarios(datosSistema)
                        
                    elif opcionUsuario == '2':                
                        usr.listarUsuarios(datosSistema)
                        
                    elif opcionUsuario == '3':
                        usr.eliminarUsuario(datosSistema)
                        
                    elif opcionUsuario == '4':                    
                        usr.modificarUsuario(datosSistema)
                        
                    elif opcionUsuario == '5':
                        print('\nVolviendo al menu principal.')
                        break
                    else:
                        print('\nOpcion no valida intente nuevamente.')

            elif opcion == '2':
                while True:
                    msg.sub_menu_contactos()
                    opcionContacto = input('Seleccione una opcion de contactos: ')
                    
                    if opcionContacto == '1':
                        con.registrarContacto(datosSistema)

                    elif opcionContacto == '2':
                        con.listarContactos(datosSistema)

                    elif opcionContacto == '3':
                        con.modificarContacto(datosSistema)
                        
                    elif opcionContacto == '4':
                        con.eliminarContacto(datosSistema)

                    elif opcionContacto == '5':
                        print('\nVolviendo al menu principal.')
                        break
                    else:
                        print('\nOpcion no valida intente nuevamente.')

            elif opcion == '3':
                print('\nCerrando sesion.')
                break # este break rompe el bucle del while
            
            else:
                print('\nOpcion no valida. Porfavor intente nuevamente.')

        elif usuarioConectado['rol'] == 'operario':
            msg.menuOperario()
            opcion = input('Seleccione una opcion: ')

            if opcion == '1':
                while True:
                    msg.sub_menu_contactos()
                    opcionContacto = input('Seleccione una opcion de contactos: ')
                    
                    if opcionContacto == '1':
                        con.registrarContacto(datosSistema)

                    elif opcionContacto == '2':
                        con.listarContactos(datosSistema)

                    elif opcionContacto == '3':
                        con.modificarContacto(datosSistema)

                    elif opcionContacto == '4':
                        con.eliminarContacto(datosSistema)
                        
                    elif opcionContacto == '5':
                        print('\nVolviendo al menu principal.')
                        break
                    else:
                        print('\nOpcion no valida intente nuevamente.')
                
            elif opcion == '2':
                print('\nCerrando sesion.')
                break
                
            else:
                print('\nOpcion no valida. Porfavor intete nuevamente.')