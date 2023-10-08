import pygame 
from support import import_csv_layout, import_cut_graphics
from settings import tile_size, screen_height, screen_width
from tiles import Tile, StaticTile, Object, Coin,AnimatedTile
from enemy import Enemy
from decoration import Sky, Water, Clouds
from player import Player
from particles import ParticleEffect
from game_data import *
from caonon import Canon
from bomb import CannonBall,Bullet

pygame.font.init()

class Level:
	def __init__(self,current_level,surface):

		# general setup
		self.display_surface = surface
		self.world_shift = 0
		self.current_x = None

		#font 
		self.font = pygame.font.SysFont('comicsans',30)
		
		# audio 
		self.coin_sound = pygame.mixer.Sound('../Assets/audio/effects/coin.wav')
		self.stomp_sound = pygame.mixer.Sound('../Assets/audio/effects/stomp.wav')
		self.canonexplo_sound = pygame.mixer.Sound('../Assets/audio/effects/explosion.mp3')
		self.canonexplo_sound.set_volume(0.3)
		self.gameOver_sound = pygame.mixer.Sound('../Assets/audio/game-over.mp3')
		self.level_bg_music = pygame.mixer.Sound('../Assets/audio/level_music.wav')
		self.level_bg_music.set_volume(0.3)
		self.level_bg_music.play(-1)

		#welcome
		self.welcome()
		self.game_status=True

		# level Data
		self.current_level = current_level
		level_data = levels[self.current_level]

		# player 
		player_layout = import_csv_layout(level_data['player'])
		self.player = pygame.sprite.GroupSingle()
		self.goal = pygame.sprite.GroupSingle()
		self.player_setup(player_layout)

		# dust 
		self.dust_sprite = pygame.sprite.GroupSingle()
		self.player_on_ground = False

		# explosion particles 
		self.explosion_sprites = pygame.sprite.Group()

		# terrain setup
		terrain_layout = import_csv_layout(level_data['terrain'])
		self.terrain_sprites = self.create_tile_group(terrain_layout,'terrain')

		# fg_ojbects 
		fg_objects_layout = import_csv_layout(level_data['fg_objects'])
		self.fg_objects_sprites = self.create_tile_group(fg_objects_layout,'fg_objects')

		# bg_ojbects 
		bg_objects_layout = import_csv_layout(level_data['bg_objects'])
		self.bg_objects_sprites = self.create_tile_group(bg_objects_layout,'bg_objects')

		# coins 
		coin_layout = import_csv_layout(level_data['coins'])
		self.coin_sprites = self.create_tile_group(coin_layout,'coins')

		# enemy 
		enemy_layout = import_csv_layout(level_data['enemies'])
		self.enemy_sprites = self.create_tile_group(enemy_layout,'enemies')

		#  constraint 
		constraint_layout = import_csv_layout(level_data['constraints'])
		self.constraint_sprites = self.create_tile_group(constraint_layout,'constraint')

		#canon
		canon_layout = import_csv_layout(level_data['canon'])
		self.canon_sprites = self.create_tile_group(canon_layout,'canon')

		# canono Ball
		self.canon_ball=pygame.sprite.Group()
		self.add_canono_ball_status=False

		#player shoot
		self.bullets=pygame.sprite.Group()

		self.collidable_sprites = self.terrain_sprites.sprites() + self.fg_objects_sprites.sprites() + self.canon_sprites.sprites()

		#coins show
		self.coin = pygame.image.load('../Assets/coin.png').convert_alpha()
		self.coin_rect = self.coin.get_rect(topleft = (50,61))
		self.coins=0

		#enemy count
		self.enemy = pygame.transform.scale(pygame.image.load('../Assets/5-Enemy-Captain/Idle/1.png').convert_alpha(),(40,50))
		self.enemy_rect = self.coin.get_rect(topleft = (45,93))
		self.font = pygame.font.SysFont('comicsans',30)

		#decoration
		self.clouds=Clouds(8,tile_size*150,40)

	def show_coins(self):
		self.display_surface.blit(self.coin,self.coin_rect)
		coin_amount_surf = self.font.render(str(self.coins),False,'#33323d')
		coin_amount_rect = coin_amount_surf.get_rect(midleft = (self.coin_rect.right + 4,self.coin_rect.centery))
		self.display_surface.blit(coin_amount_surf,coin_amount_rect)

	def show_enemy_count(self):
		enemy_count=len(self.enemy_sprites.sprites())
		self.display_surface.blit(self.enemy,self.enemy_rect)
		enemy_count_surf = self.font.render(str(enemy_count),True,'#33323d')
		enemy_count_rect = enemy_count_surf.get_rect(midleft = (self.enemy_rect.right + 4,self.enemy_rect.centery+10))
		self.display_surface.blit(enemy_count_surf,enemy_count_rect)

	def create_tile_group(self,layout,type):
		sprite_group = pygame.sprite.Group()

		for row_index, row in enumerate(layout):
			for col_index,val in enumerate(row):
				if val != '-1':
					x = col_index * tile_size
					y = row_index * tile_size

					if type == 'terrain':
						terrain_tile_list = import_cut_graphics('../Assets/8-Tile-Sets/Tile-Sets.png')
						tile_surface = terrain_tile_list[int(val)]
						if val in ['22','23','28','29']:
							sprite = StaticTile((tile_size,8),x,y,tile_surface)
						else :
							sprite = StaticTile((tile_size,tile_size),x,y,tile_surface)
						
					if type == 'fg_objects':
						if val=='0':
							sprite = Object((35,44),x,y,"../Assets/7-Objects/fg_objects/Barrel.png")
						if val=='1':
							sprite = Object((35,40),x,y,"../Assets/7-Objects/fg_objects/crate.png")

					if type == 'bg_objects':
						if val=='0':
							sprite = AnimatedTile((14,32),x,y,"../Assets/7-Objects/6-Candle/")
						if val=='1':
							sprite = Object((16,21),x,y,"../Assets/7-Objects/bg_objects/Blue Bottle.png")
						if val=='2':
							sprite = Object((32,56),x,y,"../Assets/7-Objects/bg_objects/Chair.png")
						
						if val=='3':
							sprite = Object((32,56),x,y,"../Assets/7-Objects/bg_objects/Chair_flip.png")
						
						if val=='4':
							sprite = Object((14,24),x,y,"../Assets/7-Objects/bg_objects/Green bottle.png")
						if val=='5':
							sprite = Object((16,31),x,y,"../Assets/7-Objects/bg_objects/Red bottle.png")
						if val=='6':
							sprite = Object((19,14),x,y,"../Assets/7-Objects/bg_objects/Skull.png")
						
						if val=='7':
							sprite = Object((80,32),x,y,"../Assets/7-Objects/bg_objects/Table.png")
							
						if val=='8':
							sprite = Object((58,61),x,y,"../Assets/7-Objects/bg_objects/Windows.png")
							
			

					if type == 'coins':
						if val == '1': sprite = Coin((tile_size,tile_size),x,y,'../Assets/7-Objects/coins/silver',1)
						if val == '0': sprite = Coin((tile_size,tile_size),x,y,'../Assets/7-Objects/coins/gold',5)

					if type == 'canon':
						if val == '0': sprite = Canon((x,y+tile_size),1,self.display_surface, canon_assets_path,canon_animations_list)
						if val == '1': sprite = Canon((x,y+tile_size),0,self.display_surface, canon_assets_path,canon_animations_list)

					if type == 'enemies':
						if val=="0":
							sprite = Enemy((x,y),self.display_surface,100,10,2,enemy_blad_pirate_assets_path,enemy_blad_pirate_animations_list)
						if val=="1":
							sprite = Enemy((x,y),self.display_surface,150,15,3,enemy_big_guy_assets_path,enemy_big_guy_animations_list)
						if val=="2":
							sprite = Enemy((x,y),self.display_surface,1000,20,4,enemy_captain_assets_path,enemy_captain_animations_list)
							

					if type == 'constraint':
						sprite = Tile((tile_size,tile_size),x,y)

					sprite_group.add(sprite)
		
		return sprite_group

	def player_setup(self,layout):
		for row_index, row in enumerate(layout):
			for col_index,val in enumerate(row):
				x = col_index * tile_size
				y = row_index * tile_size
				if val == '0':
					sprite = Player((x,y),self.display_surface,player_assets_path,palyer_animations_list)
					self.player.add(sprite)
				if val == '1':
					door_surface = pygame.image.load('../Assets/7-Objects/2-Door/1-Closed/1.png').convert_alpha()
					sprite = StaticTile((78,96),x,y,door_surface)
					self.goal.add(sprite)

	def enemy_collision_reverse(self):
		for enemy in self.enemy_sprites.sprites():
			if pygame.sprite.spritecollide(enemy,self.constraint_sprites,False):
				enemy.reverse()

	def horizontal_movement_collision(self):
		player = self.player.sprite
		player.rect.x += player.direction.x * player.speed
		self.collidable_sprites = self.terrain_sprites.sprites() + self.fg_objects_sprites.sprites() + self.canon_sprites.sprites()
		for sprite in self.collidable_sprites:
			if sprite.rect.colliderect(player.rect):
				if player.direction.x < 0: 
					player.rect.left = sprite.rect.right
					player.on_left = True
					self.current_x = player.rect.left
				elif player.direction.x > 0:
					player.rect.right = sprite.rect.left
					player.on_right = True
					self.current_x = player.rect.right

	def vertical_movement_collision(self):
		player = self.player.sprite
		player.apply_gravity()

		for sprite in self.collidable_sprites:
			if sprite.rect.colliderect(player.rect):
				if player.direction.y > 0: 
					player.rect.bottom = sprite.rect.top
					player.direction.y = 0
					player.on_ground = True
				elif player.direction.y < 0:
					player.rect.top = sprite.rect.bottom
					player.direction.y = 0
					player.on_ceiling = True
		if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
			player.on_ground = False

	def player_jump(self):
		player=self.player.sprite
		player.jump()
		jump=ParticleEffect((player.rect.x+30,player.rect.y+30),"jump")
		self.dust_sprite.add(jump)

	def scroll_x(self):
		player = self.player.sprite
		player_x = player.rect.centerx
		direction_x = player.direction.x

		if player_x < screen_width / 3 and direction_x < 0:
			self.world_shift = player.C_SPEED
			player.speed = 0
		elif player_x > screen_width - (screen_width / 3) and direction_x > 0:
			self.world_shift = - player.C_SPEED
			player.speed = 0
		else:
			player.speed = player.C_SPEED
			self.world_shift = 0

	def welcome(self):
		welcomefont = pygame.font.SysFont('comicsans',100)
		welcome_text=welcomefont.render("Welcome to The Game",1,"#E48022")
		text=self.font.render("Press any key to continue....",1,"#F71478")
		name_text=welcomefont.render("Developed by Hirok Reza",1,"#E48022")
		self.display_surface.blit(welcome_text,((screen_width - welcome_text.get_width())/2,(screen_height-welcome_text.get_height())/2-welcome_text.get_height()))
		self.display_surface.blit(name_text,((screen_width - name_text.get_width())/2,(screen_height-name_text.get_height())/2))
		self.display_surface.blit(text,((screen_width - text.get_width()),(screen_height-text.get_height())))
		pygame.display.update()

	def game_end(self):
		self.level_bg_music.stop()
		self.gameOver_sound.play()
		winfont = pygame.font.SysFont('comicsans',100)
		win_text=winfont.render("Game Over",1,"green")
		self.display_surface.blit(win_text,((screen_width - win_text.get_width())/2,(screen_height-win_text.get_height())/2))
		pygame.display.update()
		pygame.time.delay(2000)

	def check_death(self):
		if self.player.sprite.rect.top > screen_height or self.player.sprite.health <= 0:
			self.game_end()
			self.game_status=False
		
	def check_win(self):
		if pygame.sprite.spritecollide(self.player.sprite,self.goal,False):
			if  len(self.enemy_sprites.sprites()) > 3:
				text=self.font.render("Enemy should be less than 3 to complete the level....",1,"#2aaef5")
				self.display_surface.blit(text,((screen_width - text.get_width()),(screen_height-text.get_height())))
			else:
				self.game_end()
				self.game_status=False
			
	def check_coin_collisions(self):
		collided_coins = pygame.sprite.spritecollide(self.player.sprite,self.coin_sprites,True)
		if collided_coins:
			self.coin_sound.play()
			for coin in collided_coins:
				self.coins+=coin.value

	def check_enemy_collisions(self):
		enemy_collisions = pygame.sprite.spritecollide(self.player.sprite,self.enemy_sprites,False)

		if enemy_collisions:
			for enemy in enemy_collisions:
				enemy_center = enemy.rect.centery
				enemy_top = enemy.rect.top
				player_bottom = self.player.sprite.rect.bottom
				if enemy_top < player_bottom < enemy_center and self.player.sprite.direction.y >= 0:
					self.player.sprite.direction.y = -15
					enemy.get_hit(self.player.sprite.attack_power*4)
					if enemy.health <=0:
						self.stomp_sound.play()
						explosion_sprite = ParticleEffect(enemy.rect.center,'explosion')
						self.explosion_sprites.add(explosion_sprite)
						enemy.kill()
				else:
					self.player.sprite.get_hit(enemy.attack_power)
					enemy.status="Attack"
				
	def shoot_canon_ball(self):
		player=self.player.sprite
		for canon in self.canon_sprites.sprites():
				if not canon.flip and screen_width*0.60 > canon.rect.left - player.rect.centerx > 0  and 0<canon.rect.centerx <screen_width:
					if canon.shoot_ready:
						ball=CannonBall(canon.rect.center,(30,30),self.display_surface,1)
						self.canon_ball.add(ball)
					canon.shoot()

				elif canon.flip and -1*screen_width*0.60 < canon.rect.right - player.rect.centerx < 0 and 0<canon.rect.centerx <screen_width : 
					if canon.shoot_ready:
						ball=CannonBall(canon.rect.center,(30,30),self.display_surface,-1)
						self.canon_ball.add(ball)
					canon.shoot()
				
	def check_canon_ball_collisions(self):
		if self.canon_ball:
			collided_balls = pygame.sprite.spritecollide(self.player.sprite,self.canon_ball,False)
			if collided_balls:
				for ball in collided_balls:
					self.player.sprite.get_hit(ball.damage)

	def shoot_bullets(self):
		if len(self.bullets.sprites()) < 10 :
			player=self.player.sprite
			bullet=Bullet(player.rect.center,(50,30),self.display_surface,1)
			if not player.facing_right:
				bullet.direction.x*=-1
			self.bullets.add(bullet)

	def bullets_collision(self):
		for sprite in  self.terrain_sprites.sprites() + self.fg_objects_sprites.sprites():
			pygame.sprite.spritecollide(sprite,self.bullets,True)

	def bullets_canons_collided(self):
		for canon in self.canon_sprites.sprites():
			if pygame.sprite.spritecollide(canon,self.bullets,True):
				canon.get_hit(self.player.sprite.attack_power*4)
				if canon.health <=0:
					expo=ParticleEffect(canon.rect.center,"bomb_explotion")
					self.explosion_sprites.add(expo)
					self.canonexplo_sound.play()
					canon.kill()

	def bullets_enemy_collided(self):
		for enemy in self.enemy_sprites.sprites():
			if pygame.sprite.spritecollide(enemy,self.bullets,True):
					enemy.get_hit(self.player.sprite.attack_power*2)
					if enemy.health <=0:
						self.stomp_sound.play()
						explosion_sprite = ParticleEffect(enemy.rect.center,'explosion')
						self.explosion_sprites.add(explosion_sprite)
						enemy.kill()
				
	def run(self):

		# run the entire game / level 
		
		# # clouds
		# self.sky.draw(self.display_surface)
		self.clouds.draw(self.display_surface,self.world_shift)
		
		self.goal.update(self.world_shift)
		self.goal.draw(self.display_surface)

		# terrain 
		self.terrain_sprites.update(self.world_shift)
		self.terrain_sprites.draw(self.display_surface)

		#bg_object
		self.bg_objects_sprites.update(self.world_shift)
		self.bg_objects_sprites.draw(self.display_surface)

		# Objects
		self.fg_objects_sprites.update(self.world_shift)
		self.fg_objects_sprites.draw(self.display_surface)

		# # coins 
		self.coin_sprites.update(self.world_shift)
		self.coin_sprites.draw(self.display_surface)
		
		# # enemy 
		self.enemy_sprites.update(self.world_shift)
		self.constraint_sprites.update(self.world_shift)
		self.enemy_collision_reverse()
		self.enemy_sprites.draw(self.display_surface)
		self.explosion_sprites.update(self.world_shift)
		self.explosion_sprites.draw(self.display_surface)

		#canon_ball
		self.canon_ball.update(self.world_shift)
		self.canon_ball.draw(self.display_surface)
		self.check_canon_ball_collisions()

		#canonos
		self.canon_sprites.update(self.world_shift)
		self.canon_sprites.draw(self.display_surface)
		
		#canon Ball
		self.shoot_canon_ball()

		# player bullets
		self.bullets.update(self.world_shift)
		self.bullets.draw(self.display_surface)
		self.bullets_collision()
		self.bullets_canons_collided()
		self.bullets_enemy_collided()

		# player sprites
		self.player.update()
		self.horizontal_movement_collision()
		self.vertical_movement_collision()
		
		self.scroll_x()
		self.player.draw(self.display_surface)

		self.check_death()
		self.check_win()

		self.check_coin_collisions()
		self.check_enemy_collisions()

		# general info
		self.show_coins()
		self.show_enemy_count()

		#debuging sector
		# print(len(self.bullets.sprites()))
		# print(len(self.canon_ball.sprites()))
		# print("player speed " +str(self.player.sprite.speed))
		# print("World shift " +str(self.world_shift))

