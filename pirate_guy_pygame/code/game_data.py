level_0 = {
		'terrain': '../levels/0/level_0_terrain.csv',
		'coins':'../levels/0/level_0_coins.csv',	
		'objects': '../levels/0/level_0_objects.csv',
		'enemies':'../levels/0/level_0_enemies.csv',
        'player': '../levels/0/level_0_player.csv',
		'constraints':'../levels/0/level_0_constraints.csv',
        'canon':'../levels/0/level_0_canon.csv',
		'node_pos': (110,400),
		'unlock': 1,
		'node_graphics': '../graphics/overworld/0'}
level_1 = {
		'terrain': '../levels/1/level_1_terrain.csv',
		'coins':'../levels/1/level_1_coins.csv',	
		'fg_objects': '../levels/1/level_1_fg_objects.csv',
		'bg_objects': '../levels/1/level_1_bg_objects.csv',
		'enemies':'../levels/1/level_1_enemies.csv',
        'player': '../levels/1/level_1_player.csv',
		'constraints':'../levels/1/level_1_constraints.csv',
        'canon':'../levels/1/level_1_canon.csv',
		'node_pos': (110,400),
		'unlock': 2,
		'node_graphics': '../graphics/overworld/0'}

levels = {
	0: level_0,
	1: level_1
	}


player_assets_path='../Assets/1-Player-Bomb Guy/'
palyer_animations_list=['idle','run','jump','fall',"hit","dead_hit","dead_Ground"]
enemy_blad_pirate_assets_path ="../Assets/2-Enemy-Bald Pirate/"
enemy_blad_pirate_animations_list =["Run","Attack","Hit","Dead Hit"]
enemy_big_guy_assets_path ="../Assets/4-Enemy-Big Guy/"
enemy_big_guy_animations_list =["Run","Attack","Hit","Dead Hit"]
enemy_captain_assets_path ="../Assets/5-Enemy-Captain/"
enemy_captain_animations_list =["Idle","Run","Attack","Scare Run","Hit","Dead Hit"]

canon_assets_path= "../Assets/7-Objects/16-Enemy-Cannon/"
canon_animations_list =["Idle","Attack"]