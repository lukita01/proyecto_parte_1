import pygame
from pygame.locals import *
from funciones import *
from config import *

def evento_movimientos_personaje(evento:pygame.event, movimientos:dict,
                                 personaje_rifle:dict):
    
    if evento.type == QUIT:
        terminar()

    if evento.type == KEYDOWN:
        if evento.key == K_UP or evento.key == K_w:
            movimientos["mover_arriba"] = True
            movimientos["mover_abajo"] = False
        if evento.key == K_DOWN or evento.key == K_s:
            movimientos["mover_abajo"] = True
            movimientos["mover_arriba"] = False
        if evento.key == K_RIGHT or evento.key == K_d:
            movimientos["mover_derecha"] = True
            movimientos["mover_izquierda"] = False
        if evento.key == K_LEFT or evento.key == K_a:
            movimientos["mover_izquierda"] = True
            movimientos["mover_derecha"] = False

        if evento.key == K_p:
            pausa()        
        
    if evento.type == KEYUP:
        if evento.key == K_UP or evento.key == K_w:
            movimientos["mover_arriba"] = False
        if evento.key == K_DOWN or evento.key == K_s:
            movimientos["mover_abajo"] = False
        if evento.key == K_RIGHT or evento.key == K_d:
            movimientos["mover_derecha"] = False
        if evento.key == K_LEFT or evento.key == K_a:
            movimientos["mover_izquierda"] = False

           
def evento_cambio_de_arma(evento:pygame.event, dict_armas:dict, municion_ak:int):
    if evento.type == KEYDOWN:
        if evento.key == K_2 and municion_ak > 0 :
            dict_armas["mostrar_pistola"] = False
            dict_armas["mostrar_rifle"] = True

        if evento.key == K_1: 
            dict_armas["mostrar_rifle"] = False   
            dict_armas["mostrar_pistola"] = True

def eventos_de_tiempo(evento:pygame.event, dict_eventos_tiempo:dict):
    if evento.type == EVENTO_TIEMPO_DISPARO:
        dict_eventos_tiempo["disparo"] = True

    if evento.type == EVENTO_TIEMPO_RAFAGA:
        dict_eventos_tiempo["disparos"]  = True 

    if evento.type == EVENTO_NUEVO_BOTIQUIN:
        dict_eventos_tiempo["botiquin"] = crear_botiquin(imagen_botiquin,pantalla)
    
    if evento.type == EVENTO_RESPAWN_AK:
        dict_eventos_tiempo["ak_disponible"] = crear_botiquin(imagen_ak,pantalla)

    if evento.type == EVENTO_ELIMINAR_AK:
        dict_eventos_tiempo["ak_disponible"] = None
    
    if evento.type == EVENTO_ELIMINAR_BOTIQUIN:
        dict_eventos_tiempo["botiquin"]  = None
            
    if evento.type == EVENTO_EFECTO_RESPAWN:
        dict_eventos_tiempo["efecto"]  = not dict_eventos_tiempo["efecto"]    

def evento_mouse_disparos(evento:pygame.event ,dict_armas:dict , personaje_rifle:dict, rafagas:list , 
                 dict_eventos_tiempo:dict, dict_contadores:dict):
    
    if evento.type == MOUSEBUTTONDOWN:       
        if evento.button == 1:
            if  dict_armas["mostrar_pistola"] and dict_eventos_tiempo["disparo"]:
                rafagas.append(crear_disparo(personaje_rifle["recta"].midtop,velocidad_disparo))  
                sonido_pistola.play()
                dict_eventos_tiempo["disparo"] = False

            elif dict_armas["mostrar_rifle"] and dict_eventos_tiempo["disparos"]:
                dict_contadores["municion_ak"] -= 1    
                rafagas.append(crear_disparo(personaje_rifle["recta"].midtop,velocidad_disparo)) 
                sonido_rifle.play()    
                dict_eventos_tiempo["disparos"] = False
                if dict_contadores["municion_ak"] == 0:
                    dict_armas["mostrar_pistola"] = True
                    dict_armas["mostrar_rifle"] = False





