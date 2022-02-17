<?php
#Variables para creacion de socket servidor 127.0.0.1
define('HOST_NAME',"localhost"); 
define('PORT',"10000");
#Instancia de clase socket_create
$socket = socket_create(AF_INET, SOCK_STREAM, SOL_TCP);
#opciones de socket -> level SOL_SOCKET , optmname -> SO_REUSEADDR, optvalue -> 1
socket_set_option($socket, SOL_SOCKET, SO_REUSEADDR, 1);
socket_bind($socket, 0, PORT);
socket_listen($socket);
#Arreglo con informacion de conecciones
$clientSocket = array($socket);
#bucle Infinito mantiene abierta la comunicacion
while (true) {
    $newSocket = $clientSocket;
    #Sockets observados tomados de arreglo $clientSocket
	socket_select($newSocket, $null, $null, 0, 10);
	if (in_array($socket, $newSocket)) {
		$newSocket = socket_accept($socket);
        $clientSocket[] = $newSocket;
        #lectura de datos recibidos 
        $data = socket_read($newSocket, 1024);
        #Paso de datos a cadena de texto
        $data = strval($data);
        #Apertura de archivo csv 
        $csv = fopen("export/cars.csv", 'c+') or die("Se produjo un error al abrir el documentoCSV");
        #Decodificacion de cadena de texto segun codificacion previa al envio
        $text = utf8_decode($data);
        #Formato de cadena de texto para separadores y saltos de linea del documento
        $text = str_replace("-",";",$text);
        $text = str_replace("|","\n",$text);
        #Escritura de documento Csv
        fwrite($csv, $text) or die("No se pudo escribir en el archivo CSV");
        #Cierre de documento Csv
        fclose($csv);
	}	
	}