import pygame, os, button, blast
pygame.init()

WINFO = pygame.display.Info()
WIDTH, HEIGHT = WINFO.current_w, WINFO.current_h

WIN = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("GAME OF TANKS")

RED_HIT = pygame.USEREVENT + 1
BLUE_HIT = pygame.USEREVENT + 2
EXPLOSION_GROUP = pygame.sprite.Group() 

FPS = 60
MAX_BULLETS = 3
BW, BH = 110, 25
HW, HH = 50, 40
VEL, BULLET_VEL = 8, 20
TANK_WIDTH, TANK_HEIGHT = 220, 140

HEALTH = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'Health.png')), (HW, HH))

START = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'Start.png')), (200, 160))
START_REC = button.Button((WIDTH/2)-100, ((HEIGHT*3)/4)+30, START, 1)

INITIAL = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'Initial.png')), (WIDTH, HEIGHT))

RED_TANK = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'Tank1.png')), (TANK_WIDTH, TANK_HEIGHT))
RED_TANK_MASK = pygame.mask.from_surface(RED_TANK)

T1TINT = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'T1Tint.png')), (TANK_WIDTH, TANK_HEIGHT))

BLUE_TANK = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'Tank2.png')), (TANK_WIDTH, TANK_HEIGHT))
BLUE_TANK_MASK = pygame.mask.from_surface(BLUE_TANK)

T2TINT = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'T2Tint.png')), (TANK_WIDTH, TANK_HEIGHT))

GROUND = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'MainGround.png')), (WIDTH, HEIGHT))

BLACKBG = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'BlackBG.png')), (WIDTH, HEIGHT))

ALPHA = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'Alpha.png')), (8*HW, HH))

BRAVO = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'Bravo.png')), (8*HW, HH))

ALPHA_WIN = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'AlphaWin.png')), (20*HW, 2*HH))

BRAVO_WIN = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'BravoWin.png')), (20*HW, 2*HH))

OVER_RED = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'OverRed.png')), (16*HW, 2.25*HH))

OVER_BLUE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'OverBlue.png')), (16*HW, 2.25*HH))

RED_BULLET = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'RedBullet.png')), (BW, BH))
RED_BULLET_MASK = pygame.mask.from_surface(RED_BULLET)

BLUE_BULLET = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'BlueBullet.png')), (BW, BH))
BLUE_BULLET_MASK = pygame.mask.from_surface(BLUE_BULLET)

CLICK = pygame.mixer.Sound(os.path.join('Assets', 'Click.mp3'))

BLAST = pygame.mixer.Sound(os.path.join('Assets', 'Blast.mp3'))

TANK_BLAST = pygame.mixer.Sound(os.path.join('Assets', 'TankBlast.mp3'))

BIG_BLAST = pygame.mixer.Sound(os.path.join('Assets', 'BigBlast.mp3'))

SHOT = pygame.mixer.Sound(os.path.join('Assets', 'Shot.mp3'))

INTRO = pygame.mixer.Sound(os.path.join('Assets', 'Intro.mp3'))
INTRO.set_volume(0.6)
 
INGAME = pygame.mixer.Sound(os.path.join('Assets', 'InGame.mp3'))
INGAME.set_volume(0.6)

OUTRO = pygame.mixer.Sound(os.path.join('Assets', 'Outro.mp3'))
OUTRO.set_volume(0.6)

