import pygame, sys
from settings import * 
from level import Level


# Pygame setup
pygame.init()
screen = pygame.display.set_mode((screen_width,screen_height))
clock = pygame.time.Clock()
bg=pygame.transform.scale(pygame.image.load("../Assets/bg.png").convert_alpha(),(screen_width,screen_height))
wc=pygame.transform.scale(pygame.image.load("../Assets/welcome.png").convert_alpha(),(screen_width,screen_height))

screen.blit(wc,(0,0))

run=False

	
level=Level(1,screen)

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type==pygame.KEYDOWN:
			run=True
			if event.key==pygame.K_RCTRL or event.key==pygame.K_w:
				level.shoot_bullets()
			if event.key==pygame.K_SPACE:
				level.player_jump()
	if run:
		screen.blit(bg,(0,0))
		level.run()
		if not  level.game_status:
			screen.blit(wc,(0,0))
			level=Level(1,screen)
			run=False


	pygame.display.update()
	clock.tick(60)