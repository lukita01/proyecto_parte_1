import pygame
import os
import json
pygame.mixer.init()
pygame.font.init()

# ANCHO Y ALTO DE LA PANTALLA
ancho, alto = (800 , 600)

dir_actual = os.getcwd()

pantalla = pygame.display.set_mode((ancho,alto)) 

#CREO UN TIPO DE EVENTO NUEVO
EVENTO_NUEVO_BOTIQUIN = pygame.USEREVENT + 1
EVENTO_RESPAWN_AK = pygame.USEREVENT + 2
EVENTO_TIEMPO_DISPARO = pygame.USEREVENT + 3
EVENTO_TIEMPO_RAFAGA = pygame.USEREVENT + 4
EVENTO_EFECTO_RESPAWN= pygame.USEREVENT + 5
EVENTO_ELIMINAR_AK= pygame.USEREVENT + 6
EVENTO_ELIMINAR_BOTIQUIN= pygame.USEREVENT + 7

# COLORES HARCODEADOS
azul = ( 0 , 100 , 200)
negro = (0,0,0)
blanco = (255, 255, 255)
amarillo = (255 , 242 , 0)
rojo = (255,0,0)

respawn = False

speed_personaje = 10

velocidad_disparo = 7

valor_archivo = False
#CANTIDAD DESDEADA PARA EL RESPAWN DE ZOMBIES
cantidad_zombies_rojos = 8
cantidad_zombies_jefes = 3

#TAMAÑO PREDETERMINADO DE BOTONES
Tamaño_botones = 200 , 50
Tamaño_botones_win = 250,70


mostrar_tutorial = True
#FUENTE PREDETERMINADA
fuente = pygame.font.Font(None,40)
fuente_mas_chico = pygame.font.Font(None,30)

