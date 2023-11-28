import pygame
from config import*
from pygame.locals import *
from funciones import*
import json
import os
from modularizacion.movimientos import* 
from modularizacion.eventos import * 
from modularizacion.colisiones import *
pygame.init()
pygame.display.set_caption("primer juego")
clock = pygame.time.Clock()

try:
    with open(os.path.join(dir_actual,"src/rutas/puntaje_maximo.json") , "r") as archivo:
        puntaje_maximo = json.load(archivo)
except:
    puntaje_maximo = [{"puntaje_maximo":"0"}]

while True:
    pantalla.blit(imagen_fondo_inicio,(0,0))
    musica_juego.play(-1)
    crear_boton(pantalla, "PLAY", blanco, rect_btn_play, rojo, rojo, fuente)
    crear_boton(pantalla, "EXIT", blanco, rect_btn_exit, rojo, rojo, fuente)
    respuesta =  pantalla_inicio(rect_btn_play,rect_btn_exit)
    if respuesta == 1:
        respawn = True
    elif respuesta == 2:
        terminar()

    pantalla.blit(imagen_fondo_tutorial,(0,0))
    if mostrar_tutorial: 
        pausa_tutorial()
    mostrar_tutorial = False
    while respawn:
        pygame.time.set_timer(EVENTO_NUEVO_BOTIQUIN,8000) 
        pygame.time.set_timer(EVENTO_RESPAWN_AK,17000)
        pygame.time.set_timer(EVENTO_TIEMPO_DISPARO , 350)
        pygame.time.set_timer(EVENTO_TIEMPO_RAFAGA,150)
        pygame.time.set_timer(EVENTO_EFECTO_RESPAWN,350)
        pygame.time.set_timer(EVENTO_ELIMINAR_AK,20000)
        pygame.time.set_timer(EVENTO_ELIMINAR_BOTIQUIN,11000)
        cantidad_zombies_principio = 10
        lista_zombies_rojos = []
        lista_zombies_normales = []
        lista_zombies_jefes = []
        rafagas = []
        correr_progama = True
        continuar_jugando = True
        dict_movimientos = {"mover_abajo":False, "mover_arriba":False , "mover_derecha":False ,"mover_izquierda":False} 
        dict_armas = {"mostrar_rifle":False, "mostrar_pistola":True}
        dict_eventos_tiempo = {"disparo":False, "disparos":False, "botiquin":None , "ak_disponible":None , "efecto": False} 
        dict_contadores = {"score":0, "contador_general":0, "contador_continuar":0, "contador_vidas": 3,  "municion_ak":0}
        rafaga_anterior = {"rafaga_anterior":None}
        personaje_rifle = personaje_principal(imagen_personaje_rifle,pantalla)
        personaje_pistola = personaje_principal(imagen_personaje_pistola,pantalla)
        crear_orda_zombies(lista_zombies_normales, cantidad_zombies_principio,imagen_zombie_normal,pantalla,vida_zombie_normal)

        pygame.mouse.set_visible(False)
        while continuar_jugando:
            pygame.mouse.set_visible(False)

            while correr_progama:
                clock.tick((60))
                for evento in pygame.event.get():
                    # CAPTURA LOS EVENTOS DE TECLADO DEL PERSONAJE 
                    evento_movimientos_personaje(evento , dict_movimientos ,  personaje_rifle)
                    # CAPTURA LOS EVENTOS DE CAMBIO DE ARMA CON LOS BOTONES
                    evento_cambio_de_arma(evento, dict_armas, dict_contadores["municion_ak"])
                    # CAPTURA TODOS LOS EVENTOS DE TIEMPO COMO RESPAW DE BOTIQUINES,AK,ETC...
                    eventos_de_tiempo( evento, dict_eventos_tiempo)
                    #CAPTURA LOS CLICKS DE DISPAROS CON EL MOUSE
                    evento_mouse_disparos(evento , dict_armas, personaje_rifle, rafagas , dict_eventos_tiempo ,dict_contadores)

                # CON LOS MOVIEMIENTOS DE LOS EVENTOS MUEVE AL PERSONAJE.
                movimiento_personaje_principal(dict_movimientos, personaje_rifle, speed_personaje)

                #MOVIENTO DE LOS ZOMBIES
                movimiento_zombies(lista_zombies_normales, speed_zombie_normal , dict_contadores )
                movimiento_zombies_rojos(lista_zombies_rojos, speed_zombie_rojo , dict_contadores )     
                movimiento_zombies_jefes(lista_zombies_jefes, speed_zombie_jefe , dict_contadores )       

                # MOVIENTO DE DISPARO
                movimiento_disparos(rafagas)    

                #DETECTO LAS COLISIONES DE LOS DISPAROS CON LOS ZOMBIES Y LOS ELIMINO, AUMENTO SCORE.s
                if rafagas:
                    for rafaga in rafagas[:]:
                        detecta_colision_de_disparo_zombie_normal(
                            rafagas, rafaga, lista_zombies_normales, dict_contadores , rafaga_anterior)

                        detecta_colision_de_disparo_zombie_rojo(
                            rafagas, rafaga, lista_zombies_rojos, dict_contadores , rafaga_anterior)

                        detecta_colision_de_disparo_zombie_jefe(
                            rafagas, rafaga, lista_zombies_jefes, dict_contadores , rafaga_anterior)
                                                         
                #COLISION DE PERSONAJE CON ZOMBIES Y PERDIDA DE VIDA
                detecta_colision_zombie_normal(
                    lista_zombies_normales, personaje_rifle, offset, dict_contadores)
                
                detecta_colision_zombie_rojo(
                    lista_zombies_rojos, personaje_rifle, offset, dict_contadores)
                
                detecta_colision_zombie_jefe(
                    lista_zombies_jefes, personaje_rifle, offset, dict_contadores)
               

                # DETECTA COLISION DE EL PERSONAJE CON UN BOTIQUIN 
                detecta_colision_botiquin(
                    dict_eventos_tiempo, offset , personaje_rifle, dict_contadores)

                # DETECTA COLISION DE EL PERSONAJE CON UN AK
                detecta_colision_ak(
                    dict_eventos_tiempo, personaje_rifle, offset , dict_contadores, dict_armas)

                # SI EL CONTADOR DE VIDAS LLEGA A 0 SE CIERRA EL PROGAMA PERDIENDO LA PARTIDA               
                if dict_contadores["contador_vidas"] == 0:
                    correr_progama = False

                # OBJETIVO PARA GANAR
                if  dict_contadores["contador_continuar"] == 0 and dict_contadores['score'] > 20 and  len(lista_zombies_jefes) == 0:
                    correr_progama = False

                #CREAR LAS ORDAS DE ZOMBIES
                if len(lista_zombies_normales) == 0:
                    crear_orda_zombies(lista_zombies_normales, cantidad_zombies_principio, imagen_zombie_normal, pantalla,vida_zombie_normal)
                    
                if dict_contadores["contador_general"] == 10 and len(lista_zombies_rojos) == 0:    
                    crear_orda_zombies(lista_zombies_rojos, cantidad_zombies_rojos, imagen_zombie_rojo, pantalla,vida_zombie_rojo)
                    if dict_contadores["contador_continuar"] == 0:
                       dict_contadores["contador_general"] = 0

                if  dict_contadores["contador_continuar"] == 0 and dict_contadores["score"] == 20 and len(lista_zombies_jefes) == 0 :
                    crear_orda_zombies(lista_zombies_jefes, cantidad_zombies_jefes, imagen_zombie_jefe, pantalla,vida_zombie_jefe)

                elif dict_contadores["contador_continuar"] == 1 and  dict_contadores["contador_general"] == 20 and len(lista_zombies_jefes) == 0:
                    crear_orda_zombies(lista_zombies_jefes, cantidad_zombies_jefes, imagen_zombie_jefe, pantalla,vida_zombie_jefe)
                    dict_contadores["contador_general"] = 0

                pantalla.blit(imagen_pantalla,(0,0))

                #DIBUJO DISPARO
                for rafaga in rafagas:
                    pygame.draw.rect(pantalla, rafaga["color"], rafaga["recta"])

                if dict_eventos_tiempo["botiquin"]:
                    if dict_eventos_tiempo["efecto"]:
                        pantalla.blit(imagen_botiquin_efecto, dict_eventos_tiempo["botiquin"]["recta"])
                    else:
                        pantalla.blit(dict_eventos_tiempo["botiquin"]["imagen"], dict_eventos_tiempo["botiquin"]["recta"])

                if dict_eventos_tiempo["ak_disponible"]:
                    if dict_eventos_tiempo["efecto"]:
                        pantalla.blit(imagen_ak_efecto,dict_eventos_tiempo["ak_disponible"]["recta"]) 
                    else:    
                        pantalla.blit(dict_eventos_tiempo["ak_disponible"]["imagen"],dict_eventos_tiempo["ak_disponible"]["recta"])   

                # BLITEO TODOS LOS TIPOS DE ZOMBIES    
                for zombie in lista_zombies_normales:
                    pantalla.blit(zombie["imagen"], zombie["recta"])

                for zombie_rojo in lista_zombies_rojos:
                    pantalla.blit(zombie_rojo["imagen"], zombie_rojo["recta"])

                for zombie_jefe in lista_zombies_jefes:
                    pantalla.blit(zombie_jefe["imagen"],zombie_jefe["recta"])    

                #DIBUJO LA VIDA Y EL SCORE
                mostrar_texto(pantalla,f" VIDA: {dict_contadores['contador_vidas']}",fuente_mas_chico,cordenada_arriba_derecha,rojo)
                mostrar_texto(pantalla,f"SCORE: {dict_contadores['score']}",fuente_mas_chico,cordenada_arriba_izquierda,rojo)

                if dict_contadores["municion_ak"]:
                    mostrar_texto(pantalla,f"municion { dict_contadores['municion_ak']}",fuente_mas_chico,cordenada_abajo_izquierda,rojo)

                #BLITEO AL PERSONAJE PRINCIPAL
                if dict_armas["mostrar_rifle"] :
                    pantalla.blit(personaje_rifle["imagen"], personaje_rifle["recta"])

                if dict_armas["mostrar_pistola"]:
                    pantalla.blit(personaje_pistola["imagen"], personaje_rifle["recta"])

                pygame.display.flip()
            #EN EL CASO QUE EL SCORE ACTUAL SEA UN RECORD SE GUARDA EN UN ARCHIVO JSON
            if dict_contadores['score'] > int(puntaje_maximo[0]["puntaje_maximo"]):  
                puntaje_maximo[0]["puntaje_maximo"] = str(dict_contadores['score'])
                with open(os.path.join("src/rutas/puntaje_maximo.json") , "w") as archivo:
                    json.dump(puntaje_maximo, archivo)
                    
            musica_juego.stop()
            pygame.mouse.set_visible(True)
            pygame.display.flip()

            if dict_contadores['score'] > 20 and len(lista_zombies_jefes) == 0 and dict_contadores["contador_continuar"] == 0: 
                pantalla.fill((0,0,0))
                pantalla.blit(imagen_fondo_win,(0,0))
                crear_boton(pantalla, "MENU", blanco, rect_btn_menu_principal_win, azul, azul, fuente)
                crear_boton(pantalla, "REINICIAR", blanco, rect_btn_reiniciar_win, azul, azul, fuente)
                crear_boton(pantalla, "CONTINUAR", blanco, rect_btn_continuar_win, azul, azul, fuente)
                mostrar_texto(pantalla,"MAX SCORE:" + puntaje_maximo[0]["puntaje_maximo"],fuente,cordenada_arriba_derecha,blanco)
                mostrar_texto(pantalla,f"SCORE: {dict_contadores['score']}",fuente,cordenada_arriba_izquierda,blanco)
                indicar = pantalla_fin(rect_btn_menu_principal_win, rect_btn_reiniciar_win, rect_btn_continuar_win)
                if indicar == 1:
                    respawn= False
                    continuar_jugando = False
                elif indicar == 2:
                    continuar_jugando = False
                elif indicar == 3:
                    correr_progama = True
                    dict_contadores["contador_continuar"] +=1        
            else:
                #sonido_game_over.play()
                pantalla.blit(imagen_fondo_final,(0,0))
                crear_boton(pantalla, "MENU", blanco, rect_btn_menu_principal, rojo, rojo, fuente)
                crear_boton(pantalla, "REINICIAR", blanco, rect_btn_reiniciar, rojo, rojo, fuente) 
                mostrar_texto(pantalla,f"SCORE: {dict_contadores['score']}",fuente,cordenada_arriba_izquierda,blanco)
                mostrar_texto(pantalla,"MAX SCORE:" + puntaje_maximo[0]["puntaje_maximo"],fuente,cordenada_arriba_derecha,blanco)
                indicar = pantalla_fin(rect_btn_menu_principal ,rect_btn_reiniciar)
                if indicar == 1:
                    respawn = False
                    continuar_jugando = False
                elif indicar == 2:
                    continuar_jugando =  False
                elif indicar == 3:
                    correr_progama = True           
            musica_juego.play()
        

