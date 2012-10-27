Truco-Chat
==========

Este juego es una versión del conocido juego de cartas "Truco", realizado en python a través del módulo pilas, el cual facilita la creación de juegos en 2 dimensiones.

La característica principal que ofrece esta opción de truco virtual es el chat. Esta implementación fue pensada para proporcionarle un mayor parecido al juego en la vida real.


Reglas - ¿Cómo se juega?
------------------------

Para aquel que no sabe cómo se juega al truco y quiere comenzar, le aconsejamos que consulte las reglas del juego en el siguiente <a href="http://es.wikipedia.org/wiki/Truco_argentino">link</a>.


Modo de uso
-----------

Sistema de puntajes
*******************

Una de las características de esta versión es el sistema de puntos, que no es llevado a cabo por el sistema, sino por los jugadores.

Cada jugador al terminar la ronda deberá reclamar sus correspondientes puntos al otro jugador, haciendo que se parezca más a la realidad.


Comandos
********

1. ``desconectar``: Este comando se usa para desconectarse del servidor.
2. ``cantar:``: Luego de este comando se escribe la proposicion (truco, envido, etc) para decirla de una manera formal.
3. ``terminar``: Hace que se termine la ronda. Cabe destacar que el otro jugador, luego de que se haya ejecutado el comando, debe escribir 'n'(para no terminar la ronda) o 's' (para terminar la ronda).
4. ``pedir:``: Luego de este comando se escribe los puntos (en numeros) que el jugador reclama. Cabe destacar que el otro jugador, luego de que se haya ejecutado el comando, debe escribir 'n'(para no entregar los puntos) o 's' (para entregar los puntos).
5. ``tirar:``: Luego de este comando se escribe el numero de carta que el jugador  usa en la 'mesa'(no podra usarla de nuevo).
6. ``nick:``: Luego de este comando se escribe el nick que el usuario quiere ponerse.
7. ``decir_cartas``: Le dice las respectivas cartas que posee a cada jugador.
8. ``nueva_partida``: Inicia una nueva ronda.


Enviar mensaje
**************

Para enviar un mensaje a otro jugador simplemente habrá que ingresar el mensaje (o comando) en el cuadro de Enviar y presionar el botón enviar.


Conectarse con el host
**********************

Deberá ingresar la direccion de intranet (de la computadora que esta corriendo el archivo server) en el cuadro de arriba y luego presionar conectar. Si todo salió bien deberia decir en el cuadro de conversación "conectado".


Acerca de...
------------

    Versión   -> 0.1
    Licencia  -> Creative commons Atribución - Compartir Igual 3.0
    Creador   -> Franco Agresta & Luciano Castillo  
    Profesión -> Estudiantes de programación del ITS Villada
    Provincia -> Córdoba
    Localidad -> Córdoba capital
    Website   -> https://github.com/franquitt/Truco-Chat


Contacto
--------

Por cualquier duda o sugerencia enviar un mail a:

    francoagresta96@hotmail.com
    lucho.castillo97@gmail.com


<a rel="license" href="http://creativecommons.org/licenses/by-sa/3.0/deed.es"><img alt="Licencia Creative Commons" style="border-width:0" src="http://i.creativecommons.org/l/by-sa/3.0/88x31.png" /></a><br /><span xmlns:dct="http://purl.org/dc/terms/" property="dct:title">Truco-chat</span> por <a xmlns:cc="http://creativecommons.org/ns#" href="https://github.com/franquitt/Truco-Chat/" property="cc:attributionName" rel="cc:attributionURL">Franco Agresta & Luciano Castillo</a> se encuentra bajo una <a rel="license" href="http://creativecommons.org/licenses/by-sa/3.0/deed.es">Licencia Creative Commons Atribución-CompartirIgual 3.0 Unported</a>.