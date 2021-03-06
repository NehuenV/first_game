import pygame
from pygame.locals import *
import os
import sys
from librerias import ImagenDinamica


pygame.init()
#ventana
ANCHO = 1366
ALTO = 768
ventana = pygame.display.set_mode((ANCHO, ALTO), pygame.FULLSCREEN)
pygame.display.set_caption("Battle Front")

#colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
ORANGE = (241, 163, 64)

#jugadores
velocidadJugador = 8
velocidadBola = 10
jugador1 = ImagenDinamica.ImagenDinamica("Imagenes/jugador1.png",ventana, velocidadJugador)  # ruta, display, velocidad de movimiento
jugador2 = ImagenDinamica.ImagenDinamica("Imagenes/jugador2.png",ventana, velocidadJugador)
bola = ImagenDinamica.ImagenDinamica("Imagenes/bolaBillar.png", ventana, velocidadBola)
fondo = pygame.image.load("Imagenes/fondo.jpg")

jugador1.cambiarTamañoImg(71,150)
jugador2.cambiarTamañoImg(71,150)
bola.cambiarTamañoImg(64,64)


jugador1.setTopes(80, (ANCHO//2)-jugador1.getPixels()[0], 133, ALTO-jugador1.getPixels()[1]-60)  # defino los limites a los que se puede mover la imagen
jugador2.setTopes((ANCHO//2), ANCHO-jugador2.getPixels()[0]-80, 133, ALTO-jugador2.getPixels()[1]-60)
bola.setTopes(83, ANCHO-bola.getPixels()[0]-83, 135, ALTO-bola.getPixels()[1]-60)

#SECCION VIDAS:
#creo 12 objetos o imagenes de vidas
LstVidas = []
for i in range(12):
	LstVidas.append(pygame.image.load("Imagenes/vida.png"))

#Obtengo los rectangulos de cada imagen de la vida, esto me sirve para las colisiones
LstRectVidas = []
x = 0
for img in LstVidas:
	LstRectVidas.append(LstVidas[x].get_rect())
	x += 1

#POSVIDAS ME SIRVE PARA ALINEAR LAS VIDAS EN LA PANTALLA
pixelsVida = 50
cantVidas = 6
espacioBlanco = (ALTO - (pixelsVida*cantVidas)) // (cantVidas+1)
POSVIDAS = (espacioBlanco,
			(espacioBlanco*2)+pixelsVida,
			(espacioBlanco*3)+(pixelsVida*2),
			(espacioBlanco*4)+(pixelsVida*3),
			(espacioBlanco*5)+(pixelsVida*4),
			(espacioBlanco*6)+(pixelsVida*5))

#CREO UNA LISTA PARA GUARDAR EL RECTANGULO DE CADA IMG DE LA VIDA 
for x in range(cantVidas):
	LstRectVidas[x].left, LstRectVidas[x].top = -6, POSVIDAS[x]
i = cantVidas

#LO MISMO PERO CON LOS QUE FALTAN
for x in range(cantVidas):
	LstRectVidas[i].left, LstRectVidas[i].top = ANCHO-43, POSVIDAS[x]
	i += 1

FuenteArial = pygame.font.SysFont("Arial", 56)
FuenteArial2 = pygame.font.SysFont("Arial", 40)

aux = 1; score1 = 0; score2 = 0 
#bucle de fin de partida
while True:
	musicGame = pygame.mixer.Sound("Music/musicGame.wav")
	musicGame.play()

	#POSICIONO A LOS JUGADORES Y LA BOLA 
	jugador1.setPos(83, (ALTO//2)-(jugador1.getPixels()[0]//2))
	jugador2.setPos(ANCHO-jugador2.getPixels()[0]-83, (ALTO-jugador2.getPixels()[0])//2)	
	bola.setPos((ANCHO//2)-(bola.getPixels()[0]//2), (ALTO//2)-(bola.getPixels()[1]//2))
	
	#POSICIONO LOS RECTANGULOS DE LOS JUGADORES Y LA BOLA
	bola.getRectangulo().left, bola.getRectangulo().top = bola.getPos()
	jugador1.getRectangulo().left, jugador1.getRectangulo().top = jugador1.getPos()
	jugador2.getRectangulo().left, jugador2.getRectangulo().top = jugador2.getPos()

	#ME SIVE PARA VERIFICAR SI LAS VIDAS SIGUEN EN JUEGO O NO
	vidasOn = [True, True, True, True, True, True, True, True, True, True, True, True]

	#otros

	clock = pygame.time.Clock()

	#Otras variables
	tope = True
	listTeclas = []
	diccionario = [K_w, K_s, K_a, K_d, K_UP, K_DOWN, K_LEFT, K_RIGHT, K_ESCAPE]
	inicializar = True
	direccionHorizontal = 'derecha'
	direccionVertical = 'subir'
	#Variables para medir tiempo
	maxTime = 91; 
	initialTime = 88
	#Score
	textoScore = FuenteArial2.render("Score", 0, (200, 60, 8))  # guardo el tiempo en un texto arial

	#game loop
	vivo1 = True; vivo2 = True
	while vivo1 and vivo2:

		clock.tick(60)  # declaro 60fps

		#Mido el Tiempo
		Time = int(pygame.time.get_ticks()/1000)  # mido el tiempo
		if aux == Time:
			aux += 1  # Uso un aux para que cada ves que pasa un segundo pueda saberlo
			maxTime -= 1  # y por cada segundo voy decrementando el tiempo maximo asignado
		textoTime = FuenteArial.render(str(maxTime), 0, (200, 60, 8))  # guardo el tiempo en un texto arial
		
		#Verifico si hay eventos(QUIT, apretar y soltar teclas) y hago algo
		for evento in pygame.event.get():  # Hay un evento?
			print(evento)
			if evento.type == QUIT:  # El evento es QUIT?
				pygame.quit()  
				sys.exit()
				
			elif (evento.type == KEYUP and len(listTeclas)>0):  # El evento es KEYUP? y hay algo en la lista? 
					if(evento.key in listTeclas):
						listTeclas.remove(evento.key)  # como deje de apretar la tecla, la quito de la lista de teclas apretadas
			
			elif evento.type == KEYDOWN:  # El evento es KEYDOWN?
				if ((evento.key in diccionario) and ((evento.key in listTeclas) == False)):
					listTeclas.append(evento.key)  # si la tecla no estaba en la lista, la agrego
					
		#Mover jugadores
		w, a, s, d, arriba, abajo, izquierda, derecha = False, False, False, False, False, False, False, False
		cont1, cont2 = 0, 0
		bloqueado1, bloqueado2 = False, False
		#verifico cuantas teclas y cuales teclas hay en la lista pulsadas por cada jugador
		for elemento in listTeclas:
			if(elemento == K_ESCAPE): pygame.quit() ;sys.exit()
			elif elemento == K_w: w = True; cont1+=1  # aumento el contador de teclas apretadas del jugador 1
			elif elemento == K_s: s = True; cont1+=1
			elif elemento == K_a: a = True; cont1+=1
			elif elemento == K_d: d = True; cont1+=1
			elif elemento == K_LEFT: izquierda = True; cont2+=1
			elif elemento == K_RIGHT: derecha = True; cont2+=1
			elif elemento == K_UP: arriba = True; cont2+=1
			elif elemento == K_DOWN: abajo = True; cont2+=1
		
		#si el jugador 1 apreto 3 o menos teclas quiere decir que se podra mover, sino no
		if cont1<=3:
			if(w and s):  # si apreto arriba y abajo tengo que decidir a donde moverme:
				for elemento in listTeclas:  # busco en la lista el elemento mas viejo y le doy preferencia al nuevo
			 		if elemento == K_w:
			 			# lo muevo al lado contrario, ya que el primer elemento de la lista es el mas viejo apretado
			 			# y yo necesito que el elemento mas nuevo tenga preferencia sobre el viejo
			 			jugador1.moverAbajo()
			 			break
			 		if elemento == K_s:
			 			jugador1.moverArriba()
			 			break
			if(a and d):  # si apreto izquierda y derecha tengo que decidir a donde moverme:
				for elemento in listTeclas:
			 		if elemento == K_a:
			 			# lo muevo al lado contrario, ya que el primer elemento de la lista es el mas viejo apretado
			 			# y yo necesito que el elemento mas nuevo tenga preferencia sobre el viejo
			 			jugador1.moverDer()
			 			break
			 		if elemento == K_d:
			 			jugador1.moverIzq()
			 			break
			if(d): jugador1.moverDer()
			if(s): jugador1.moverAbajo()
			if(a): jugador1.moverIzq()
			if(w): jugador1.moverArriba()

		#si el jugador 2 apreto 3 o menos teclas quiere decir que se podra mover, sino no
		if cont2<=3:
			if(arriba and abajo): 
				for elemento in listTeclas:
			 		if elemento == K_UP:
						# lo muevo al lado contrario, ya que el primer elemento de la lista es el mas viejo apretado
			 			# y yo necesito que el elemento mas nuevo tenga preferencia sobre el viejo
			 			jugador2.moverAbajo()
			 			break
			 		if elemento == K_DOWN:
			 			jugador2.moverArriba()
			 			break

			if(izquierda and derecha):
				for elemento in listTeclas:
			 		if elemento == K_RIGHT:
			 			# lo muevo al lado contrario, ya que el primer elemento de la lista es el mas viejo apretado
			 			# y yo necesito que el elemento mas nuevo tenga preferencia sobre el viejo
			 			jugador2.moverIzq()
			 			break
			 		if elemento == K_LEFT:
			 			jugador2.moverDer()
			 			break
			if(derecha): jugador2.moverDer()
			if(abajo): jugador2.moverAbajo()
			if(izquierda): jugador2.moverIzq()
			if(arriba): jugador2.moverArriba()

		#Dibujo la bola y los jugadores y los rectangulos de colision
		
			if maxTime>= initialTime:
				#seguira al jugador hasta que el tiempo sea 87
				bola.setPosX(jugador1.getPosX()+jugador1.getPixels()[0])
				bola.setPosY(jugador1.getPosY()+jugador1.getPixels()[1]//4)
			
		#determino si choco la bola con el jugador 1, si choco, en la zona delantera del jugador
		#entonces se movera en diagonal hacia su derecha, si choco en la zona trasera, 
		#se movera en diagonal hacia su izquierda

		if(bola.getRectangulo().colliderect(jugador1.getRectangulo())):
			
			if (bola.getPosX() >= (jugador1.getPosX()+(jugador1.getPixels()[0]//2))):
				direccionHorizontal = 'derecha'

				if(((bola.getPosY()+(bola.getPixels()[1] // 2)) <= (jugador1.getPosY()+(jugador1.getPixels()[1]//2)))
				and (bola.getPosY()+bola.getPixels()[1]) >= jugador1.getPosY()):
					direccionVertical = 'subir'
				else:
					direccionVertical = 'bajar'
			else:
				direccionHorizontal = 'izquierda'
				if ((bola.getPosY()+bola.getPixels()[1]//2) <= (jugador1.getPosY()+(jugador1.getPixels()[1]//2))):
					direccionVertical = 'subir'
				else:
					direccionVertical = 'bajar'

		#determino si choco la bola con el jugador 2, si choco, en la zona delantera del jugador
		#entonces se movera en diagonal hacia su izquierda, si choco en la zona trasera, 
		#se movera en diagonal hacia su derecha
		if(bola.getRectangulo().colliderect(jugador2.getRectangulo())):
			
			if (bola.getPosX()+bola.getPixels()[0] >= jugador2.getPosX()
			and bola.getPosX()+bola.getPixels()[0] <= jugador2.getPosX()+(jugador2.getPixels()[0]//2)):

				direccionHorizontal = 'izquierda'
				if(((bola.getPosY()+(bola.getPixels()[1] // 2)) <= (jugador2.getPosY()+(jugador2.getPixels()[1]//2)))
				and (bola.getPosY()+bola.getPixels()[1]) >= jugador2.getPosY()):
					direccionVertical = 'subir'
				else:
					direccionVertical = 'bajar'
			else:
				direccionHorizontal = 'derecha'
				if(((bola.getPosY()+(bola.getPixels()[1] // 2)) <= (jugador2.getPosY()+(jugador2.getPixels()[1]//2)))
				and (bola.getPosY()+bola.getPixels()[1]) >= jugador2.getPosY()):
					direccionVertical = 'subir'
				else:
					direccionVertical = 'bajar'
		
		if bola.getPosY() <= bola.getTopeSuperior():
			direccionVertical = 'bajar'
			
		if bola.getPosY() >= bola.getTopeInferior():
			direccionVertical = 'subir'

		if bola.getPosX()>= bola.getTopeDerecho():
			direccionHorizontal = 'izquierda'

		if bola.getPosX() <= bola.getTopeIzquierdo():
			direccionHorizontal = 'derecha'

		if direccionHorizontal == 'derecha' and direccionVertical == 'bajar':
			bola.moverInfDerecho()
		elif direccionHorizontal == 'derecha' and direccionVertical == 'subir':
			bola.moverSupDerecho()
		elif direccionHorizontal == 'izquierda' and direccionVertical == 'bajar':
			bola.moverInfIzquierdo()
		elif direccionHorizontal == 'izquierda' and direccionVertical == 'subir':
			bola.moverSupIzquierdo()
		

		#Dibujo el fondo
		ventana.blit(fondo, (0,0))  # Dibujo el fondo

		#Verifico si hubo colisiones en alguna vida
		# y pongo la posicion de la vida en False si es que hubo alguna colision
		for x in range(cantVidas*2):
			if(LstRectVidas[x].colliderect(bola.getRectangulo()) == True):
				vidasOn[x] = False

		cont1 = 0; cont2 = 0; x = 0 ; i = cantVidas
		for x in range(cantVidas*2):
			if x <= cantVidas-1 and vidasOn[x] == False:
				cont1 += 1
			if x > cantVidas-1 and vidasOn[x] == False:
				cont2 += 1

		#verifico si perdieron todas las vidas
		if cont1 == cantVidas: vivo1 = False;
		if cont2 == cantVidas: vivo2 = False;
	
		#Verifico si el tiempo llego a cero quien tiene mas vida y quien gano
		if maxTime == 0:
			if cont1 < cont2:
				vivo2 = False
			elif cont1 > cont2:
				vivo1 = False
			elif cont1 == cont2:
				vivo1 = False
				vivo2 = False

		#Dibujo las vidas del jugador 1 y del jugador 2
		i = 0; x = 0
		for vida in LstVidas:
			if i <= cantVidas-1 and vidasOn[i]: 
				ventana.blit(vida, (-6,POSVIDAS[x]))
			if i > cantVidas-1 and vidasOn[i]:
				ventana.blit(vida, (ANCHO-43,POSVIDAS[x]))
			x += 1
			i += 1
			if x == cantVidas:
				x = 0

		#Lineas del fondo
		#pygame.draw.line(ventana, ORANGE, (40,0), (40, ALTO), 5)  # LINEA BASE 1
		#pygame.draw.line(ventana, ORANGE, (ANCHO-40,0), (ANCHO-40, ALTO), 5)  # LINEA BASE 2
		#pygame.draw.line(ventana, BLACK, (ANCHO/2,0),(ANCHO/2,ALTO), 1)  # LINEA MEDIO

		#dibujo la bola
		bola.getRectangulo().left, bola.getRectangulo().top = bola.getPos()
		bola.dibujarImg(*bola.getPos())
		
		#dibujo los jugadores
		jugador1.getRectangulo().left, jugador1.getRectangulo().top = jugador1.getPos()  
		jugador1.dibujarImg(*jugador1.getPos())  # Dibujo al jugador 1, uso un * ya que le paso una tupla
		
		jugador2.getRectangulo().left, jugador2.getRectangulo().top = jugador2.getPos()
		jugador2.dibujarImg(*jugador2.getPos())  # Dibujo al jugador 2
		
		#dibujo el tiempo
		ventana.blit(textoTime, ((ANCHO/2)-24, 45))  

		#dibujo los scores
		textoScore1 = FuenteArial2.render(str(score1), 0, (200, 60, 8))  
		textoScore2 = FuenteArial2.render(str(score2), 0, (200, 60, 8))  
		ventana.blit(textoScore, (70, 45))  
		ventana.blit(textoScore, ((ANCHO-240), 45))  
		ventana.blit(textoScore1, (220, 45))  # imprimo el score1
		ventana.blit(textoScore2, ((ANCHO-100), 45))  # imprimo el score2

		#pygame.draw.rect(ventana, ORANGE, bola.getRectangulo())
		#pygame.draw.rect(ventana, ORANGE, jugador1.getRectangulo())
		#pygame.draw.rect(ventana, ORANGE, jugador2.getRectangulo())
		
		#actualizo la pantalla
		pygame.display.update()

		#si perdio el jugador 1, esperare 3 segundos y mostrare un msj que gano el jugador2
		if vivo1 == False and vivo2:
			sonido = pygame.mixer.Sound("Music/win.wav")
			sonido.play()
			score2 += 1
			#Mido el Tiempo
			maxTime = 3
			aux = int(pygame.time.get_ticks()/1000) + 1 
			textoGano = FuenteArial.render("Player 2 Win", 0, (200, 60, 8))  # guardo el tiempo en un texto arial

			while (maxTime!=0):
				Time = int(pygame.time.get_ticks()/1000)  # mido el tiempo
				ventana.blit(textoGano, ((ANCHO/2)-140, (ALTO//2)-30))  # imprimo el texto
				pygame.display.update()

				if aux == Time:
					aux += 1  # Uso un aux para que cada ves que pasa un segundo pueda saberlo
					maxTime -= 1  # y por cada segundo voy decrementando el tiempo maximo asignado
		#si perdio el jugador 2, esperare 3 segundos y mostrare un msj que gano el jugador1
		if vivo2 == False and vivo1:
			sonido = pygame.mixer.Sound("Music/win.wav")
			sonido.play()
			score1 += 1
			#Mido el Tiempo
			maxTime = 3
			aux = int(pygame.time.get_ticks()/1000) + 1 
			textoGano = FuenteArial.render("Player 1 Win", 0, (200, 60, 8))  # guardo el tiempo en un texto arial

			while (maxTime!=0):
				Time = int(pygame.time.get_ticks()/1000)  # mido el tiempo
				ventana.blit(textoGano, ((ANCHO/2)-140, (ALTO//2)-30))  # imprimo el texto
				pygame.display.update()

				if aux == Time:
					aux += 1  # Uso un aux para que cada ves que pasa un segundo pueda saberlo
					maxTime -= 1  # y por cada segundo voy decrementando el tiempo maximo asignado
		if vivo2 == False and vivo1 == False:
			score1 += 1
			score2 += 1
			#Mido el Tiempo
			maxTime = 3
			aux = int(pygame.time.get_ticks()/1000) + 1 
			textoDraw = FuenteArial.render("Draw", 0, (200, 60, 8))  # guardo el tiempo en un texto arial

			while (maxTime!=0):
				Time = int(pygame.time.get_ticks()/1000)  # mido el tiempo
				ventana.blit(textoDraw, ((ANCHO/2)-50, (ALTO//2)-30))  # imprimo el texto
				pygame.display.update()

				if aux == Time:
					aux += 1  # Uso un aux para que cada ves que pasa un segundo pueda saberlo
					maxTime -= 1  # y por cada segundo voy decrementando el tiempo maximo asignado
