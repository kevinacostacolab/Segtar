
def main():

  import functions
  from google.colab import files
  import csv

  ##Proceso que elimina los clientes fallecidos y arma un archivo con los casos mencionados
  ##El archivo se llama Fallecidos.csv

  #Abro el archivo de los seguros de tarjeta
  fichero = open('/content/SEGTARJ_1_20241010.txt')
  fichero_lineas = fichero.readlines()

  #Establezco el nombre del archivo de los fallecidos
  nombre_archivo_fallecidos = 'Fallecidos'
  nombre_archivo_segtar = 'SEGTARJ'
  nombre_archivo_excepciones = 'Excepciones'

  #Variables
  documento_cuit = ''
  validacion_cuit = False
  nueva_cadena = ''
  primera_ejecucion = True


  #listas para crear archivos:
  datos_fallecidos = []
  datos_excepcionales = []
  datos_no_excepcionales=[]

  #Obtengo los numeros de cliente fallecidos
  cuentas_fallecidos = functions.cargar_cuentas_csv('/content/Fallecidos_TC.csv')

  #lambdas
  casos_cuit = lambda x: x != 0 and x < 30000000000


  ########  Recorro todas las lineas del archivo ##############

  for linea in fichero_lineas:

    if primera_ejecucion:
      datos_excepcionales.append(linea)
      datos_no_excepcionales.append(linea)
      primera_ejecucion = False
    else:

      #Toma datos de identificacion de clientes y concateno para cruzar con fallecidos
      vdo_codigo = functions.extraer_por_ocurrencia(linea,'@','@',12)
      documento = functions.extraer_por_ocurrencia(linea,'@','@',13)
      cod_identificacion = vdo_codigo + '-' + documento

      #Busca si el cliente esta en la lista de fallecidos
      if  functions.verificar_valor(cuentas_fallecidos,cod_identificacion):
        #Agrego linea del txt a la lista de fallecidos
        datos_fallecidos.append(linea)
      else:

        #Dni y Cuit de los clientes
        cuit=functions.extraer_por_ocurrencia(linea,'@','@',11)

        #Defino la variable documento si es nulo para que el siguiente if
        if len(documento) < 3:
          documento = '99999999'

        #Verifico que el cuit contenga al documento con lambda
        if casos_cuit(int(cuit)):

          if cuit.find(documento) != -1:

            datos_no_excepcionales.append(linea)

          else:
            #extraigo el documento que tengo dentro del cuit
            documento_cuit = cuit[2:len(cuit)-1]
            #reemplazo el documento del archivo por el documento del cuit
            nueva_cadena = functions.reemplazar_dato(linea,'@','@',13,documento_cuit)
            #Agrego los datos de la linea al array
            datos_excepcionales.append(linea)
            datos_no_excepcionales.append(nueva_cadena)
        else:
          datos_excepcionales.append(linea)


  #Creo el csv de los fallecidos
  functions.creacion_csv(nombre_archivo_fallecidos,datos_fallecidos)
  #Creo el txt de los casos no excepcionales
  functions.creacion_txt(nombre_archivo_segtar,datos_no_excepcionales)
  #Creo el txt de los casos excepcinoales
  functions.creacion_txt(nombre_archivo_excepciones,datos_excepcionales)


  files.download(f'/content/{nombre_archivo_segtar}.txt')
  files.download(f'/content/{nombre_archivo_excepciones}.txt')
  files.download(f'/content/{nombre_archivo_fallecidos}.csv')

