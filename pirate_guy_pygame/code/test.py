from csv import reader


with open('../levels/0/level_0_terrain.csv') as map:
        levels = reader(map,delimiter = ',')
        for level in levels:
            print(type(level))
            print(level)