import cv2
import face_recognition as fr
import os
import numpy
from datetime import datetime

#Crear Base de datos

ruta= 'Empleados'
mis_imagenes = []
nombres_empleados = []
lista_empleados = os.listdir(ruta)

for nombre in lista_empleados:
    imagen_actual = cv2.imread(f'{ruta}/{nombre}')
    mis_imagenes.append(imagen_actual)
    nombres_empleados.append(os.path.splitext(nombre)[0])

#codificar imagenes

def codificar(imagenes):

    #crear una lista nueva

    lista_codificada= []

    #pasar imagenes a rgb

    for imagen in imagenes:
        imagen = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)
        
        #codificar

        codificado = fr.face_encodings(imagen)[0]

        #agregar a la lista

        lista_codificada.append(codificado)

        # devolver lista conficidad

    return lista_codificada

#registros de ingresos

def registro_asistencia(persona):

    f = open("registro.csv", "r+")
    lista_datos = f.readlines()
    nombres_registro= []
    for linea in lista_datos:
        ingreso = linea.split(',')
        nombres_registro.append(ingreso[0])

        if persona not in nombres_registro:
            ahora= datetime.now()
            string_ahora= ahora.strftime('%H:%M:%S')
            f.writelines(f'\n{persona}, {string_ahora} ')



lista_codificada = codificar(mis_imagenes)  

#toma imagenes de camara web

captura = cv2.VideoCapture(0,cv2.CAP_DSHOW)

#leer imagen de la camara

exito, imagen = captura.read()
if not exito:
    print("no se pudo tomar la captura")

else:
    #reconocer la cara en la captura
    cara_captura= fr.face_locations(imagen)

    #codfiicar la captura
    cara_captura_codificada= fr.face_encodings(imagen, cara_captura)

    #buscar coincidencia

    for caracodif, caraubic in zip (cara_captura_codificada, cara_captura):

        coincidencias = fr.compare_faces(lista_codificada, caracodif)
        distancia = fr.face_distance(lista_codificada,caracodif)
        
        indice_coincidencia= numpy.argmin(distancia)

        #mostrar coincidencias
        if distancia[indice_coincidencia] > 0.6:
            print("Usted no trabaja en este lugar")

        else:
            #buscar el nombre del empleado
            nombre= nombres_empleados[indice_coincidencia]

            #mostrar en pantalla imagen, cuadro y nombre con recuadro
            y1,x1,y2,x2 = caraubic

            cv2.rectangle(imagen,(x1,y1),(x2,y2)(0,250,0), 2)        
            cv2.rectangle(imagen,(x1,y2 - 35), (x2,y2),(0,250,0),cv2.FILLED)
            cv2.putText(imagen, nombre, (x1 + 6, y2 -6), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 2 )
           
            registro_asistencia(nombre)

            #mostrar imagenes
            cv2.imshow('imagen web', imagen)
            
            #mantener abierta la ventana
            cv2.waitKey(0)

            
           

    
