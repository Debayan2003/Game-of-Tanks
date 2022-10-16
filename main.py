import pygame
import os
import button
pygame.init()

winfo = pygame.display.Info()
WIDTH, HEIGHT = winfo.current_w, winfo.current_h

WIN = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("GAME OF TANKS")

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
CUSTOM = (238, 118, 0)

BORDER = pygame.Rect((WIDTH/2) - 5, 0, 10, HEIGHT)

HEALTH_FONT = pygame.font.SysFont('cooper black', 40)
WINNER_FONT1 = pygame.font.SysFont('cooper black', 100)
WINNER_FONT2 = pygame.font.SysFont('cooper black', 105)

FPS = 60
VEL = 8
BULLET_VEL = 16
MAX_BULLETS = 3
TANK_WIDTH, TANK_HEIGHT = 220, 140

RED_HIT = pygame.USEREVENT + 1
BLUE_HIT = pygame.USEREVENT + 2

hw, hh = 50, 40
HEALTH = pygame.transform.scale(pygame.image.load(os.path.join('Python Programs\Games\Game of Tanks\Assets', 'Health.png')), (hw, hh))

START = pygame.transform.scale(pygame.image.load(os.path.join('Python Programs\Games\Game of Tanks\Assets', 'Start.png')), (200, 160))
START_REC = button.Button((WIDTH/2)-100, ((HEIGHT*3)/4)+30, START, 1)

INITIAL = pygame.transform.scale(pygame.image.load(os.path.join('Python Programs\Games\Game of Tanks\Assets', 'Initial.png')), (WIDTH, HEIGHT))

RED_TANK = pygame.transform.scale(pygame.image.load(os.path.join('Python Programs\Games\Game of Tanks\Assets', 'tank1.png')), (TANK_WIDTH, TANK_HEIGHT))

T1TINT = pygame.transform.scale(pygame.image.load(os.path.join('Python Programs\Games\Game of Tanks\Assets', 't1tint.png')), (TANK_WIDTH, TANK_HEIGHT))

BLUE_TANK = pygame.transform.scale(pygame.image.load(os.path.join('Python Programs\Games\Game of Tanks\Assets', 'tank2.png')), (TANK_WIDTH, TANK_HEIGHT))

T2TINT = pygame.transform.scale(pygame.image.load(os.path.join('Python Programs\Games\Game of Tanks\Assets', 't2tint.png')), (TANK_WIDTH, TANK_HEIGHT))

GROUND = pygame.transform.scale(pygame.image.load(os.path.join('Python Programs\Games\Game of Tanks\Assets', 'MainGround.jpg')), (WIDTH, HEIGHT))

BLACKBG = pygame.transform.scale(pygame.image.load(os.path.join('Python Programs\Games\Game of Tanks\Assets', 'BlackBG.jpg')), (WIDTH, HEIGHT))

ALPHA = pygame.transform.scale(pygame.image.load(os.path.join('Python Programs\Games\Game of Tanks\Assets', 'Alpha.png')), (8*hw, hh))

BRAVO = pygame.transform.scale(pygame.image.load(os.path.join('Python Programs\Games\Game of Tanks\Assets', 'Bravo.png')), (8*hw, hh))

ALPHA_WIN = pygame.transform.scale(pygame.image.load(os.path.join('Python Programs\Games\Game of Tanks\Assets', 'AlphaWin.png')), (20*hw, 2*hh))

BRAVO_WIN = pygame.transform.scale(pygame.image.load(os.path.join('Python Programs\Games\Game of Tanks\Assets', 'BravoWin.png')), (20*hw, 2*hh))

def draw_window(blue, red, blue_bullets, red_bullets, blue_health, red_health, t1, t2):
    x = 10

    WIN.blit(GROUND, (0, 0))
    pygame.draw.rect(WIN, CUSTOM, BORDER)

    WIN.blit(ALPHA, (hw*11/4, 10))
    for i in range(red_health):
        WIN.blit(HEALTH, (ALPHA.get_width() + (i+11/4)*hw + x, x))
    
    WIN.blit(BRAVO, ((WIDTH/2) + hw*3 , 10))
    for i in range(blue_health):
        WIN.blit(HEALTH, ((WIDTH/2) + BRAVO.get_width() + (i+3)*hw + x, x))

    if t1 > 0:
        WIN.blit(T1TINT, (red.x, red.y))
    else:
        WIN.blit(RED_TANK, (red.x, red.y))

    if t2 > 0:
        WIN.blit(T2TINT, (blue.x, blue.y))
    else:
        WIN.blit(BLUE_TANK, (blue.x, blue.y))

    for bullet in blue_bullets:
        pygame.draw.circle(WIN, WHITE, (bullet.x, bullet.y), 12, 0)
        pygame.draw.circle(WIN, BLUE, (bullet.x, bullet.y), 10, 0)

    for bullet in red_bullets:
        pygame.draw.circle(WIN, WHITE, (bullet.x, bullet.y), 12, 0)
        pygame.draw.circle(WIN, RED, (bullet.x, bullet.y), 10, 0)

    pygame.display.update()

