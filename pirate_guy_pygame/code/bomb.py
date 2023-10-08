from support import import_folder
import pygame
from settings import *

class Base(pygame.sprite.Sprite):
    def __init__(self,pos,size,surface) -> None:
        super().__init__()
        x=pos[0]+size[0]/2
        y=pos[1]+size[1]/2
        self.display_surface=surface
        self.image=pygame.Surface(size)
        self.rect=self.image.get_rect(center=(x,y))
        self.direction=pygame.math.Vector2(0,0)

        self.damge=0

    def check_inside(self):
        if self.rect.x > screen_width*1.5 or self.rect.x < - screen_width*0.5:
            self.kill()

    def update(self, shift) -> None:
        self.rect.x+=shift
        self.rect.x+=self.direction.x
        self.check_inside()

class Bomb(pygame.sprite.Sprite):
    def __init__(self,pos,size,surface,direction) -> None:
        super().__init__()
        self.display_surface=surface
        self.frames=import_folder("../Assets/7-Objects/1-BOMB/2-Bomb On")
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect=self.image.get_rect(center=pos)
        self.mask=None
        self.direction=pygame.math.Vector2(20,1)
        self.gravity=0.5

        self.damge=200

    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y


    def animate(self):
        self.frame_index += 0.15
        if self.frame_index >= len(self.frames):
            self.frame_index=0
        self.image = self.frames[int(self.frame_index)]
        self.mask=pygame.mask.from_surface(self.image)


    def update(self, shift) -> None:
        self.animate()
        self.rect.x+=shift

class CannonBall(Base):
    def __init__(self,pos,size,surface,direction) -> None:
        super().__init__(pos,size,surface)
        self.image=pygame.image.load("../Assets/7-Objects/16-Enemy-Cannon/Cannon Ball/1.png").convert_alpha()
        self.rect.y-=15
        self.rect.x-=5
        self.damage=25
        self.direction.x=-3
        self.direction.x*=direction

class Bullet(Base):
    def __init__(self, pos, size, surface,direction) -> None:
        super().__init__(pos, size, surface)
        self.image=pygame.image.load("../Assets/bullet.png").convert_alpha()
        self.image=pygame.transform.scale(self.image,size)
        if direction < 0:
            self.image=pygame.transform.flip(self.image,True,False)
        self.rect.y-=15
        self.rect.x-=5
        self.damage=50
        self.direction.x=9
        self.direction.x*=direction
        