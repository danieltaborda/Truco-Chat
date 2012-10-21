#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket
import thread
from threading import Thread
import wx
import time
import pilas
import re
from pilas.interfaz.base_interfaz import BaseInterfaz

class Cliente(Thread):
    
    def __init__(self, destino, host):
        Thread.__init__(self)
        self.destino = destino
        self._socket = socket.socket()
        self._socket.connect((host, 6968))
        self.start()
        
    def entrada(self, dato):
        """Lee el teclado y lo envía al server."""
        print "enviando:" + dato + "\n"
        self._socket.send(str(dato))
            
    def salida(self, msj):
        antes = self.destino.texto
        print antes + "\n"
        despues = str(antes) + str(msj) + str("\n")
        print despues + "\n"
        self.destino.texto = despues
        
    def run(self):
        # hilo es para poder leer el teclado y el socket
        # al mismo tiempo, ya que los dos métodos se bloquean.
        self.salida("Conectado.")
        while 1:
            try:
                dato = self._socket.recv(2048) ## Esta linea
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


class CuadroConversacion(BaseInterfaz):

    def __init__(self, texto_inicial="", x=0, y=0, ancho=350, limite_de_caracteres=80, icono=None):
        BaseInterfaz.__init__(self, x=x, y=y)
        self.texto = texto_inicial
        self.cursor = ""
        self.imagen_caja = pilas.imagenes.cargar('/home/franco/Escritorio/cuadro.svg')#"interfaz/caja.png")#'/home/franco/Escritorio/cuadro.svg')
        alto = self.imagen_caja.alto()
        self._cargar_lienzo(ancho, alto)

        if icono:
            self.icono = pilas.imagenes.cargar(icono)
        else:
            self.icono = None


        self.centro = ("centro", "centro")

        self._actualizar_imagen()
        self.limite_de_caracteres = limite_de_caracteres
        self.cualquier_caracter()

        self.escena.suelta_tecla.conectar(self.cuando_pulsa_una_tecla)
        pilas.mundo.agregar_tarea_siempre(0.40, self._actualizar_cursor)
        self.fijo = True

    def _actualizar_cursor(self):


        self._actualizar_imagen()
        return True

    def cualquier_caracter(self):
        self.caracteres_permitidos = re.compile(".*")

    def solo_numeros(self):
        self.caracteres_permitidos = re.compile("\d+")

    def solo_letras(self):
        self.caracteres_permitidos = re.compile("[a-z]+")

    def cuando_pulsa_una_tecla(self, evento):
        self.activo = False
        if self.tiene_el_foco and self.activo:

            if evento.codigo == '\x08' or evento.texto == '\x08':
                # Indica que se quiere borrar un caracter
                self.texto = self.texto[:-1]

            else:
                if len(self.texto) < self.limite_de_caracteres:
                    nuevo_texto = self.texto + evento.texto

                    if (self.caracteres_permitidos.match(evento.texto)):
                        self.texto = self.texto + evento.texto
                    else:
                        print "Rechazando el ingreso del caracter:", evento.texto
                else:
                    print "Rechazando caracter por llegar al limite."

            self._actualizar_imagen()

    def _cargar_lienzo(self, ancho, alto):
        self.imagen = pilas.imagenes.cargar_superficie(ancho, alto)

    def _actualizar_imagen(self):
        ancho = self.imagen_caja.ancho()
        alto = self.imagen_caja.alto()
        self.imagen.pintar_parte_de_imagen(self.imagen_caja, 0, 0, 40, ancho, 0, 0)

        if self.icono:
            dx = 20
            self.imagen.pintar_parte_de_imagen(self.icono, 0, 0, 40, ancho, 7, 7)
        else:
            dx = 0

        for x in range(40, self.imagen.ancho() - 40):
            self.imagen.pintar_parte_de_imagen(self.imagen_caja, ancho - 40, 0, 40, alto, x, 0)

        self.imagen.texto(self.texto + self.cursor, 15 + dx, 20)




pilas.iniciar(ancho = 900, alto = 600)



class ClienteP():#anteriormente class Cliente(object), adaptado para correr en otro hilo
    def __init__(self):
        self.enviar = pilas.interfaz.IngresoDeTexto(ancho=350, limite_de_caracteres=48)
        self.enviar.y = -280
        self.boton_enviar = pilas.interfaz.Boton("Enviar")
        self.boton_enviar.y = -280
        self.boton_enviar.x = 220
        self.conectar = pilas.interfaz.IngresoDeTexto(ancho=350, limite_de_caracteres=48)
        self.conectar.y = 280
        self.boton_conectar = pilas.interfaz.Boton("Conectar")
        self.boton_conectar.y = 280
        self.boton_conectar.x = 220
        self.cuadro_conversacion = CuadroConversacion()
        self.cuadro_conversacion.x = 260

        self.cuadro_conversacion.texto = "Bienvenido a Truco Chat\n"


        def conectar():
            coneccion = self.conectar.texto
            self.cliente = Cliente(self.cuadro_conversacion, coneccion)
        def enviar_dato():
            self.cliente.entrada(self.enviar.texto)
            self.enviar.texto = " "
        self.boton_conectar.conectar(conectar)
        self.boton_enviar.conectar(enviar_dato)
                


        #def conectar(self):
                        

cliente = ClienteP()
pilas.ejecutar()