#CORDENADAS HARCODEADAS
cordenada_arriba_derecha = (600,50)
cordenada_arriba_izquierda = (150,50)
cordenada_medio_abajo = (ancho // 2,alto - 50)
cordenada_abajo_izquierda = (150,alto-50)
centro_pantalla = (ancho // 2 , alto // 2)

#VIDA DE LOS ZOMBIES
vida_zombie_normal = 2
vida_zombie_rojo = 3
vida_zombie_jefe = 6

speed_zombie_normal = 2
speed_zombie_rojo = 1
speed_zombie_jefe = 1

def cargar_imagenes_dict(lista:list, indice:int , clave_direccion:str ,clave_tamaño_x:str = None,clave_tamaño_y:str = None):
        ''''
        Esta funcion recibe la lista: list de diccionarios:dict.\n
        el indice:int  donde esta ubicado ese diccionario en la lista.\n
        la clave: str del diccionario para acceder a la ruta donde esta ubicado ese archivo.\n
        la clave del tamaño x: str donde se ubica el valor X.\n
        la clave del tamaño y: str donde se ubica el valor y .\n
        en caso que reciba sonidos no hace falta los tamaños.\n
        si recibe imagenes retorna: pygame.transform.scale(pygame.image.load(lista[indice][clave_direccion]),(clave_tamaño_x,clave_tamaño_y))\n
        si recibe sonidos retorna: pygame.mixer.Sound(lista[indice][clave_direccion])\n
        esta funcion se puede llamar con cargar_imagenes_dict o cargar_sonido_dict.
        '''''
        if clave_tamaño_x:
            clave_tamaño_x = int(lista[indice][clave_tamaño_x])
            clave_tamaño_y = int(lista[indice][clave_tamaño_y])
            return pygame.transform.scale(pygame.image.load(lista[indice][clave_direccion]),(clave_tamaño_x,clave_tamaño_y))
        else:
            return pygame.mixer.Sound(lista[indice][clave_direccion])     
cargar_sonido_dict = cargar_imagenes_dict

with open(os.path.join(dir_actual, "src/rutas/ruta_imagenes.json"), "r") as file:
    lista_imagenes = json.load(file)    

with open(os.path.join(dir_actual,"src/rutas/ruta_sonidos.csv"),"r") as file:
    encabezado = file.readline().strip()
    lista_sonidos = file.readlines()
    for i,valor in enumerate(lista_sonidos):
        diccionario = {}
        valor = valor.strip()
        diccionario[encabezado] = valor
        lista_sonidos[i] = diccionario

#CARGO LA MUSICA
sonido_rifle = cargar_sonido_dict(lista_sonidos, 0, "dir_sonido")
sonido_pistola = cargar_sonido_dict(lista_sonidos, 1, "dir_sonido")    
musica_juego = cargar_sonido_dict(lista_sonidos, 2 , "dir_sonido")
sonido_game_over = cargar_sonido_dict(lista_sonidos, 3, "dir_sonido")
#CARGO LAS IMAGENES A VARIABLES
imagen_ak = cargar_imagenes_dict(lista_imagenes, 0, "dir_imagen", "tamanio_x", "tamanio_y")
imagen_ak_efecto = cargar_imagenes_dict(lista_imagenes, 1, "dir_imagen", "tamanio_x", "tamanio_y")
imagen_personaje_rifle = cargar_imagenes_dict(lista_imagenes, 2, "dir_imagen", "tamanio_x", "tamanio_y") 
imagen_personaje_pistola = cargar_imagenes_dict(lista_imagenes, 3, "dir_imagen", "tamanio_x", "tamanio_y")
imagen_zombie_normal = cargar_imagenes_dict(lista_imagenes, 4 , "dir_imagen", "tamanio_x", "tamanio_y")
imagen_zombie_rojo = cargar_imagenes_dict(lista_imagenes, 5, "dir_imagen", "tamanio_x", "tamanio_y")
imagen_zombie_jefe = cargar_imagenes_dict(lista_imagenes, 6 , "dir_imagen", "tamanio_x", "tamanio_y")
imagen_botiquin = cargar_imagenes_dict(lista_imagenes, 7, "dir_imagen", "tamanio_x","tamanio_y")
imagen_botiquin_efecto = cargar_imagenes_dict(lista_imagenes, 8, "dir_imagen", "tamanio_x", "tamanio_y")
imagen_pantalla = cargar_imagenes_dict(lista_imagenes, 9, "dir_imagen", "tamanio_x", "tamanio_y")
imagen_fondo_final= cargar_imagenes_dict(lista_imagenes,10 , "dir_imagen", "tamanio_x","tamanio_y")  
imagen_fondo_inicio = cargar_imagenes_dict( lista_imagenes , 11 , "dir_imagen", "tamanio_x", "tamanio_y")  
imagen_fondo_win = cargar_imagenes_dict( lista_imagenes , 12 , "dir_imagen", "tamanio_x", "tamanio_y")
imagen_fondo_tutorial = cargar_imagenes_dict( lista_imagenes , 13 , "dir_imagen", "tamanio_x", "tamanio_y")

#RECTAS BOTONES
rect_btn_reiniciar = pygame.Rect(pantalla.get_width() // 2 - Tamaño_botones[0] // 2, 250 , Tamaño_botones[0], Tamaño_botones[1])
rect_btn_menu_principal= pygame.Rect(pantalla.get_width() // 2 - Tamaño_botones[0] // 2, 150 , Tamaño_botones[0], Tamaño_botones[1])

rect_btn_reiniciar_win = pygame.Rect(200 - Tamaño_botones[0] // 2, 430 , Tamaño_botones_win[0], Tamaño_botones_win[1])
rect_btn_menu_principal_win= pygame.Rect(550 - Tamaño_botones[0] // 2, 430  , Tamaño_botones_win[0], Tamaño_botones_win[1])
rect_btn_continuar_win= pygame.Rect(380 - Tamaño_botones[0] // 2, 510  , Tamaño_botones_win[0], Tamaño_botones_win[1])

rect_btn_exit= pygame.Rect(pantalla.get_width() // 2 - Tamaño_botones[0] // 2, 250 , Tamaño_botones[0], Tamaño_botones[1])
rect_btn_play= pygame.Rect(pantalla.get_width() // 2 - Tamaño_botones[0] // 2, 150 , Tamaño_botones[0], Tamaño_botones[1])
