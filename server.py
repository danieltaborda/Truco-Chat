#!/usr/bin/env python
# -*- coding: utf-8 -*-

# diguito69 :       chat con nick 
# Agresta corp. :   Truco Chat
import socket
import threading
import os
import select
import funciones
import random
import time

def repartidor():#Funcion general.. reparte las cartas 
    cartas_posibles=["1 de espada", "2 de espada", "3 de espada", "4 de espada", "5 de espada", "6 de espada", "7 de espada", "10 de espada", "11 de espada", "12 de espada", "1 de copa", "2 de copa", "3 de copa", "4 de copa", "5 de copa", "6 de copa", "7 de copa", "10 de copa", "11 de copa", "12 de copa", "1 de oro", "2 de oro", "3 de oro", "4 de oro", "5 de oro", "6 de oro", "7 de oro", "10 de oro", "11 de oro", "12 de oro", "1 de basto", "2 de basto", "3 de basto", "4 de basto", "5 de basto", "6 de basto", "7 de basto", "10 de basto", "11 de basto", "12 de basto"]
    pack_1 = []
    pack_2 = []
    for i in range(3):#el truco necesita 3 cartas por jugador 
        carta_elegida = random.choice(cartas_posibles)# elegimos una carta al azar
        pack_1.append(carta_elegida)#la agregamos a la lista personal del jugador
        cartas_posibles.remove(carta_elegida)# la removemos de la lista general para que no salga de vuelta 

    for i in range(3):#Identico a los puntos anteriores, pero manejando la lista del otro jugador
        carta_elegida = random.choice(cartas_posibles)
        pack_2.append(carta_elegida)
        cartas_posibles.remove(carta_elegida)
    
    return pack_1, pack_2

def esperar(tiempo):
    time.sleep(int(tiempo))


