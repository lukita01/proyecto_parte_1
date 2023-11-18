import pygame
from config import*
from pygame.locals import *
from funciones import*
import json
import os

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
    y =  pantalla_inicio(rect_btn_play,rect_btn_exit)
    if y == 1:
        respawn = True
    elif y == 2:
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
        flag = True
        ak_disponible = None
        botiquin = None
        mover_abajo = False
        mover_arriba = False
        mover_derecha = False
        mover_izquierda = False
        cantidad_zombies_principio = 10
        contador_general = 0
        score = 0
        contador_vidas = 3
        rafaga_anterior = None
        mostrar_pistola = True
        mostrar_rifle = False
        lista_zombies_rojos = []
        lista_zombies_normales = []
        lista_zombies_jefes = []
        disparo = False
        disparos = False
        rafagas = []	
        municion_ak = 0
        efecto = False
        contador_continuar = 0
        correr_progama = True
        continuar_jugando = True
        personaje_rifle = personaje_principal(imagen_personaje_rifle,pantalla)
        personaje_pistola = personaje_principal(imagen_personaje_pistola,pantalla)
        crear_orda_zombies(lista_zombies_normales, cantidad_zombies_principio,imagen_zombie_normal,pantalla,vida_zombie_normal)
        pygame.mouse.set_visible(False)
        while continuar_jugando:
            pygame.mouse.set_visible(False)

            while correr_progama:
                clock.tick((60))
                for evento in pygame.event.get():

                    if evento.type == QUIT:
                        terminar()

                    if evento.type == KEYDOWN:
                        if evento.key == K_UP or evento.key == K_w:
                            mover_arriba = True
                            mover_abajo = False
                        if evento.key == K_DOWN or evento.key == K_s:
                            mover_abajo = True
                            mover_arriba = False
                        if evento.key == K_RIGHT or evento.key == K_d:
                            mover_derecha = True
                            mover_izquierda = False
                        if evento.key == K_LEFT or evento.key == K_a:
                            mover_izquierda = True
                            mover_derecha = False

                        if evento.key == K_2 and municion_ak > 0 :
                            mostrar_pistola = False
                            mostrar_rifle = True

                        if evento.key == K_1: 
                            mostrar_rifle = False   
                            mostrar_pistola = True

                        if evento.key == K_p:
                            pausa()        

                    if evento.type == KEYUP:
                        if evento.key == K_UP or evento.key == K_w:
                            mover_arriba = False
                        if evento.key == K_DOWN or evento.key == K_s:
                            mover_abajo = False
                        if evento.key == K_RIGHT or evento.key == K_d:
                            mover_derecha = False
                        if evento.key == K_LEFT or evento.key == K_a:
                            mover_izquierda = False

                    if evento.type == EVENTO_TIEMPO_DISPARO:
                        disparo = True
                    if evento.type == EVENTO_TIEMPO_RAFAGA:
                        disparos = True    

                    #CLICK CREAR UN DISPARO o MODO RAFAGA

                    if evento.type == MOUSEBUTTONDOWN:       
                        if evento.button == 1:
                            if mostrar_pistola and disparo:
                                rafagas.append(crear_disparo(personaje_rifle["recta"].midtop,velocidad_disparo))  
                                sonido_pistola.play()
                                disparo = False

                            elif mostrar_rifle and disparos:
                                municion_ak -= 1
                                rafagas.append(crear_disparo(personaje_rifle["recta"].midtop,velocidad_disparo)) 
                                sonido_rifle.play()    
                                disparos = False
                                if municion_ak == 0:
                                    mostrar_pistola = True
                                    mostrar_rifle = False

                    #CREO EL BOTIQUIN CON UN EVENTO DE TIEMPO            
                    if evento.type == EVENTO_NUEVO_BOTIQUIN:
                        botiquin = crear_botiquin(imagen_botiquin,pantalla)
                    
                    if evento.type == EVENTO_RESPAWN_AK:
                        ak_disponible = crear_botiquin(imagen_ak,pantalla)

                    if evento.type == EVENTO_ELIMINAR_AK:
                        ak_disponible = None
                    
                    if evento.type == EVENTO_ELIMINAR_BOTIQUIN:
                        botiquin = None
                            
                    if evento.type == EVENTO_EFECTO_RESPAWN:
                        efecto = not efecto

                # MOVIENTO DE TODOS LOS PERSONAJES
                if mover_arriba and personaje_rifle["recta"].top > 0:
                    personaje_rifle["recta"].top -= speed_personaje
                elif mover_abajo and personaje_rifle["recta"].bottom < alto:
                    personaje_rifle["recta"].top += speed_personaje      
                if mover_derecha and personaje_rifle["recta"].right < ancho:
                    personaje_rifle["recta"].left += speed_personaje
                elif mover_izquierda and personaje_rifle["recta"].left > 0 :
                    personaje_rifle["recta"].left -= speed_personaje    

                #MOVIENTO DE LOS ZOMBIES         
                for zombie in lista_zombies_normales:
                    if zombie["recta"].top < alto:
                        zombie["recta"].top += 2
                    else:
                        contador_vidas -=1
                        lista_zombies_normales.remove(zombie)

                for zombie_rojo in lista_zombies_rojos:
                    if zombie_rojo["recta"].top < alto:
                        zombie_rojo["recta"].top += 1
                    else:
                        contador_vidas -=1  
                        lista_zombies_rojos.remove(zombie_rojo)

                for zombie_jefe in lista_zombies_jefes:
                    if zombie_jefe["recta"].top < alto:

                        zombie_jefe["recta"].top += 1
                    else:
                        contador_vidas -=1
                        lista_zombies_jefes.remove(zombie_jefe)

                # MOVIENTO DE DISPARO
                for rafaga in rafagas:
                    rafaga["recta"].bottom -= rafaga["speed"]        

                #DETECTO LAS COLISIONES DE LOS DISPAROS CON LOS ZOMBIES Y LOS ELIMINO, AUMENTO SCORE.
                if rafagas:
                    for rafaga in rafagas[:]:
                        for zombie in lista_zombies_normales[:]:
                            if zombie["recta"].colliderect(rafaga["recta"]):
                                zombie["vida"] -=1
                                try:
                                    rafagas.remove(rafaga)  
                                    rafaga_anterior = rafaga  
                                except:    
                                    if rafaga_anterior != rafaga:
                                        rafagas.remove(rafaga)
                                        rafaga_anterior = rafaga
                            if zombie["vida"] == 0:
                                lista_zombies_normales.remove(zombie)
                                score +=1
                                contador_general +=1  

                        for zombie_rojo in lista_zombies_rojos[:]:
                            if zombie_rojo["recta"].colliderect(rafaga["recta"]):
                                zombie_rojo["vida"] -=1
                                try:
                                    rafagas.remove(rafaga)
                                    rafaga_anterior = rafaga    
                                except:    
                                    if rafaga_anterior != rafaga:
                                        rafagas.remove(rafaga)
                            if zombie_rojo["vida"] == 0:
                                lista_zombies_rojos.remove(zombie_rojo)
                                score +=1
                                contador_general +=1
                                
                        for zombie_jefe in lista_zombies_jefes[:]:
                            if zombie_jefe["recta"].colliderect(rafaga["recta"]):
                                zombie_jefe["vida"] -=1
                                try:
                                    rafagas.remove(rafaga)
                                    rafaga_anterior = rafaga    
                                except:    
                                    if rafaga_anterior != rafaga:
                                        rafagas.remove(rafaga)
                            if zombie_jefe["vida"] == 0:
                                lista_zombies_jefes.remove(zombie_jefe)
                                score +=1
                                if contador_continuar == 1:
                                    contador_general += 1

                        #ELIMINO EL DISPARO SI SALIO DE LA PANTALLA        
                        if rafaga["recta"].bottom <= 0:
                            try:
                                rafagas.remove(rafaga)
                                rafaga_anterior = rafaga  
                            except:
                                if rafaga_anterior != rafaga:
                                    rafagas.remove(rafaga)
                                                    
                    
                #COLISION DE PERSONAJES CON ZOMBIES Y PERDIDA DE VIDA
                for zombie in lista_zombies_normales:
                    if personaje_rifle["mascara"].overlap(zombie["mascara"], offset(zombie["recta"],personaje_rifle["recta"])):
                        zombie["vida"] -=1
                        if zombie["vida"] == 0:
                            lista_zombies_normales.remove(zombie)
                            contador_vidas -=1

                for zombie_rojo in lista_zombies_rojos:
                    if personaje_rifle["mascara"].overlap(zombie_rojo["mascara"], offset(zombie_rojo["recta"],personaje_rifle["recta"])):
                        zombie_rojo["vida"] -=1
                        if zombie_rojo["vida"] == 0:
                            lista_zombies_rojos.remove(zombie_rojo)
                            contador_vidas -=1 

                for zombie_jefe in lista_zombies_jefes:
                    if personaje_rifle["mascara"].overlap(zombie_jefe["mascara"], offset(zombie_jefe["recta"],personaje_rifle["recta"])):
                        zombie_jefe["vida"] -=1
                        if zombie_jefe["vida"] == 0:
                            lista_zombies_jefes.remove(zombie_jefe)
                            contador_vidas -=1

                if botiquin:
                    if personaje_rifle["mascara"].overlap(botiquin["mascara"], offset(botiquin["recta"],personaje_rifle["recta"])):
                        botiquin = None 
                        if contador_vidas < 5:   
                            contador_vidas +=1

                if ak_disponible:
                    if personaje_rifle["mascara"].overlap(ak_disponible["mascara"], offset(ak_disponible["recta"],personaje_rifle["recta"])):
                        municion_ak = 60
                        mostrar_rifle = True
                        mostrar_pistola = False
                        ak_disponible = None 
                                
                if contador_vidas == 0:
                    correr_progama = False

                if  contador_continuar == 0 and score > 10 and  len(lista_zombies_jefes) == 0:
                    correr_progama = False

                #CREAR LAS ORDAS DE ZOMBIES
                if len(lista_zombies_normales) == 0:
                    crear_orda_zombies(lista_zombies_normales, cantidad_zombies_principio, imagen_zombie_normal, pantalla,vida_zombie_normal)
                    
                if contador_general == 10 and len(lista_zombies_rojos) == 0:    
                    crear_orda_zombies(lista_zombies_rojos, cantidad_zombies_rojos, imagen_zombie_rojo, pantalla,vida_zombie_rojo)
                    if contador_continuar == 0:
                        contador_general = 0

                if  contador_continuar == 0 and score == 10 and len(lista_zombies_jefes) == 0 :
                    crear_orda_zombies(lista_zombies_jefes, cantidad_zombies_jefes, imagen_zombie_jefe, pantalla,vida_zombie_jefe)

                elif contador_continuar == 1 and  contador_general == 20 and len(lista_zombies_jefes) == 0:
                    crear_orda_zombies(lista_zombies_jefes, cantidad_zombies_jefes, imagen_zombie_jefe, pantalla,vida_zombie_jefe)
                    contador_general = 0

                pantalla.blit(imagen_pantalla,(0,0))

                #DIBUJO DISPARO
                for rafaga in rafagas:
                    pygame.draw.rect(pantalla, rafaga["color"], rafaga["recta"])

                if botiquin:
                    if efecto:
                        pantalla.blit(imagen_botiquin_efecto, botiquin["recta"])
                    else:
                        pantalla.blit(botiquin["imagen"], botiquin["recta"])

                if ak_disponible:
                    if efecto:
                        pantalla.blit(imagen_ak_efecto,ak_disponible["recta"]) 
                    else:    
                        pantalla.blit(ak_disponible["imagen"],ak_disponible["recta"])   

                # BLITEO TODOS LOS TIPOS DE ZOMBIES    
                for zombie in lista_zombies_normales:
                    pantalla.blit(zombie["imagen"], zombie["recta"])

                for zombie_rojo in lista_zombies_rojos:
                    pantalla.blit(zombie_rojo["imagen"], zombie_rojo["recta"])

                for zombie_jefe in lista_zombies_jefes:
                    pantalla.blit(zombie_jefe["imagen"],zombie_jefe["recta"])    

                #DIBUJO LA VIDA Y EL SCORE
                mostrar_texto(pantalla,f" VIDA: {contador_vidas}",fuente_mas_chico,cordenada_arriba_derecha,rojo)
                mostrar_texto(pantalla,f"SCORE: {score}",fuente_mas_chico,cordenada_arriba_izquierda,rojo)

                if municion_ak:
                    mostrar_texto(pantalla,f"municion {municion_ak}",fuente_mas_chico,cordenada_abajo_izquierda,rojo)

                #BLITEO AL PERSONAJE PRINCIPAL
                if mostrar_rifle:
                    pantalla.blit(personaje_rifle["imagen"], personaje_rifle["recta"])

                if mostrar_pistola:
                    pantalla.blit(personaje_pistola["imagen"], personaje_rifle["recta"])

                pygame.display.flip()

            if score > int(puntaje_maximo[0]["puntaje_maximo"]):  
                puntaje_maximo[0]["puntaje_maximo"] = str(score)
                with open(os.path.join("src/rutas/puntaje_maximo.json") , "w") as archivo:
                    json.dump(puntaje_maximo, archivo)
                    
            musica_juego.stop()

            pygame.mouse.set_visible(True)
            pygame.display.flip()

            if score > 10 and contador_continuar == 0: 
                pantalla.fill((0,0,0))
                pantalla.blit(imagen_fondo_win,(0,0))

                crear_boton(pantalla, "MENU", blanco, rect_btn_menu_principal_win, azul, azul, fuente)
                crear_boton(pantalla, "REINICIAR", blanco, rect_btn_reiniciar_win, azul, azul, fuente)
                crear_boton(pantalla, "CONTINUAR", blanco, rect_btn_continuar_win, azul, azul, fuente)
                mostrar_texto(pantalla,"MAX SCORE:" + puntaje_maximo[0]["puntaje_maximo"],fuente,cordenada_arriba_derecha,blanco)
                mostrar_texto(pantalla,f"SCORE: {score}",fuente,cordenada_arriba_izquierda,blanco)

                indicar =  pantalla_fin(rect_btn_menu_principal_win, rect_btn_reiniciar_win, rect_btn_continuar_win)
                if indicar == 1:
                    respawn= False
                    continuar_jugando = False
                elif indicar == 2:
                    continuar_jugando = False
                elif indicar == 3:
                    correr_progama = True
                    contador_continuar +=1        
            else:
                sonido_game_over.play()
                pantalla.blit(imagen_fondo_final,(0,0))

                crear_boton(pantalla, "MENU", blanco, rect_btn_menu_principal, rojo, rojo, fuente)
                crear_boton(pantalla, "REINICIAR", blanco, rect_btn_reiniciar, rojo, rojo, fuente) 

                mostrar_texto(pantalla,f"SCORE: {score}",fuente,cordenada_arriba_izquierda,blanco)
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
        

