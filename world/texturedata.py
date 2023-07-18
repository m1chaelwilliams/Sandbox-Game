from globals import *

class Atlas:
    def __init__(self, file_path: str, size: tuple, textures: dict):
        self.file_path = file_path
        self.size = size
        self.textures = textures
class AtlasTexture:
    def __init__(self, name: str, position: tuple, size: tuple, type = "default") -> None:
        self.name = name
        self.position = position
        self.size = size
class Texture:
    def __init__(self, name: str, size: tuple, file_path: str, type: str = "default") -> None:
        self.name = name
        self.size = size
        self.file_path = file_path
        self.type = type


ow_atlas_textures = {
    'grass':AtlasTexture('grass', (0,0), (TILESIZE, TILESIZE)),
    'dirt':AtlasTexture('dirt', (0,1), (TILESIZE, TILESIZE)),
    'stone':AtlasTexture('stone', (1,0), (TILESIZE, TILESIZE)),
    'wood':AtlasTexture('stone', (1,1), (TILESIZE, TILESIZE)),
    'leaves':AtlasTexture('stone', (2,0), (TILESIZE, TILESIZE)),
    'coal':AtlasTexture('stone', (2,1), (TILESIZE, TILESIZE)),
    'chest':AtlasTexture('chest', (3,0), (TILESIZE, TILESIZE)),
    'crafting_table':AtlasTexture('crafting_table', (3,1.5), (TILESIZE, TILESIZE//2)),
    'grass_wall':AtlasTexture('grass_wall', (4,0), (TILESIZE, TILESIZE)),
    'stone_wall':AtlasTexture('stone_wall', (5,0), (TILESIZE, TILESIZE)),
    'dirt_wall':AtlasTexture('dirt_wall', (4,1), (TILESIZE, TILESIZE)),
    'wood_wall':AtlasTexture('wood_wall', (5,1), (TILESIZE, TILESIZE)),
    'door':AtlasTexture('door', (6,0), (TILESIZE*2, TILESIZE*2)),
    'wood_planks':AtlasTexture('wood_planks', (8,0), (TILESIZE, TILESIZE)),
    'wood_slab':AtlasTexture('wood_slab', (9,0.5), (TILESIZE, TILESIZE//2)),
    'wood_stairs':AtlasTexture('wood_stairs', (8,1), (TILESIZE, TILESIZE)),
    'wood_platform':AtlasTexture('wood_platform', (9,1.5), (TILESIZE, TILESIZE//2)),
    'wood_pickaxe':AtlasTexture('wood_pickaxe', (0,2), (TILESIZE, TILESIZE)),
    'stone_pickaxe':AtlasTexture('stone_pickaxe', (1,2), (TILESIZE, TILESIZE)),
    'iron_pickaxe':AtlasTexture('iron_pickaxe', (0,3), (TILESIZE, TILESIZE)),
    'diamond_pickaxe':AtlasTexture('diamond_pickaxe', (1,3), (TILESIZE, TILESIZE)),
    'furnace':AtlasTexture('furnace', (2,2), (TILESIZE, TILESIZE)),
    'stick':AtlasTexture('stick', (0,4), (TILESIZE, TILESIZE)),
    'iron':AtlasTexture('iron', (3,2), (TILESIZE, TILESIZE)),
    'diamond':AtlasTexture('diamond', (2,3), (TILESIZE, TILESIZE)),
}
inventory_textures = {
    'grass':AtlasTexture('grass', (0,0), (TILESIZE, TILESIZE)),
    'dirt':AtlasTexture('dirt', (0,1), (TILESIZE, TILESIZE)),
    'stone':AtlasTexture('stone', (1,0), (TILESIZE, TILESIZE)),
    'wood':AtlasTexture('stone', (1,1), (TILESIZE, TILESIZE)),
    'leaves':AtlasTexture('stone', (2,0), (TILESIZE, TILESIZE)),
    'coal':AtlasTexture('stone', (2,1), (TILESIZE, TILESIZE)),
    'chest':AtlasTexture('chest', (3,0), (TILESIZE, TILESIZE)),
    'crafting_table':AtlasTexture('crafting_table', (3,1), (TILESIZE, TILESIZE)),
    'grass_wall':AtlasTexture('grass_wall', (4,0), (TILESIZE, TILESIZE)),
    'stone_wall':AtlasTexture('stone_wall', (5,0), (TILESIZE, TILESIZE)),
    'dirt_wall':AtlasTexture('dirt_wall', (4,1), (TILESIZE, TILESIZE)),
    'wood_wall':AtlasTexture('wood_wall', (5,1), (TILESIZE, TILESIZE)),
    'door':AtlasTexture('door', (7,0), (TILESIZE, TILESIZE*2)),
    'wood_planks':AtlasTexture('wood_planks', (8,0), (TILESIZE, TILESIZE)),
    'wood_slab':AtlasTexture('wood_slab', (9,0), (TILESIZE, TILESIZE)),
    'wood_stairs':AtlasTexture('wood_stairs', (8,1), (TILESIZE, TILESIZE)),
    'wood_platform':AtlasTexture('wood_platform', (9,1), (TILESIZE, TILESIZE)),
    'wood_pickaxe':AtlasTexture('wood_pickaxe', (0,2), (TILESIZE, TILESIZE)),
    'stone_pickaxe':AtlasTexture('stone_pickaxe', (1,2), (TILESIZE, TILESIZE)),
    'iron_pickaxe':AtlasTexture('iron_pickaxe', (0,3), (TILESIZE, TILESIZE)),
    'diamond_pickaxe':AtlasTexture('diamond_pickaxe', (1,3), (TILESIZE, TILESIZE)),
    'furnace':AtlasTexture('furnace', (2,2), (TILESIZE, TILESIZE)),
    'stick':AtlasTexture('stick', (0,4), (TILESIZE, TILESIZE)),
    'iron':AtlasTexture('iron', (3,2), (TILESIZE, TILESIZE)),
    'diamond':AtlasTexture('diamond', (2,3), (TILESIZE, TILESIZE)),
}
player_textures = {
    'player_static':Texture('player_static', (TILESIZE, TILESIZE*2), "res/player/player_static.png", "player"),
    'player_running':Texture('player_running', (TILESIZE*2, TILESIZE*2), "res/player/player_running.png", "player"),
    'player_jumping':Texture('player_jumping', (TILESIZE, TILESIZE*2), "res/player/player_jumping.png", "player"),
}
misc_textures = {
    'breaking_block':Texture('breaking_block', (TILESIZE*4, TILESIZE), 'res/block_breaking.png')
}
atlas_textures = {
    'ow_atlas':Atlas('res/atlas/owatlas.png', (16*TILESIZE,16*TILESIZE), ow_atlas_textures)
}