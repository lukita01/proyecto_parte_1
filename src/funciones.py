import pygame
from random import randrange
from config import *
from pygame.locals import *
from pygame import surface,font

pygame.init()
# FUNCION COLORES RANDOMS
def color_random() ->tuple:
    """
    retorna una tupla de 3 elementos
    con numeros randoms \n
    se usa para retornar un color random\n
    return ->  tupla (r , g , b)
    """
    from random import randrange
    r = randrange(256)
    g = randrange(256)
    b = randrange(256)
    return(r , g , b)

#FUNCION CREAR LOS BOTONES DEL MENU
def crear_boton(pantalla:pygame.surface, texto:str, color_font:tuple, recta_btn:pygame.Rect, bg_color: tuple, 
                bg_color_hover:tuple = False,fuente = pygame.font.Font(None,36)):
    ''''
    se utiliza para crear un boton y que se dibuje en la pantalla\n
    se le ingresa:\n
    La pantalla: surface donde se quiere dibujar, El texto: Str deseado , Color: Tuple de la fuente
    , recta: Rect ya fabricada, El color: Tuple para el background del boton ,
    color: Tuple para el color del Background Hover y una Fuente.\n
    el hover del background sirve para que al momento de pasar el cursor\n
    encima del boton cambie de color
    '''''
    if not bg_color_hover:
        bg_color_hover = bg_color
    render = fuente.render(texto,True,color_font)
    recta_text = render.get_rect(center = recta_btn.center)
    if recta_btn.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(pantalla,bg_color_hover,recta_btn,border_radius = 5)
    else:
        pygame.draw.rect(pantalla,bg_color,recta_btn,border_radius = 5)    
    pantalla.blit(render,recta_text)

#DESFASAMIENTO DE MASCARAS
def offset(recta_1:Rect , recta_2: Rect) -> tuple:
    ''''
    Se le ingresa dos rectas:Rect  ya fabricadas\n
    Sirve para a la hora de hacer el overlap de dos rectas
    te lo calcular automaticamente\n
    Para poder calcular el desfasamiento entre las dos rectas\n
    return offset = (recta_1.x - recta_2.x , recta_1.y - recta_2.y)
    '''''
    return (recta_1.x - recta_2.x , recta_1.y - recta_2.y)

# CREA TEXTO CON JUNTO CON SU UBICACION
def mostrar_texto (pantalla:surface, texto:str, fuente:font = pygame.font.Font(None,40), coordenadas:tuple = (100,100)
                   , color_texto:tuple = (negro), color_fondo:tuple = None):
    ''''
    Esta funcion dibuja un texto deseado en la pantalla\n
    Recibe:\n
    Pantalla: Surface se quierda dibujar, texto: Str deseado , Fuente:Font , Cordenadas:tuple donde dibujar,
    Color: tuple del texto  y un Color: tuple  para el background del texto si se desea

    '''''
    superficie_texto = fuente.render(texto, True, color_texto, color_fondo)
    rectangulo_texto = superficie_texto.get_rect(center = coordenadas)
    pantalla.blit(superficie_texto, rectangulo_texto)    

# CREA UN DISPARO Y SU VELOCIDAD
def crear_disparo(mid_bottom:int ,velocidad:int = 5 ) -> dict:
    ''''
    Esta funcion crea un diccionario con valores necesario para un disparo\n
    Recibe:\n
    mid_bottom: tuple es donde se ubica la parte inferior del disparo
    y la Velocidad: int  deseada del disparo\n
    retorna un diccionario con el disparo creado, ejemplo:\n
    retorna {"recta":pygame.Rect(mid_bottom[0] + 17, mid_bottom[1] - 8, 6, 16),"speed":velocidad, "color":amarillo}\n
    '''''
    return {"recta":pygame.Rect(mid_bottom[0] + 17, mid_bottom[1] - 8, 6, 16),"speed":velocidad, "color":amarillo}

