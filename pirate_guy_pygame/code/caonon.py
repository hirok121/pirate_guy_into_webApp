import pygame
from support import import_folder
from game_data import canon_assets_path,canon_animations_list
from particles import ParticleEffect


class Canon(pygame.sprite.Sprite):
	
    def __init__(self,pos,flip,surface,canon_assets_path,animations_list):
        super().__init__()
        self.canon_assets_path=canon_assets_path
        self.animations_list=animations_list
        self.animations=self.import_canon_assets(self.canon_assets_path,self.animations_list)
        self.frame_index = 0
        self.animation_speed=0.15
        self.image=pygame.Surface((62,46))
        self.rect = self.image.get_rect(bottomleft = (pos))
        self.status="Idle"
        self.health=500
        self.max_health=500
        self.health_bar_frames=import_folder("../Assets/7-Objects/Enemy_health_bar")
        self.flip=flip
        self.display_surface=surface

        ## shooting machanism
        self.shoot_ready=True
        self.reload_time=4000
        self.shoot_time=0

    def animate(self):
        animation=self.animations[self.status]

        self.frame_index += 0.15
        if self.frame_index >= len(animation):
            self.frame_index = 0
            if self.status=="Attack":
                self.status="Idle"

        if self.flip:
            self.image=pygame.transform.flip( animation[int(self.frame_index)%len(animation)],True,False)
        else:
            self.image = animation[int(self.frame_index)%len(animation)]
        
    def get_status(self):
        pass
        
    def shoot(self):
        if self.shoot_ready:
            self.status="Attack"
            self.shoot_time=pygame.time.get_ticks()
            self.shoot_ready=False
    
    def reloading(self):
        current_time=pygame.time.get_ticks()
        if current_time -  self.shoot_time >= self.reload_time:
            self.shoot_ready=True

    def get_hit(self,amount):
        self.health-=amount
    
    def show_health(self):
        health_retio=self.health/self.max_health
        frame_index=int(health_retio*(len(self.health_bar_frames)-1))
        bar=self.health_bar_frames[frame_index]
        pos=(self.rect.x,self.rect.y-10)
        self.display_surface.blit(bar,pos)

    def import_canon_assets(self,assets_path,animations_list):
        character_path = assets_path
        animations = {}

        for animation in animations_list:
            full_path = character_path + animation
            animations[animation] = import_folder(full_path)
        
        return animations

    def update(self,shift):
        self.rect.x += shift
        self.get_status()
        self.animate()
        self.show_health()
        self.reloading()