# -*- coding: utf-8 -*-
#
#

import socket
from threading import Thread
import pilas


class Cliente(Thread):
    
    def __init__(self, destino):
        Thread.__init__(self)
        self.destino = destino
        self._socket = socket.socket()
        self._socket.connect(('localhost', 6969))
        self.start()        
        
    def entrada(self, dato):
        """Lee el teclado y lo envía al server."""

        self._socket.send(str(dato.texto))
            
    def salida(self, msj):
        self.destino.definir_texto(self.destino.obtener_texto() + msj + '\n')
        
    def run(self):
        # hilo es para poder leer el teclado y el socket
        # al mismo tiempo, ya que los dos métodos se bloquean.
        self.salida("Conectado.")
        while 1:
            try:
                dato = self._socket.recv(1024) ## Esta linea
            except:
                break 
            # Si dato es una cadena vacía seguro es porque el
            # server se desconectó, entonces termina el bucle.
            # (Porque se produciría un bucle infinito).
            if dato == "":
                self.salida("El server se ha desconectado.")
                break
            self.salida(dato)
            
        self.salida("Cerrando...")
        self._socket.close()
        self.salida("Cerrado.")



pilas.iniciar(ancho = 900, alto = 600)


class Escena:

    def __init__(self):
        self.txtbHost = pilas.interfaz.IngresoDeTexto(y=280, limite_de_caracteres=48)
        self.btnEnviar = pilas.interfaz.Boton(texto='Enviar', x=220, y=-280)
        self.txtbChat = pilas.interfaz.IngresoDeTexto(y=-280, limite_de_caracteres=48)
        self.txtChat = pilas.actores.Texto(texto=u'Esperando conexión ...\n', magnitud=15)
        self.btnConectar = pilas.interfaz.Boton(texto='Conectar', x=220, y=280)
        def conectar():
            self.cliente = Cliente(self.txtChat)
        def enviar_dato():
            self.cliente.entrada(self.txtbChat)
            
        self.btnConectar.conectar(conectar)
        self.btnEnviar.conectar(enviar_dato)

Escena()

pilas.ejecutar()



