import pygame
from random import randrange
from config import *
from pygame.locals import *
from pygame import surface,font

pygame.init()
# FUNCION COLORES RANDOMS
def color_random() ->tuple:
    from random import randrange
    r = randrange(256)
    g = randrange(256)
    b = randrange(256)
    return(r , g , b)

#FUNCION CREAR LOS BOTONES DEL MENU
def crear_boton(pantalla:pygame.surface, texto:str, color_font:tuple, recta_btn:pygame.Rect, bg_color: tuple, 
                bg_color_hover:tuple = False,fuente = pygame.font.Font(None,36)):
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
    return (recta_1.x - recta_2.x , recta_1.y - recta_2.y)

# CREA TEXTO CON JUNTO CON SU UBICACION
def mostrar_texto (pantalla:surface, texto:str, fuente:font = pygame.font.Font(None,40), coordenadas:tuple = (100,100)
                   , color_texto:tuple = (negro), color_fondo:tuple = None):
    superficie_texto = fuente.render(texto, True, color_texto, color_fondo)
    rectangulo_texto = superficie_texto.get_rect(center = coordenadas)
    pantalla.blit(superficie_texto, rectangulo_texto)

# CREA UN DISPARO Y SU VELOCIDAD
def crear_disparo(mid_bottom:int ,velocidad:int = 5 ) -> dict:
    return {"recta":pygame.Rect(mid_bottom[0] + 17, mid_bottom[1] - 8, 6, 16),"speed":velocidad, "color":amarillo}

# CREA AL PERSONAJE PRINCILA Y SU RESPAWN
def personaje_principal(imagen:surface, pantalla:surface) -> dict: 
    recta = imagen.get_rect(center = (pantalla.get_width() // 2 ,pantalla.get_height() - imagen.get_height() // 2))
    mascara= pygame.mask.from_surface(imagen)
    return {"recta":recta, "mascara":mascara, "imagen":imagen}

# CREA UN ZOMBIE Y SU CORDENADA DE RESPAWN
def crear_zombie(imagen:pygame.surface , x:int , y:int,vida:int = 0) -> dict:  
    recta = imagen.get_rect(center = (x , y))
    mascara = pygame.mask.from_surface(imagen)
    return {"recta":recta, "mascara":mascara, "imagen":imagen, "vida":vida}

# CREAR UN BOTIQUIN Y SU RESPAWN ALEATORIO
def crear_botiquin(imagen:pygame.surface, pantalla:pygame.surface) -> dict:
    return crear_zombie(imagen,randrange(imagen.get_width() // 2, pantalla.get_width() - imagen.get_width() // 2),
                        randrange(imagen.get_height() // 2,pantalla.get_height() - imagen.get_height() // 2),)

#AÑADE A LA LISTA DICCIONARIOS DE ZOMBIES PARA Q SE CARGEN Y APAREZCAN
def crear_orda_zombies(lista:list , cantidad:int, imagen:pygame.surface , pantalla:pygame.surface , vida:int):
    for zombies in range(0,cantidad):
        lista.append(crear_zombie(imagen, 
                                  (randrange(imagen.get_width() // 2 ,pantalla.get_width() - imagen.get_width() // 2))
                                  ,randrange(-1500,-300),vida))
        
# TERMINA EL PROGAMA Y CIERRA PYGAME
def terminar():
    pygame.quit()
    exit()

#PAUSA EL PROGAMA HASTA Q PRESIONE UNA TECLA                    
def pausa_tutorial():
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

#FUNCION CREAR LOS BOTONES DEL MENU
def crear_boton(pantalla:pygame.surface, texto:str, color_font:tuple, recta_btn:Rect, bg_color: tuple, 
                bg_color_hover:tuple = False,fuente = pygame.font.Font(None,36)):
    
    if not bg_color_hover:
        bg_color_hover = bg_color
    render = fuente.render(texto,True,color_font)
    recta_txt = render.get_rect(center = recta_btn.center)
    if recta_txt.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(pantalla,bg_color_hover,recta_btn,border_radius = 5)
    else:
        pygame.draw.rect(pantalla,bg_color,recta_btn,border_radius = 5)    
    pantalla.blit(render,recta_txt)

#PANTALLA FINAL DEL JUEGO                    
def pantalla_fin(rectangulo_1:Rect, rectangulo_2:Rect , rectangulo_3:Rect = None):
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
                           
                
    