import pygame 
from player import Human
from random import randint
from support import import_folder

class Enemy(Human):
	def __init__(self,pos,surface,health,attack_power,speed,assets_path,animations_list):
		super().__init__(pos,surface,assets_path,animations_list)
		self.speed = speed
		self.health=health
		self.max_health=health
		self.attack_power=attack_power
		self.direction=pygame.math.Vector2(1,0)
		self.rect.width=64
		self.rect.height=64
		self.health_bar_frames=import_folder("../Assets/7-Objects/Enemy_health_bar")
		

	def get_status(self):
		if self.hit:
			self.status="Hit"
		else:
			self.status="Run"

		
		if self.direction.x < 0:
			self.facing_right=False
		elif self.direction.x > 0:
			self.facing_right=True
		
	def show_health(self):
		health_retio=self.health/self.max_health
		frame_index=int(health_retio*(len(self.health_bar_frames)-1))
		bar=self.health_bar_frames[frame_index]
		pos=(self.rect.x,self.rect.y-10)
		self.display_surface.blit(bar,pos)

	def move(self):
		self.rect.x +=self.direction.x *self.speed


	def reverse(self):
		self.direction.x *= -1

	def update(self,shift):
		self.rect.x += shift
		self.animate()
		self.move()
		self.get_status()
		self.animate()
		self.show_health()
		self.invincibility_timer()