# CREA AL PERSONAJE PRINCILA Y SU RESPAWN
def personaje_principal(imagen:surface, pantalla:surface) -> dict: 
    '''
    Esta funcion crea un diccionario con lo necesario para un personaje.\n
    Recibe:\n
    una La imagen:Surface y Pantalla:Surface de la pantalla.\n
    La funcion retorna la recta , La mascara y la imagen del personaje\n
    ejemplo de retorno:\n
    return {"recta":recta, "mascara":mascara, "imagen":imagen}
    '''''
    recta = imagen.get_rect(center = (pantalla.get_width() // 2 ,pantalla.get_height() - imagen.get_height() // 2))
    mascara= pygame.mask.from_surface(imagen)
    return {"recta":recta, "mascara":mascara, "imagen":imagen}

# CREA UN ZOMBIE Y SU CORDENADA DE RESPAWN
def crear_zombie(imagen:pygame.surface , x:int , y:int,vida:int = 0) -> dict:  
    '''
    Esta funcion sirve para crear los personajes tipo zombie.\n
    Recibe la imagen del zombie:surface ,Las cordenas X:int  y  Y:int  ,La vida:int  del mismo.\n
    retorna La recta, La mascara , La imagen, y La vida del personaje,Ejemplo:\n
    return {"recta":recta, "mascara":mascara, "imagen":imagen, "vida":vida}
    '''''
    recta = imagen.get_rect(center = (x , y))
    mascara = pygame.mask.from_surface(imagen)
    return {"recta":recta, "mascara":mascara, "imagen":imagen, "vida":vida}

# CREAR UN BOTIQUIN Y SU RESPAWN ALEATORIO
def crear_botiquin(imagen:pygame.surface, pantalla:pygame.surface) -> dict:
    '''
    Recibe la imagen:surface , La pantalla: surface donde ubicarlo
    y lo ubica de forma random en la pantalla.\n
    retorna  return {"recta":recta, "mascara":mascara, "imagen":imagen, "vida":vida}
    '''''
    return crear_zombie(imagen,randrange(imagen.get_width() // 2, pantalla.get_width() - imagen.get_width() // 2),
                        randrange(imagen.get_height() // 2,pantalla.get_height() - imagen.get_height() // 2),)

#AÑADE A LA LISTA DICCIONARIOS DE ZOMBIES PARA Q SE CARGEN Y APAREZCAN
def crear_orda_zombies(lista:list , cantidad:int, imagen:pygame.surface , pantalla:pygame.surface , vida:int):
    '''
    Esta funcion sirve para cargar una lista con principalmente zombies.
    Recibe:\n
    Una lista:list , cantidad: int , imagen:surface , pantalla:surface , vida: int\n 
    no Retorna nada ya q la lista son mutables,se les carga automaticamente.
    '''''
    for zombies in range(0,cantidad):
        lista.append(crear_zombie(imagen, 
                                  (randrange(imagen.get_width() // 2 ,pantalla.get_width() - imagen.get_width() // 2))
                                  ,randrange(-1500,-300),vida))
        
# TERMINA EL PROGAMA Y CIERRA PYGAME
def terminar():
    '''
    Esta funcion sive para cerrar automaticante el pygame.
    '''''
    pygame.quit()
    exit()

#PAUSA EL PROGAMA HASTA Q PRESIONE UNA TECLA                    
def pausa_tutorial():
    '''
    Esta funcion pausa el progama entrando en un bucle.\n
    sale del mismo cuando se precione una tecla o boton del mouse. 
    '''''

    pygame.display.flip()
    while True:
        for evento in pygame.event.get():
            if evento.type == QUIT:
                terminar()
            if evento.type == KEYDOWN:
                if evento.key == K_ESCAPE:
                   terminar()
                return   
            if evento.type == MOUSEBUTTONDOWN:
                return    
def pausa():
    '''
    Esta funcion pausa el progama cuando se preciona la P entrando en un bucle.\n
    Y sale si se preciona la P nuevamente o el Escape.\n
    muestra un texto en la pantalla con la frase : PAUSA.
    '''''
    while True:
        pausa = mostrar_texto(pantalla,"PAUSA",fuente,centro_pantalla,rojo)
        pygame.display.flip()
        for evento in pygame.event.get():
            if evento.type == QUIT:
                terminar()
            if evento.type == KEYDOWN:
                if evento.key == K_ESCAPE:
                   terminar()
                if evento.key == K_p:
                    return
                
#PANTALLA FINAL DEL JUEGO                    
def pantalla_fin(rectangulo_1:Rect, rectangulo_2:Rect , rectangulo_3:Rect = None):
    '''
    Esta funcion recibe 3 o 2 Rectangulos: Rect.\n
    Sirve para detectar si 3 o 2 rectangulos en la pantalla 
    se les preciona con la funcion collidepoint de pygame.\n
    Recibe el evento de pos de event.get(),de pygame.\n
    La funcion entra en un bucle hasta que detecte un click
    en alguna de las rectas\n
    si detecta colision en el 1er rect retorna: 1 (int)\n
    si detecta en el 2do retorna: 2 (int)\n
    si detecta en el 3ro retorna: 3 (int) . 
    '''''
    while True:
        pygame.display.flip()
        for evento in pygame.event.get():
            if evento.type == QUIT:
                terminar()
            elif evento.type == KEYDOWN:
                if evento.key == K_ESCAPE:
                    terminar()
            elif evento.type == MOUSEBUTTONDOWN:
                if rectangulo_1.collidepoint(evento.pos):
                    return 1
                elif rectangulo_2.collidepoint(evento.pos):
                    return 2
                if rectangulo_3:
                    if rectangulo_3.collidepoint(evento.pos):
                        return 3
                                        
pantalla_inicio = pantalla_fin                
                           
                
    