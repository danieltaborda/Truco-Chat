#!/usr/bin/env python
# -*- coding: utf-8 -*-


import socket
import thread
from threading import Thread
import wx
import time
import pilas


pilas.iniciar(ancho = 900, alto = 600)

class ClienteP():
    '''Anteriormente class Cliente(object), adaptado para correr en otro hilo'''
    
    def __init__(self):
        '''Se piden los parametros: el host y el objeto donde se mostarán las conversaciones'''
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
        
        def enviar():                
                aponer = str(self.enviar.texto)
                hola = pilas.actores.Texto(aponer)
        self.boton_enviar.conectar(enviar)
        #self.boton_conectar.conectar(self.conectar)
                


        #def conectar(self):
                        

cliente = ClienteP()
pilas.ejecutar()
