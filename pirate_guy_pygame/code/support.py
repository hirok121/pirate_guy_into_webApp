from csv import reader
from settings import tile_size
from os import walk
import pygame

def import_folder(path,scale=False,size=None):

	'''This Function take a argumennt as a path of folder containing only images and Return the list of Image_Surfaces'''

	surface_list = []

	for _,__,image_files in walk(path):
		for image in image_files:
			full_path = path + '/' + image
			# print(full_path)
			if scale:
				im_size_x=tile_size
				im_size_y=tile_size
				if "jump" in path :
					im_size_x=tile_size/1.5
				image_surf=pygame.transform.scale(pygame.image.load(full_path).convert_alpha(),size)
			else:
				image_surf = pygame.image.load(full_path).convert_alpha()

			surface_list.append(image_surf)

	return surface_list

def import_csv_layout(path):
	'''This Function take a argumennt as a Full_path of a CSV_File that contains Position of tiles and Return the list of list having separated value'''
	terrain_map = []
	with open(path) as map:
		level = reader(map,delimiter = ',')
		for row in level:
			terrain_map.append(list(row))
		return terrain_map

def import_cut_graphics(path):
	'''This Function take a argumennt as a Full_path of a Image and cut them into size OF TILE  and Return the list of small image and all are pygmae.Surface object'''
	surface = pygame.image.load(path).convert_alpha()
	tile_num_x = int(surface.get_size()[0] / tile_size)
	tile_num_y = int(surface.get_size()[1] / tile_size)

	cut_tiles = []
	for row in range(tile_num_y):
		for col in range(tile_num_x):
			x = col * tile_size
			y = row * tile_size
			new_surf = pygame.Surface((tile_size,tile_size),flags = pygame.SRCALPHA)
			new_surf.blit(surface,(0,0),pygame.Rect(x,y,tile_size,tile_size))
			cut_tiles.append(new_surf)

	return cut_tiles
