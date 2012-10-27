#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Franco Agresta & Luciano Castillo
#

import sys
import re
import time
import socket
import trhead
import trheading
import pilas
from PyQt4 import QtGui, QtCore, Qt
from threading import Thread
from pilas.interfaz.base_interfaz import BaseInterfaz


class Cliente(Thread):
    
    def __init__(self, destino, host):
        Thread.__init__(self)
        self.destino = destino
        self.var = -50
        self._socket = socket.socket()
        self._socket.connect((host, 6969))
        self.start()
        print "inicio el thread"
        
    def entrada(self, dato):
        """Lee el teclado y lo envía al server."""
        self._socket.send(str(dato))
            
    def salida(self, msj):
        antes = self.destino.toPlainText()
        ahora = antes + str(msj) + "\n"
        self.destino.setPlainText(str(ahora))
        
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
            if dato[:16] == 'Tus cartas son: ':
                for i in range(len(carta)):
                    carta[i].x = [310]
                    atras[i].x = [310]
                
                data=list(dato[16:])
                dat = ''
                for i in range(len(data)):
                    if data[i] != '[' and data[i] != ']' and data[i] != "'" and data[i] != '"' and data[i] != ' ':
                        dat += data[i]
                ac = ''
                acu = []
                for i in dat:
                    if i != ',':
                        ac += i
                    else:
                        acu.append(ac)
                        ac = ''
                acu.append(ac)
                ghj = -250
                for i in range(len(acu)):
                    try:
                        a=int(acu[i][1])
                        carta[i].imagen = 'cartas/' + acu[i][:2] + '/' + acu[i][4:] + '.jpg'
                    except:
                        carta[i].imagen = 'cartas/' + acu[i][0] + '/' + acu[i][3:] + '.jpg'
                    carta[i].x, atras[i].x = [ghj], [ghj]
                    carta[i].y, atras[i].y = [-150], [150]
                    carta[i].rotacion, atras[i].rotacion = [360], [360]
                    ghj += 130
            if 'Server: jugador_2 ha tirado en la mesa el ' in dato:
                carta[0].y = [self.var]
                carta[0].x = [ghj-260]
                carta[0].escala = 0.25
                self.var -= 10
            self.salida(dato)
            
        self.salida("Cerrando...")
        self._socket.close()
        self.salida("Cerrado.")
        
        
class Ventana(QtGui.QMainWindow):

    def __init__(self, canvas):
        QtGui.QMainWindow.__init__(self)
        self.setWindowTitle("Truco")
        self.canvas = canvas
        self.resize(930, 500)
        self.move(0, 0)

        self.cwidget = QtGui.QWidget(self)
        self.layout = QtGui.QHBoxLayout()

        self.cwidget.setLayout(self.layout)
        self.setCentralWidget(self.cwidget)

        self.layout.addWidget(self.canvas, 1)

        # Creando el panel lateral
        self.layout_panel = QtGui.QVBoxLayout()
        self.layout.addLayout(self.layout_panel)
        
        self.statusBar()
        self.setFocus()
        
        salir = QtGui.QAction('Salir', self)
        salir.setShortcut('Alt+F4')
        salir.setStatusTip('Cerrar aplicacion')
        
        modo_de_uso = QtGui.QAction('Manual', self)
        modo_de_uso.setShortcut('F1')
        modo_de_uso.setStatusTip('Modo de uso')
        
        comandos = QtGui.QAction('Comandos', self)
        comandos.setShortcut('F2')
        comandos.setStatusTip('Comandos del truco')
        
        acerca = QtGui.QAction('Acerca de', self)
        acerca.setShortcut('F3')
        acerca.setStatusTip('Acerca de ...')
        
        menu = self.menuBar()
        archivo = menu.addMenu('&Archivo')
        archivo.addAction(salir)
        ayuda = menu.addMenu('A&yuda')
        ayuda.addAction(modo_de_uso)
        ayuda.addAction(comandos)
        ayuda.addAction(acerca)
        
        self.connect(salir, QtCore.SIGNAL('triggered()'), QtGui.qApp, QtCore.SLOT('quit()'))

        self.CampoConectar = QtGui.QLineEdit()
        self.CampoConectar.setText("Host..")
        self.layout_panel.addWidget(self.CampoConectar)
        
        self.BotonConectar = QtGui.QPushButton("Conectar")
        self.BotonConectar.setStatusTip('Conectar al servidor')
        self.layout_panel.addWidget(self.BotonConectar)
        
        self.CampoEnviar = QtGui.QLineEdit()
        self.CampoEnviar.setText("Mensaje")
        self.layout_panel.addWidget(self.CampoEnviar)
        
        self.BotonEnviar = QtGui.QPushButton("Enviar")
        self.BotonEnviar.setStatusTip('Enviar mensaje')
        self.layout_panel.addWidget(self.BotonEnviar)

        self.lista = QtGui.QPlainTextEdit()
        self.layout_panel.addWidget(self.lista)
        self.lista.setReadOnly(True)

        # Creando el primer mensaje

        self.lista.setPlainText("Bienvenido a Truco-Chat\n")
        print self.lista.toPlainText()

        #Funciones*-*-*-*
def Conectar():
    host =  ventana.CampoConectar.text()
    ventana.cliente = Cliente(ventana.lista, host)
def Enviar():
    mensaje =  ventana.CampoEnviar.text()
    ventana.cliente.entrada(str(mensaje))
    ventana.CampoEnviar.setText("")


app = QtGui.QApplication(sys.argv[1:])

pilas.iniciar(usar_motor="qtsugar")

carta, atras = [pilas.actores.Actor('cartas/atras/carta.png', x=200), pilas.actores.Actor('cartas/atras/carta.png', x=200), pilas.actores.Actor('cartas/atras/carta.png', x=200)], [pilas.actores.Actor('cartas/atras/carta.png', x=200), pilas.actores.Actor('cartas/atras/carta.png', x=200), pilas.actores.Actor('cartas/atras/carta.png', x=200)]
for i in range(len(carta)):
    carta[i].escala, atras[i].escala = 0.5, 0.5

anvas = pilas.mundo.motor.canvas
ventana = Ventana(canvas)

app.connect(ventana.BotonConectar, Qt.SIGNAL("clicked()"), Conectar)
app.connect(ventana.BotonEnviar, Qt.SIGNAL("clicked()"), Enviar)
ventana.show()
sys.exit(app.exec_())


