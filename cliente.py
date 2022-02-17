import socket, sys,pickle

#Clase de Objeto
class Car:
    #Constructor
    def __init__(self,name,color,model,model_type,units):
        #propiedades
        self.name = name
        self.color = color
        self.model = model
        self.model_type = model_type
        self.units = units
        self.sheet = {}
    #Metodo de clase para retornar lista con las propiedades del objeto
    def get_items_list(self):
        return [self.name,self.color,self.model,self.model_type,self.units]

#Clase para procesamiento de campos
class Process_fields:
    #Constructor
    def __init__(self,doc):
        #Diccionario con todos los objetos
        self.objects = {'objs':[]}
        #contador de columnas
        self.count_fields = 1
        #Diccionario vacio para pbjetos temporales por iteraciones
        self.obj_intern = {}
        #Columnas de cada objeto
        self.columns = ["A","B","C","D","E"]
        #Lineas del documento a lista
        self.total_array = list(doc)
        #depuracion Lista con lineas de Documento
        print("preocesado"+str(self.total_array))
        #iteracion de cada linea del documento
        for items in self.total_array:
            #Condicional para resetear objeto temporal -obj_intern-
            if self.count_fields == 1:
                self.obj_intern = {}
            #Asignacion de item de iteracion a objeto temporal 
            self.obj_intern[self.columns[self.count_fields-1]] = items
            #Creacion de Objeto de Clase Car al pasar por las 5 columnas destinadas a cada objeto
            if self.count_fields == 5:
                name = self.obj_intern[self.columns[0]]
                color = self.obj_intern[self.columns[1]]
                model = self.obj_intern[self.columns[2]]
                model_type = self.obj_intern[self.columns[3]]
                units = '"'+self.obj_intern[self.columns[4]]+'"'
                car_temp = Car(name,color,model,model_type,units)
                self.objects['objs'].append(car_temp)
                self.count_fields = 1
            #Suma a Contador si este es menor a 5
            else:
                self.count_fields += 1
        #Depuracion de Objetos de clase
        print(str(self.objects))
    
    #metodo get que obtiene el sheet completo lista con objetos creados
    def get_sheet(self):
        return self.objects


class Proceso:
    def __init__(self):
        #lista para recibir lineas del documento
        list_text = []
        #lectura del documento
        with open("cars.txt", "r") as doc:
            lines = doc.readlines()
            #Funcion lambda para traer cada linea a una lista
            list_text = list(map(lambda line: str(line).replace("\n",""), lines))
        #Instancia de clase Process_fields para tratar los campos
        pro = Process_fields(list_text)
        #Llamada a metodo de clase get_sheet con el contenido de los objetos ya tratados
        list_objs = pro.get_sheet()
        #depuracion de lista de objetos
        #print("lista Objetos  "+str(pro.get_sheet()))

        #Cadena de texto vacia para envio de texto preparado
        prep_string = ""
        #Lista creada con funcion lambda para limpieza y formateo de texto desde diccionario se usa separadores internos 
        #Para controlar los separadores de cada objeto y los separadores por linea por aparte
        list_totals = []
        list_totals = list(map(lambda item: self.cleantext(str(item.get_items_list()),"-"), list_objs['objs']))
        #Paso a lista para prepara envio
        string_enviar = list(map(lambda item_list: str(item_list),list_totals))
        #Segunda limpieza con separadoes por linea que se transformaran en los saltos de linea en PHP
        self.string_enviar = self.cleantext(string_enviar,"|")
        #Depuracion de resultado a enviar hacia el servidor PHP
        print("_____"+str(self.string_enviar))
    

    #Metodo de clase para limpieza de texto
    def cleantext(self,text,sep):
        text2 = str(text).replace("\\",'').replace(",",sep).replace("[","").replace("]","").replace("''","").replace("'","")
        text2 = text2.replace(sep+" ",sep)
        text2 = text2.replace(" "+sep,sep)
        return text2
    #Metodo Getter para devolver la cadena de texto procesada para envio
    def get_result(self):
        return self.string_enviar


#Clase Principal para creacion de Socket y lanzamiento de proceso 
class Principal:
    #Constructor
    def __init__(self):
        #propiedades para Socket Cliente - 127.0.0.1:10000 -> Servidor.php
        self.host = ''
        self.port = ''
        self.sock = ''
        #Llamado a metodo creador de coneccion
        self.connection()
        #Llamado a metodo de proceso que controlara cada paso de ejecucion para tratameinto de cadena de texto a enviar
        self.procesar()
    
    #metodo de coneccion al servidor.php

    #Funcion decoradora 
    def conf_connection(self):
        def conf(self):
            self.host = "127.0.0.1"
            self.port = 10000
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((str(self.host), int(self.port)))
            return self.sock
        return conf
    
    #Funcion decorada
    @conf_connection
    def connection(self):
        #Depuracion de coneccion 
        print("Servicio Cliente")
        self.procesar()
    
    
    
    #metodo de proceso: instancia de Clase Proceso y envio de resultado al socket servidor
    def procesar(self):
        string_enviar = Proceso().get_result()
        self.sock.send(string_enviar.encode("ascii"))



#Punto de entrada
if __name__ == '__main__':
    #Llamado a clase Principal
    Principal()