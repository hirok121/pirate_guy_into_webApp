import pygame 
from support import import_folder
from math import sin
from particles import ParticleEffect

class Human(pygame.sprite.Sprite):
	def __init__(self,pos,surface,assets_path,animations_list,speed=8):
		super().__init__()
		self.assets_path=assets_path
		self.animations_list=animations_list
		self.import_character_assets(self.assets_path,self.animations_list)
		self.frame_index = 0
		self.animation_speed = 0.15
		self.image = self.animations[self.animations_list[0]][self.frame_index]
		self.rect = self.image.get_rect(topleft = pos)
		self.display_surface = surface

		# attact_power
		self.attack_power=25

		# health management
		self.hit=False
		self.invincibility_duration = 500
		self.invincible = False
		self.hurt_time = 0

		# player movement
		self.direction = pygame.math.Vector2(0,0)
		self.C_SPEED=speed
		self.speed = self.C_SPEED

		# status
		self.status = self.animations_list[0]
		self.facing_right = True

		self.hit_sound = pygame.mixer.Sound('../Assets/audio/effects/hit.wav')



	def get_hit(self,amount):
		if not self.invincible:
			self.health-=amount
			self.hit=True
			self.invincible = True
			self.hurt_time = pygame.time.get_ticks()
			self.hit_sound.play()

	def invincibility_timer(self):
		if self.invincible:
			current_time = pygame.time.get_ticks()
			if current_time - self.hurt_time >= self.invincibility_duration:
				self.invincible = False
				self.hit=False
	
	def import_character_assets(self,assets_path,animations_list):
		character_path = assets_path
		self.animations = {}

		for animation in animations_list:
			full_path = character_path + animation
			self.animations[animation] = import_folder(full_path)

	def animate(self):
		animation = self.animations[self.status]

		# loop over frame index 
		self.frame_index += self.animation_speed
		if self.frame_index >= len(animation):
			self.frame_index = 0
			if self.status=="Attack":
				self.status="Run"

		image = animation[int(self.frame_index)% len(animation)]
		if self.facing_right:
			self.image = image
		else:
			flipped_image = pygame.transform.flip(image,True,False)
			self.image = flipped_image

class Player(Human):
	def __init__(self,pos,surface,assets_path,animations_list):
		super().__init__(pos,surface,assets_path,animations_list )
		
		# dust particles 
		self.import_dust_run_particles()
		self.dust_frame_index = 0
		self.dust_animation_speed = 0.15
		self.dust_particles=pygame.sprite.Group()
		self.invincibility_duration=750

		# player movement
		self.gravity = 0.8
		self.jump_speed = -20

		#jump
		self.jupm_count=0

		# player status
		self.on_ground = False
		self.on_ceiling = False
		self.on_left = False
		self.on_right = False

		# health management
		self.health=300
		self.max_health=300
		self.health_bar = pygame.image.load('../Assets/7-Objects/health_bar.png').convert_alpha()
		self.health_bar_topleft = (54,39)
		self.bar_max_width = 152
		self.bar_height = 4

		# audio 
		self.jump_sound = pygame.mixer.Sound('../Assets/audio/effects/hit.wav')
		self.jump_sound.set_volume(0.5)
		self.hit_sound = pygame.mixer.Sound('../Assets/audio/effects/hit.wav')

	def show_health(self,current,full):
		self.display_surface.blit(self.health_bar,(20,10))
		current_health_ratio = current / full
		current_bar_width = self.bar_max_width * current_health_ratio
		health_bar_rect = pygame.Rect(self.health_bar_topleft,(current_bar_width,self.bar_height))
		pygame.draw.rect(self.display_surface,'#dc4949',health_bar_rect)

	def import_dust_run_particles(self):
		self.dust_run_particles = import_folder('../Assets/1-Player-Bomb Guy/13-Run Particles')
	
	def run_dust_animation(self):
		if self.status == 'run' and self.on_ground:
			self.dust_frame_index += self.dust_animation_speed
			if self.dust_frame_index >= len(self.dust_run_particles):
				self.dust_frame_index = 0

			dust_particle = self.dust_run_particles[int(self.dust_frame_index)]

			if self.facing_right:
				pos = self.rect.bottomleft - pygame.math.Vector2(6,10)
				self.display_surface.blit(dust_particle,pos)
			else:
				pos = self.rect.bottomright - pygame.math.Vector2(6,10)
				flipped_dust_particle = pygame.transform.flip(dust_particle,True,False)
				self.display_surface.blit(flipped_dust_particle,pos)

	def get_input(self):
		keys = pygame.key.get_pressed()

		if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
			self.direction.x = 1
			self.facing_right = True
		elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
			self.direction.x = -1
			self.facing_right = False
		else:
			self.direction.x = 0

		if keys[pygame.K_SPACE] and self.on_ground:
			# self.jump()
			# jump=ParticleEffect((self.rect.x+30,self.rect.y+30),"jump")
			# self.dust_particles.add(jump)
			pass

	def get_status(self):
		if self.health <=0:
			self.status="dead_hit"
		elif self.hit:
			self.status="hit"
		elif self.direction.y < 0:
			self.status = 'jump'
		elif self.direction.y > 1:
			self.status = 'fall'
		else:
			if self.direction.x != 0:
				self.status = 'run'
			else:
				self.status = 'idle'

	def apply_gravity(self):
		self.direction.y += self.gravity
		self.rect.y += self.direction.y

	def rage(self):
		if self.health < self.max_health*0.5:
			self.attack_power=50

	def jump(self):
		if self.on_ground:
			self.jupm_count=0
		if self.jupm_count < 2:
			self.direction.y = self.jump_speed
			self.jump_sound.play()
			self.jupm_count+=1

	def update(self):
		if self.health > 0:
			self.get_input()
		self.get_status()
		self.animate()
		self.run_dust_animation()
		self.dust_particles.update(0)
		self.dust_particles.draw(self.display_surface)
		self.invincibility_timer()
		self.show_health(self.health,self.max_health)
		self.rage()
		