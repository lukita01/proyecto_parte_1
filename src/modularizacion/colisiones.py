import pygame
from config import *
from pygame.locals import *

def detecta_colision_de_disparo_zombie_normal(rafagas:list , rafaga:dict, lista_zombies:list , dict_contadores:dict, 
                                rafaga_anterior:dict):
    for zombie in lista_zombies[:]:
        if zombie["recta"].colliderect(rafaga["recta"]):
            zombie["vida"] -=1
            try:
                rafaga_anterior["rafaga_anterior"] = rafaga  
                rafagas.remove(rafaga)  
            except:    
                if rafaga_anterior["rafaga_anterior"] != rafaga:
                    rafagas.remove(rafaga)
        if zombie["vida"] == 0:
            lista_zombies.remove(zombie)
            dict_contadores["score"] +=1
            dict_contadores["contador_general"] +=1  
        if rafaga["recta"].bottom <= 0:
            try:
                rafaga_anterior["rafagas" ] = rafaga  
                rafagas.remove(rafaga)
            except:
                if rafaga_anterior["rafagas" ] != rafaga:
                    rafagas.remove(rafaga)
detecta_colision_de_disparo_zombie_jefe = detecta_colision_de_disparo_zombie_normal
detecta_colision_de_disparo_zombie_rojo = detecta_colision_de_disparo_zombie_normal                    

def detecta_colision_zombie_normal(lista_zombies:list, personaje_rifle:dict, offset, dict_contadores:dict):
    for zombie in lista_zombies:
        if personaje_rifle["mascara"].overlap(zombie["mascara"], offset(zombie["recta"],personaje_rifle["recta"])):
            zombie["vida"] -=1
            if zombie["vida"] == 0:
                lista_zombies.remove(zombie)
                dict_contadores["contador_vidas"] -=1
detecta_colision_zombie_rojo = detecta_colision_zombie_normal
detecta_colision_zombie_jefe = detecta_colision_zombie_normal

def detecta_colision_botiquin(dict_eventos_tiempo:dict , offset,personaje_rifle:dict, dict_contadores:dict):
    if dict_eventos_tiempo["botiquin"]:
        if personaje_rifle["mascara"].overlap(dict_eventos_tiempo["botiquin"]["mascara"], 
                        offset(dict_eventos_tiempo["botiquin"]["recta"],personaje_rifle["recta"])):
            dict_eventos_tiempo["botiquin"] = None 
            if dict_contadores["contador_vidas"] < 6:   
                dict_contadores["contador_vidas"] +=1

def detecta_colision_ak(dict_eventos_tiempo:dict ,personaje_rifle:dict, offset , 
                        dict_contadores:dict, dict_armas:dict ):
    if dict_eventos_tiempo["ak_disponible"] :
        if personaje_rifle["mascara"].overlap(dict_eventos_tiempo["ak_disponible"]["mascara"], 
                        offset(dict_eventos_tiempo["ak_disponible"]["recta"],personaje_rifle["recta"])):
            dict_contadores["municion_ak"] = 60
            dict_armas["mostrar_rifle"]  = True
            dict_armas["mostrar_pistola"] = False
            dict_eventos_tiempo["ak_disponible"] = None 