def draw_window(blue, red, blue_bullets, red_bullets, blue_health, red_health, t1, t2):
    WIN.blit(GROUND, (0, 0))

    x = (((WIDTH/2) - 13*HW)/2)
    WIN.blit(ALPHA, (x, 10))
    for i in range(red_health):
        WIN.blit(HEALTH, (x + ALPHA.get_width() + i*HW + 10, 10))

    x = x + (WIDTH/2)
    WIN.blit(BRAVO, (x , 10))
    for i in range(blue_health):
        WIN.blit(HEALTH, (x + BRAVO.get_width() + i*HW + 10, 10))

    if red_health == 0:
       WIN.blit(BLUE_TANK, (blue.x, blue.y))
    elif blue_health == 0:
       WIN.blit(RED_TANK, (red.x, red.y))
    else:
        if t1 > 0:
            WIN.blit(T1TINT, (red.x, red.y))
        else:
            WIN.blit(RED_TANK, (red.x, red.y))

        if t2 > 0:
            WIN.blit(T2TINT, (blue.x, blue.y))
        else:
            WIN.blit(BLUE_TANK, (blue.x, blue.y))

    for bullet in blue_bullets:
        WIN.blit(BLUE_BULLET, (bullet.x, bullet.y))

    for bullet in red_bullets:
        WIN.blit(RED_BULLET, (bullet.x, bullet.y))

    EXPLOSION_GROUP.update()
    EXPLOSION_GROUP.draw(WIN)

    pygame.display.update()

def red_handle_movement(keys_pressed, red, t1):
    v = VEL
    if t1 > 0:
        v = (VEL/2)
    if keys_pressed[pygame.K_a] and red.x - v > 0:  
        red.x -= v
    if keys_pressed[pygame.K_d] and red.x + v + red.width < ((WIDTH/2) - 100):  
        red.x += v
    if keys_pressed[pygame.K_w] and red.y - v > ((HEIGHT/4) + 20): 
        red.y -= v
    if keys_pressed[pygame.K_s] and red.y + v + red.height < HEIGHT: 
        red.y += v

def blue_handle_movement(keys_pressed, blue, t2):
    v = VEL
    if t2 > 0:
        v = (VEL/2)
    if keys_pressed[pygame.K_LEFT] and blue.x - v > ((WIDTH/2) + 100): 
        blue.x -= v
    if keys_pressed[pygame.K_RIGHT] and blue.x + v + blue.width < WIDTH:  
        blue.x += v
    if keys_pressed[pygame.K_UP] and blue.y - v > ((HEIGHT/4) + 20): 
        blue.y -= v
    if keys_pressed[pygame.K_DOWN] and blue.y + v + blue.height < HEIGHT:  
        blue.y += v

def handle_bullets(red_bullets, blue_bullets, red, blue, red_health, blue_health):
    for bullet in red_bullets:
        bullet.x += BULLET_VEL
        if RED_BULLET_MASK.overlap(BLUE_TANK_MASK, (blue.x - bullet.x, blue.y - bullet.y)):
            pygame.event.post(pygame.event.Event(BLUE_HIT))
            TANK_BLAST.play()
            if blue_health > 1:
                explosion = blast.Explosion(bullet.x + BW, bullet.y, 'TB', 2)  
                EXPLOSION_GROUP.add(explosion)
            else:
                TANK_BLAST.stop()
                EXPLOSION_GROUP.empty()
            red_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            red_bullets.remove(bullet)
        else :
            for col in blue_bullets:
                if RED_BULLET_MASK.overlap(BLUE_BULLET_MASK, (col.x - bullet.x, col.y - bullet.y)):
                    BLAST.play()
                    red_bullets.remove(bullet)   
                    blue_bullets.remove(col)
                    explosion = blast.Explosion(col.x, col.y + 10, 'SB', 2)  
                    EXPLOSION_GROUP.add(explosion)
                    break              

    for bullet in blue_bullets:
        bullet.x -= BULLET_VEL
        if BLUE_BULLET_MASK.overlap(RED_TANK_MASK, (red.x - bullet.x, red.y - bullet.y)):
            pygame.event.post(pygame.event.Event(RED_HIT))
            TANK_BLAST.play()
            if red_health > 1:
                explosion = blast.Explosion(bullet.x, bullet.y, 'TB', 2)  
                EXPLOSION_GROUP.add(explosion)
            else:
                TANK_BLAST.stop()
                EXPLOSION_GROUP.empty()
            blue_bullets.remove(bullet)
        elif bullet.x < -BW:
            blue_bullets.remove(bullet)
        else:
            for col in red_bullets:
                if RED_BULLET_MASK.overlap(BLUE_BULLET_MASK, (col.x - bullet.x, col.y - bullet.y)):
                    BLAST.play()
                    red_bullets.remove(col)   
                    blue_bullets.remove(bullet)
                    explosion = blast.Explosion(bullet.x, bullet.y + 10, 'SB', 2)  
                    EXPLOSION_GROUP.add(explosion)
                    break 
    
