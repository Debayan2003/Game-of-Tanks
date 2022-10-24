import pygame, os

class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, size, speed):
        pygame.sprite.Sprite.__init__(self)
        
        self.images = []

        if size == 'SB':
            IMAGES = ['SB1.png','SB2.png','SB3.png','SB4.png','SB5.png','SB6.png']
            for i in IMAGES:
                BLAST_LOAD = pygame.transform.scale(pygame.image.load(os.path.join('Assets', i)), (130, 85))
                self.images.append(BLAST_LOAD)
        
        elif size == 'BB':
            IMAGES = ['BB1.png','BB2.png','BB3.png','BB4.png','BB5.png','BB6.png','BB7.png','BB8.png','BB9.png']
            for i in IMAGES:
                BLAST_LOAD = pygame.transform.scale(pygame.image.load(os.path.join('Assets', i)), (250, 220))
                self.images.append(BLAST_LOAD)

        elif size == 'RMB':
            IMAGES = ['MB1.png','MB2.png','MB3.png','MB4.png']
            for i in IMAGES:
                BLAST_LOAD = pygame.transform.flip(pygame.transform.scale(pygame.image.load(os.path.join('Assets', i)), (90, 50)), True, False)
                self.images.append(BLAST_LOAD)

        elif size == 'BMB':
            IMAGES = ['MB1.png','MB2.png','MB3.png','MB4.png']
            for i in IMAGES:
                BLAST_LOAD = pygame.transform.scale(pygame.image.load(os.path.join('Assets', i)), (90, 50))
                self.images.append(BLAST_LOAD)

        elif size == 'TB':
            IMAGES = ['TB1.png','TB2.png','TB3.png','TB4.png','TB5.png','TB6.png','TB7.png','TB8.png']
            for i in IMAGES:
                BLAST_LOAD = pygame.transform.scale(pygame.image.load(os.path.join('Assets', i)), (125, 90))
                self.images.append(BLAST_LOAD)
        
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.counter = 0
        self.explosion_speed = speed

    def update(self):
        self.counter += 1

        if self.counter >= self.explosion_speed and self.index < len(self.images) - 1:
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]

        if self.index >= len(self.images) - 1 and self.counter >= self.explosion_speed:
            self.kill()