class Server(threading.Thread):

    def __init__(self, socket_server):#el constructor DEBE recibir un objeto socket como parametro
        threading.Thread.__init__(self)
        self.socket_server = socket_server
        self._read_fd, self._write_fd = os.pipe()
        self.clientes = [self._read_fd]
        self.nick = {}
        self.cartas1=[]
        self.cartas2=[]
        self.cartaq1=[]
        self.cartaq2=[]
        self.puntaje1 = 0 
        self.puntaje2 = 0

               
    def run(self):
        salir = False
        jugador1 = False
        jugador2 = False
        pedidodejug1 = False###pedidos de puntos(una variable por jugador)
        pedidodejug2 = False###
        termjug1 = False##pedidos de terminar la ronda(una variable por jugador)
        termjug2 = False##
        comenzar_partida = False
        apedir = 0#puntaje que se pide



        while not salir:
            clientes, b, c = select.select(self.clientes, [], [])
            for cliente in clientes:
                if (cliente == self._read_fd):
                    if os.read(self._read_fd, 1) == '0':
                        salir = True
                        break

                elif pedidodejug1 == True and self.nick[cliente] == "jugador_2":
                        cliente.send("jugador_1 ha pedido " + apedir + " puntos. Aceptar ? s/n")#(revisado)
                        msj = cliente.recv(2048)
                        esperar(2)
                        if msj == "n": # -------------------sub COMANDO-----(revisado)------

                            self.enviar("server", self.nick[cliente] + " ha denegado la peticion de puntos. ")
                            pedidodejug1 = False                       
                        elif msj == "s":# -------------------sub COMANDO -----(revisado)-------
                            self.puntaje1 = self.puntaje1 + int(apedir)
                            self.enviar("server", self.nick[cliente] + " ha aceptado la peticion de puntos. ")
                            pedidodejug1 = False

                elif pedidodejug2 == True and self.nick[cliente] == "jugador_1":
                        cliente.send("jugador_2 ha pedido " + apedir + " puntos. Aceptar ? s/n")
                        msj = cliente.recv(2048)
                        esperar(2)
                        if msj == "n": # -------------------sub COMANDO----(revisado)----------------

                            self.enviar("server", self.nick[cliente] + " ha denegado la peticion de puntos. ")
                            pedidodejug2 = False                       
                        elif msj == "s":# -------------------sub COMANDO ------(revisado)--------------
                            self.puntaje2 = self.puntaje2 + int(apedir)
                            self.enviar("server", self.nick[cliente] + " ha aceptado la peticion de puntos. ")
                            pedidodejug2 = False
                        esperar(2)

                elif termjug1 == True and self.nick[cliente] == "jugador_2":
                        cliente.send("jugador_1 ha pedido terminar. Aceptar ? s/n\n")
                        msj = cliente.recv(2048)
                        esperar(2)
                        if msj == "n": # -------------------SUB COMANDO--------------------

                            self.enviar("server", self.nick[cliente] + " ha denegado la peticion de terminar. \n")
                            termjug1 = False                       
                        elif msj == "s":# -------------------SUB COMANDO --------------------

                            self.enviar("server", self.nick[cliente] + " ha aceptado la peticion de terminar. \n")
                            self.puntaje()
                            comenzar_partida = False
                            termjug1 = False

                elif termjug2 == True and self.nick[cliente] == "jugador_1":
                        cliente.send("jugador_2 ha pedido terminar. Aceptar ? s/n\n")
                        msj = cliente.recv(2048)
                        esperar(2)
                        if msj == "n": # -------------------SUB COMANDO--------------------

                            self.enviar("server", self.nick[cliente] + " ha denegado la peticion de terminar. \n")

                            termjug2 = False                       
                        elif msj == "s":# -------------------SUB COMANDO --------------------

                            self.enviar("server", self.nick[cliente] + " ha aceptado la peticion de terminar. \n")
                            self.puntaje()
                            comenzar_partida = False
                            termjug2 = False
                        esperar(2)
                        
                        
   

                else: # -----------------------Termina el caso de pedidos ------------------------

                    
                    msj = cliente.recv(2048) ## Esta linea recibe
                    if msj == "desconectar": # -------------------COMANDO 1------(revisado)--------------

                        # Un cliente se desconect�.
                        self.enviar("server", self.nick[cliente] + " se a desconectado. ")
                        cliente.close()
                        self.clientes.remove(cliente)
                        del self.nick[cliente]



                    elif msj.startswith("Server:"):# -------------------COMANDO FALSO------(revisado)------
                        cliente.send("Tu no puedes hacer eso!\n")



                    elif msj.startswith("cantar:") and comenzar_partida == True:# COMANDO2---(revisado)-----
                        self.enviar("server", self.nick[cliente] + " ha cantado " + msj[7:] + ". \n")



                    elif msj == "puntaje" and comenzar_partida == True:# --------COMANDO3--(revisado)------
                        self.puntaje()



                    elif msj == "terminar" and comenzar_partida == True:# -------COMANDO4-----------------
                        self.enviar("server", self.nick[cliente] + " ha pedido terminar la ronda. s/n\n")
                        if self.nick[cliente] == "jugador_1": 
                            termjug1 = True
                        elif self.nick[cliente] == "jugador_2":
                            termjug2 = True



                    elif msj.startswith("pedir:") and comenzar_partida == True:#COMANDO 5(revisado)
                        apedir = msj[6:]
                        self.enviar("server", self.nick[cliente] + " ha pedido " + apedir + " puntos.\n")
                        if self.nick[cliente] == "jugador_1": 
                            pedidodejug1 = True
                        elif self.nick[cliente] == "jugador_2":
                            pedidodejug2 = True



                    elif msj.startswith("tirar:") and comenzar_partida == True:# COMANDO 6(revisado)----
                        numerodecarta = msj[6]
                        usar = True

                        if self.nick[cliente] == "jugador_1":
                            for i in self.cartaq1:
                                print i
                                if numerodecarta == i:
                                    usar=False
                            if usar != False:
                        
                                carta = self.cartas1[int(numerodecarta)]
                                self.cartaq1.append(numerodecarta)
                            else:
                                carta = "(que estas haciendo?, Ya has tirado esa carta!)\n"
                        else:
                            for i in self.cartaq2:
                                print i
                                if numerodecarta == i:
                                    usar=False
                                    print numerodecarta
                                    print 'usar=false'
                            if usar != False:
                                carta = self.cartas2[int(numerodecarta)]
                                self.cartaq2.append(numerodecarta)
                            else:
                                carta = "(que estas haciendo?, Ya has tirado esa carta!)\n"
                        self.enviar("server", self.nick[cliente] + " ha tirado en la mesa el " + carta + ". \n")




                    elif msj.startswith("nick:") and comenzar_partida == False: # COMANDO 7(revisado)---
                        # Un cliente se cambia el nick.
                        nick = self.nick[cliente]
                        if msj[5:]:
                            self.nick[cliente] = msj[5:]
                        else:
                            datos_cliente = cliente.getpeername()
                            self.nick[cliente] = datos_cliente[0] + ":" + str(datos_cliente[1])
                        self.enviar("server", nick + " se a cambiado el nombre a " + self.nick[cliente])

                        if self.nick[cliente] == "jugador_1": # -----SUB COMANDO(revisado)-----
                            jugador1 = True
                            esperar(2)
                            self.enviar("server", " jugador 1 activado")
                        if self.nick[cliente] == "jugador_2": # -------SUB COMANDO(revisado)-----
                            jugador2 = True
                            esperar(2)
                            self.enviar("server", " jugador 2 activado")



                    elif msj == "decir_cartas" and comenzar_partida == True:# ----COMANDO 8(revisado)-----
                        self.decircartas()
                        


                    elif msj == "nueva_partida" and comenzar_partida == False: #COMANDO 9(revisado)--
                        if jugador1 == True and jugador2 == True:
                            comenzar_partida = True

                            self.enviar("server", " --La partida ha comenzado-- ")
                            esperar(2)
                            self.enviar("server", " Espere por favor...")
                            esperar(3)
                            self.repartir_y_decir()
                        else:
                            self.enviar("server", " Error, jugadores no definidos...(jugador_1 y jugador_2)")



                    else:
                        # Un cliente envia un mensaje.(revisado)
                        self.enviar(cliente, msj)
    


    def enviar(self, emisor, msj):
        """Env�a un mensaje a todos los clientes de la lista."""
        if emisor == "server":
            mensaje = "Server: " + msj
        elif emisor == "nada": # -------------------Mensaje "Sin Emisor"--------------------
            mensaje = msj
        else:
            mensaje =  self.nick[emisor] + " dijo: " + msj
        print mensaje
        for cliente in self.clientes:
            if cliente != self._read_fd:
                cliente.send(mensaje)

    def puntaje(self):# -------------------Dice el puntaje--------------------
        msj = "El puntaje es:\nJugador_1: " + str(self.puntaje1) + "\nJugador_2: " + str(self.puntaje2)
        mensaje = "Server: " + msj
        print mensaje
        for cliente in self.clientes:
            if cliente != self._read_fd:
                cliente.send(mensaje)
    

    def repartir_y_decir(self): # -------------------Reparte y dice las cartas--------------------
        self.cartas1, self.cartas2 = repartidor()
        for cliente in self.clientes:
            if cliente != self._read_fd:


                if self.nick[cliente] == "jugador_1":
                    cliente.send("Tus cartas son: " + str(self.cartas1))

                if self.nick[cliente] == "jugador_2":
                    cliente.send("Tus cartas son: " + str(self.cartas2))  

  
    def decircartas(self): # -------------------dice las cartas--------------------       
        for cliente in self.clientes:
            if cliente != self._read_fd:


                if self.nick[cliente] == "jugador_1":
                    cliente.send("Tus cartas son: " + str(self.cartas1))

                if self.nick[cliente] == "jugador_2":
                    cliente.send("Tus cartas son: " + str(self.cartas2))  

       
    def agregar_cliente(self, socket_cliente):
        """Agrega un cliente a la lista de clientes conectados."""
        self.clientes.append(socket_cliente)
        datos_cliente = socket_cliente.getpeername()
        self.nick[socket_cliente] = datos_cliente[0] + ":" + str(datos_cliente[1])
        os.write(self._write_fd, '1')
    
    def cerrar(self):
        """Libera el select e indica que termine el thread."""
        os.write(self._write_fd, '0')
        
                              
def main():
    socket_server = socket.socket()#creamos un objeto socket
    socket_server.bind(("", 6969))#con el objeto socket creamos un server
    socket_server.listen(1)#definimos la Cola maxima de clientes esperando para conectarse
    chat_server = Server(socket_server)#creamos un objeto server y le pasamos como parametro el objeto socket
    chat_server.start()#corremos la funcion run del objeto server( se va a ejecutar en un hilo distinto y podremos obtener nuevos clintes mientras la corremos)
    print "Server listo, esperando conexiones."
    while 1:
        try:
            socket_cliente, datos_cliente = socket_server.accept()#Aceptamos conecciones y obtenemos un objeto socket(del cliente) y la direccion 

        except KeyboardInterrupt:
            chat_server.cerrar()
            break 
        chat_server.enviar("server", datos_cliente[0] + ":" + str(datos_cliente[1]) + " se a conectado.")
        chat_server.agregar_cliente(socket_cliente)
    print "\nCerrando..."
    socket_server.close()
    
if __name__ == "__main__":
    main()