def draw_winner(winner):
    BLACKBG.set_alpha(230)
    WIN.blit(BLACKBG, (0, 0))

    INGAME.stop()
    pygame.time.delay(300)
    OUTRO.play()

    if winner == 1:
        WIN.blit(OVER_BLUE, ((WIDTH/2) - 8*HW, (HEIGHT/4)))
        WIN.blit(ALPHA_WIN, ((WIDTH/2) - 10*HW, (HEIGHT/2)))
    else :
        WIN.blit(OVER_RED, ((WIDTH/2) - 8*HW, (HEIGHT/4)))
        WIN.blit(BRAVO_WIN, ((WIDTH/2) - 10*HW, (HEIGHT/2)))

    pygame.display.update()
    pygame.time.delay(5500)

def main():
    red = pygame.Rect((WIDTH/6), (HEIGHT/2), TANK_WIDTH, TANK_HEIGHT)
    blue = pygame.Rect((WIDTH*3/4), (HEIGHT/2), TANK_WIDTH, TANK_HEIGHT)

    blue_bullets = []
    red_bullets = []

    blue_health = red_health = 5
    t1 = t2 = 0

    clock = pygame.time.Clock()

    INTRO.play(-1)

    run = True 
    while run:
        WIN.blit(INITIAL, (0, 0))

        if START_REC.draw(WIN):
            CLICK.play()
            INTRO.stop()
            INGAME.play(-1)
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
                    bullet = pygame.Rect(red.x + red.width, red.y + red.height/2 - 70, BW, BH)
                    red_bullets.append(bullet)
                    explosion = blast.Explosion(red.x + TANK_WIDTH + 10, red.y + 10, 'RMB', 2)  
                    EXPLOSION_GROUP.add(explosion)
                    SHOT.play()

                if event.key == pygame.K_RCTRL and len(blue_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(blue.x - BW, blue.y + blue.height/2 - 70, BW, BH)
                    blue_bullets.append(bullet)
                    explosion = blast.Explosion(blue.x - 10, blue.y + 10, 'BMB', 2)  
                    EXPLOSION_GROUP.add(explosion)
                    SHOT.play()

            if event.type == RED_HIT:
                red_health -= 1
                t1 += 1

            if event.type == BLUE_HIT:
                blue_health -= 1
                t2 += 1

        keys_pressed = pygame.key.get_pressed()

        red_handle_movement(keys_pressed, red, t1)

        blue_handle_movement(keys_pressed, blue, t2)

        handle_bullets(red_bullets, blue_bullets, red, blue, red_health, blue_health)

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
        if blue_health == 0:
            explosion = blast.Explosion(blue.x + 2*HW, blue.y + HH/4, 'BB', 3)  
            EXPLOSION_GROUP.add(explosion)
            red_bullets = []
            blue_bullets = []
            BIG_BLAST.play()
            for i in range(30):
                draw_window(blue, red, blue_bullets, red_bullets, blue_health, red_health, t1, t2)            
            winner = 1

        if red_health == 0:
            explosion = blast.Explosion(red.x + 2*HW, red.y + HH/4, 'BB', 3)  
            EXPLOSION_GROUP.add(explosion)
            red_bullets = []
            blue_bullets = []
            BIG_BLAST.play()
            for i in range(30):
                draw_window(blue, red, blue_bullets, red_bullets, blue_health, red_health, t1, t2)
            winner = 2

        if winner != 0:
            draw_winner(winner)
            break
    
    main()

try:
    if __name__ == "__main__":
        main()
except pygame.error: 
    pass
