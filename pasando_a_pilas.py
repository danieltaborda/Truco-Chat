import pilas
pilas.iniciar(ancho = 900, alto = 600)
entrada_enviar = pilas.interfaz.IngresoDeTexto(ancho=350)
entrada_enviar.y = -280
boton_enviar = pilas.interfaz.Boton("Enviar")
boton_enviar.y = -280
boton_enviar.x = 220
pilas.ejecutar()