def red_handle_movement(keys_pressed, red, t1):
    v = VEL
    if t1 > 0:
        v = (VEL/2)
    if keys_pressed[pygame.K_a] and red.x - v > 0:  
        red.x -= v
    if keys_pressed[pygame.K_d] and red.x + v + red.width < BORDER.x:  
        red.x += v
    if keys_pressed[pygame.K_w] and red.y - v > 60: 
        red.y -= v
    if keys_pressed[pygame.K_s] and red.y + v + red.height < HEIGHT: 
        red.y += v

def blue_handle_movement(keys_pressed, blue, t2):
    v = VEL
    if t2 > 0:
        v = (VEL/2)
    if keys_pressed[pygame.K_LEFT] and blue.x - v > BORDER.x + BORDER.width: 
        blue.x -= v
    if keys_pressed[pygame.K_RIGHT] and blue.x + v + blue.width < WIDTH:  
        blue.x += v
    if keys_pressed[pygame.K_UP] and blue.y - v > 60: 
        blue.y -= v
    if keys_pressed[pygame.K_DOWN] and blue.y + v + blue.height < HEIGHT:  
        blue.y += v

def handle_bullets(red_bullets, blue_bullets, red, blue):
    for bullet in red_bullets:
        bullet.x += BULLET_VEL
        if blue.colliderect(bullet):
            pygame.event.post(pygame.event.Event(BLUE_HIT))
            red_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            red_bullets.remove(bullet)

    for bullet in blue_bullets:
        bullet.x -= BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            blue_bullets.remove(bullet)
        elif bullet.x < 0:
            blue_bullets.remove(bullet)

def draw_winner(winner):
    BLACKBG.set_alpha(230)
    WIN.blit(BLACKBG, (0, 0))
    if winner == 1:
        WIN.blit(ALPHA_WIN, ((WIDTH/2) - 10*hw, (HEIGHT/2) - hw))
    else :
        WIN.blit(BRAVO_WIN, ((WIDTH/2) - 10*hw, (HEIGHT/2) - hw))
    pygame.display.update()
    pygame.time.delay(3000)

def main():
    red = pygame.Rect((WIDTH/6), (HEIGHT/2), TANK_WIDTH, TANK_HEIGHT)
    blue = pygame.Rect((WIDTH*3/4), (HEIGHT/2), TANK_WIDTH, TANK_HEIGHT)

    blue_bullets = []
    red_bullets = []

    blue_health = 5
    red_health = 5

    clock = pygame.time.Clock()

    t1 = t2 = 0
    run = True
    while run:
        WIN.blit(INITIAL, (0, 0))
        if START_REC.draw(WIN):
            WIN.blit(GROUND, (0, 0))
            run = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                    pygame.quit()

        pygame.display.update()

    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                    pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x + red.width, red.y + red.height//2 - 60, 20, 10)
                    red_bullets.append(bullet)

                if event.key == pygame.K_RCTRL and len(blue_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(blue.x, blue.y + blue.height//2 - 60, 20, 10)
                    blue_bullets.append(bullet)

            if event.type == RED_HIT:
                red_health -= 1
                t1 += 1

            if event.type == BLUE_HIT:
                blue_health -= 1
                t2 += 1

        keys_pressed = pygame.key.get_pressed()
        red_handle_movement(keys_pressed, red, t1)
        blue_handle_movement(keys_pressed, blue, t2)

        handle_bullets(red_bullets, blue_bullets, red, blue)

        draw_window(blue, red, blue_bullets, red_bullets, blue_health, red_health, t1, t2)

        if 0 < t1 <= 20:
            t1 += 1
        else:
            t1 = 0
        
        if 0 < t2 <= 20:
            t2 += 1
        else:
            t2 = 0

        winner = 0 
        if blue_health <= 0:
            winner = 1

        if red_health <= 0:
            winner = 2

        if winner != 0:
            draw_winner(winner)
            break

if __name__ == "__main__":
    main()