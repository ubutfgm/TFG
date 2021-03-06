def generador(m, bot):
    '''
    Este método recibe el mensaje enviado por el usuario y la información del bot que lo recoge.
    Posteriormente recibe las rutas necesarias de obtencionDatos para llegar a los archivos que obtienen
    la información de las APIs externas. Éstos se lanzan desde el script <<lanzaTodoElProceso.sh>>

    @params m, mensaje recogido por el listener; bot, información del bot
    @return nothing
    @send envía mensaje informativo al usuario
    '''
    try:
        import os, obtencionDatos
        #from telegram import ParseMode
        
        usuario = m.chat.id
        tokenBot, users, climacellKey, weatherApiKey, persianas, luces, calderas, rutaCred, rutaAuto = obtencionDatos.obtencionDatos()
        
        import os, obtencionDatos        
        os.system("bash " + rutaAuto+"LanzaTodoElProceso.sh")

        #Leemos información del archivo        
        f = open(rutaAuto+"log.cron", "r")
        data = f.read()
        f.close()
    
        #Obtenemos la primera línea aunque se puede cambiar a la segunda...
        matrix1 = data.split('\n')
        bot.send_message(usuario, "Datos obtenidos el "+matrix1[0]+" a las "+matrix1[1].split(' ')[3] + " ya implantados.")
    except Exception as e:
        bot.send_message(usuario, "Error en módulo de obtención de datos: " + str(e) + str(rutaAuto))


