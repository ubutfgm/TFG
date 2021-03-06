def horaSubida(m, bot):
    '''
    Este método recibe el mensaje enviado por el usuario y la información del bot que lo recoge.
    Posteriormente recibe las rutas necesarias de obtencionDatos para llegar a los archivos a consultar,
    2_condicionantes y log.cron.
    Informa de la hora a la que se subirán las persianas en la próxima ejecución de la programación y
    nos permite modificar la hora de subida de las persianas. De forma que se levantarán como pronto a
    la hora en que amanece y, como tarde a la hora que le digamos.
    
    Posteriormente implanta los nuevos datos en el programador de tareas y reinicia los servicios.

    @params m, mensaje recogido por el listener; bot, información del bot
    @return nothing
    @send envía mensaje informativo al usuario
    '''
    try:
        import os, obtencionDatos
        from telegram import ParseMode
        
        usuario = m.chat.id
        tokenBot, users, climacellKey, weatherApiKey, persianas, luces, calderas, rutaCred, rutaAuto = obtencionDatos.obtencionDatos()

        # Leemos hora antigua
        f = open(rutaAuto+"2_condicionantes")
        dataOriginal = f.read()
        f.close()
        
        f = open(rutaAuto+"log.cron")
        dataLogCron = f.read()
        f.close()

        horaAntigua = dataOriginal.split("\n")[1]
        dlc = dataLogCron.split("\n")
        lineaPersianas = dlc[6].split(" ")
        
        #Esta opción es informativa cuando no se introducen parámetros
        if len(m.text.split(" "))==1:
            bot.send_message(usuario, "Las persianas se subirán como pronto a las <b>"+str(horaAntigua[:-3]) + "</b> &#128337;",parse_mode=ParseMode.HTML)
        else:
            # Esta opción cambia la hora de subida de persianas
            data=dataOriginal.split("\n")

            # Leemos la hora introducida por parámetro
            horaNueva=str(m.text.split(" ")[1])
            
            if len(horaNueva)==5:
                volcado=str(horaNueva[0])+str(horaNueva[1])+":"+str(horaNueva[3])+str(horaNueva[4])+str(":00")
                horaNueva=volcado
                f = open(rutaAuto+"2_condicionantes", "w")
                f.write(str(data[0]) + os.linesep)
                f.write(str(horaNueva) + os.linesep)
                f.write(str(data[2]) + os.linesep)
                f.write(str(data[3]) + os.linesep)
                f.close()
                
                #Comprobamos el cambio de hora
                f = open(rutaAuto+"2_condicionantes")
                dataNuevo = f.read()
                f.close()
                
                horaNueva = dataNuevo.split("\n")[1]
                mensaje="La hora ha cambiado de <i>"+str(horaAntigua[:-3]) + "</i> a <b>"+str(horaNueva[:-3])+"</b> &#128337;"

                f = open(rutaAuto+"log.cron", "w")
                for i in range(len(dlc)):
                    if (i < 6):
                        f.write(str(dlc[i]) + os.linesep)
                    if (i == 6):
                        f.write(str(lineaPersianas[0]) + str(" ") + str(lineaPersianas[1]) + str(" ") + str(lineaPersianas[2]) + str(" ") + str(horaNueva) + os.linesep)
                    if (i > 6):
                        f.write(str(dlc[i]) + os.linesep)
                        
                os.system("python3.7 "+rutaAuto+"3_cocinado.py")
                os.system("sh " + rutaAuto+"4_reescribeCron.sh")

                #Leemos hora a cambiar
                bot.send_message(usuario, mensaje ,parse_mode=ParseMode.HTML)
            else:
                bot.send_message(usuario, "Introduce el formato correcto: HH:MM")    
    except Exception as e:
        bot.send_message(usuario, "Debes introducir una hora con formato HH:MM\n")
        print("Error: "+str(e))





