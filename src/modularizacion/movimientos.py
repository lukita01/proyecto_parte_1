import pygame
from config import*

def movimiento_personaje_principal(dict_movimientos:dict, personaje_rifle:dict, speed_personaje:int):  
    if dict_movimientos["mover_arriba"] and personaje_rifle["recta"].top > 0:
        personaje_rifle["recta"].top -= speed_personaje
    elif dict_movimientos["mover_abajo"] and personaje_rifle["recta"].bottom < alto:
        personaje_rifle["recta"].top += speed_personaje      
    if dict_movimientos["mover_derecha"] and personaje_rifle["recta"].right < ancho:
        personaje_rifle["recta"].left += speed_personaje
    elif dict_movimientos["mover_izquierda"] and personaje_rifle["recta"].left > 0 :
        personaje_rifle["recta"].left -= speed_personaje

def movimiento_zombies(lista_zombies:list, speed:int, dict_contadores:dict):
    for zombie in lista_zombies:
        if zombie["recta"].top < alto:
            zombie["recta"].top += speed
        else:
            dict_contadores["contador_vidas"] -=1
            lista_zombies.remove(zombie)
movimiento_zombies_rojos = movimiento_zombies
movimiento_zombies_jefes = movimiento_zombies

def movimiento_disparos(rafagas:list):      
    for rafaga in rafagas:
        rafaga["recta"].bottom -= rafaga["speed"]
        