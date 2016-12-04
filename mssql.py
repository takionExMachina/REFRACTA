import pymssql

def queryPerson(imagen):

    conn = pymssql.connect('localhost','sa','@lF4bR@v0#123','REFRACTA')

    cursor = conn.cursor()

    cursor.execute('SELECT rut,primer_nombre,segundo_nombre,apellido_paterno,apellido_materno,'
                   'descripcion,fecha_registro,fecha_caducidad,recinto,direccion,comuna,provincia,'
                   'region FROM persona INNER JOIN imagenes ON persona.id_imagen = imagenes.id_imagen'
                   ' INNER JOIN historial ON persona.id_historial = historial.id_historial INNER JOIN '
                   'recinto on historial.id_recinto = recinto.id_recinto INNER JOIN locacion ON '
                   'recinto.id_locacion = locacion.id_locacion INNER JOIN comuna ON locacion.id_comuna = '
                   'comuna.id_comuna INNER JOIN provincia ON comuna.id_provincia = provincia.id_provincia '
                   'INNER JOIN region ON provincia.id_region = region.id_region WHERE imagenes.id_imagen = %d' % (imagen))

    result = cursor.fetchone()

    message = ''

    while result:
        message += 'rut: %s nombres: %s %s apellidos: %s %s descripcion: %s fecha: %s caduca: ' \
              '%s recinto: %s direccion: %s comuna: %s provincia: %s region: %s \n' % \
              (result[0], result[1],result[2],result[3],result[4],result[5],result[6],result[7],
               result[8],result[9],result[10],result[11],result[12] )

        result = cursor.fetchone()


    return message

def imageId(image):
    conn = pymssql.connect('localhost', 'sa', '@lF4bR@v0#123', 'REFRACTA')

    cursor = conn.cursor()

    cursor.execute('SELECT * FROM imagenes WHERE imagen LIKE ' + '\'%' + image + '%\'')

    result = cursor.fetchone()

    if result is not None:
        message = result[0]

        return message
    else:
        return 0
