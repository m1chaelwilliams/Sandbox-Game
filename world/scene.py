import pygame
from globals import *
from world.texturedata import atlas_textures, ow_atlas_textures, inventory_textures, player_textures,misc_textures
from sprites.tile import *
from world.itemdata import items
from sprites.player import Player
from groups.camera import Camera, ParallaxCamera
from inventory.inventory import Inventory
from world.prefabs import *
from utils.animations import Animation
from opensimplex import OpenSimplex
import random
import json
import os

class Scene:
    def __init__(self, app) -> None:
        self.app = app
        self.screen = self.app.screen # alias for convenience



        # groups
        self.sprites = Camera()
        self.background_group = ParallaxCamera()
        self.block_group = pygame.sprite.Group()
        self.platform_group = pygame.sprite.Group()
        self.item_group = Camera()
        self.wall_group = Camera()
        self.drop_group = Camera()
        self.chest_group = pygame.sprite.Group()
        # group list
        self.group_list = {
            'sprites':self.sprites,
            'block_group':self.block_group,
            'item_group':self.item_group,
            'wall_group':self.wall_group,
            'platform_group':self.platform_group,
            'chest_group':self.chest_group,
            'drop_group':self.drop_group,
        }

        print(len(self.block_group))
    def on_load(self):
        # world key
        self.world_key = self.app.world_key

        # textures
        self.textures = self.gen_textures(ow_atlas_textures, 'res/atlas/owatlas.png', (TILESIZE*16, TILESIZE*16))
        self.textures.update(self.gen_spritesheet_textures(player_textures))
        self.textures.update(self.gen_spritesheet_textures(misc_textures))
        self.inventory_textures = self.gen_inventory_textures(inventory_textures, 'res/atlas/owatlas.png', (TILESIZE*16, TILESIZE*16))
        # inventory
        self.inventory = Inventory(self.app, self.inventory_textures)

        # loading data
        self.load_chests()

        # animation
        self.breaking_block = Animation(self.textures['breaking_block'], (TILESIZE, TILESIZE))

        # temp
        self.player = Player([self.sprites], pygame.Surface((TILESIZE, TILESIZE*2)), (300, 0), {
            'mass':5,
            'speed':10,
            'block_group':self.block_group,
            'textures':self.textures,
            'app':self.app,
            'inventory':self.inventory,
            'app':self.app,
            'group_list':self.group_list,
            'player_textures':{
                'player_static':self.textures['player_static'],
                'player_running':self.textures['player_running'],
                'player_jumping':self.textures['player_jumping'],
            }
        })

        # chunking
        Scene.chunksize = 30
        Scene.chunkpixelsize = self.chunksize*TILESIZE
        Scene.chunkheight = 50
        Scene.seed = 1209382983

        self.player_chunk_pos = self.player.rect.x // Scene.chunkpixelsize
        self.prev_player_chunk_pos = self.player_chunk_pos

        self.all_chunks: list[Chunk] = {}
        self.load_chunks()
        self.loaded_chunks = self.gen_world()
        self.gen_background()
        self.player.active_chunk = self.loaded_chunks[self.player_chunk_pos]
        self.player.active_chunks = self.loaded_chunks
    def gen_background(self):
        noise_generator = OpenSimplex(seed=Scene.seed*2)
        heightmap = []
        for x in range(300):
            noise_value = noise_generator.noise2(x * 0.05, 0)
            height = int((noise_value + 1) * 5 + 10)  # Map noise value to desired range
            heightmap.append(height)
        
        for x in range(len(heightmap)):
            for y in range(heightmap[x]):
                block_position = (x*(TILESIZE/2) - (len(heightmap)/2)*(TILESIZE/2), 30*(TILESIZE/2) -y*(TILESIZE/2))
                blocktype = 'grass'
                if y < heightmap[x]-1:
                    blocktype = 'dirt'
                if y < heightmap[x]-5 + random.randint(-2, 2):
                    blocktype = 'stone'
                if blocktype == 'stone' and random.randint(0,15) < 2:
                    blocktype = 'coal'
                        
                BackgroundTile([self.background_group], image=pygame.transform.scale(self.textures[blocktype], (TILESIZE/2, TILESIZE/2)), position= block_position, name=blocktype)
    def gen_world(self):
        chunks = {}
        # chunks[self.player_chunk_pos] = Chunk(self.player_chunk_pos, self.sprites, self.block_group, self.wall_group, self.textures, self)
        # chunks[self.player_chunk_pos-1] = Chunk(self.player_chunk_pos-1, self.sprites, self.block_group, self.wall_group, self.textures, self)
        # chunks[self.player_chunk_pos+1] = Chunk(self.player_chunk_pos+1, self.sprites, self.block_group, self.wall_group, self.textures, self)
        if self.player_chunk_pos in self.all_chunks:
            chunks[self.player_chunk_pos] = self.all_chunks[self.player_chunk_pos]
        else:
            chunks[self.player_chunk_pos] = Chunk(self.player_chunk_pos, self.sprites, self.block_group, self.wall_group, self.textures, self)
        
        if self.player_chunk_pos-1 in self.all_chunks:
            chunks[self.player_chunk_pos-1] = self.all_chunks[self.player_chunk_pos-1]
        else:
            chunks[self.player_chunk_pos-1] = Chunk(self.player_chunk_pos-1, self.sprites, self.block_group, self.wall_group, self.textures, self)
        
        if self.player_chunk_pos+1 in self.all_chunks:
            chunks[self.player_chunk_pos+1] = self.all_chunks[self.player_chunk_pos+1]
        else:
            chunks[self.player_chunk_pos+1] = Chunk(self.player_chunk_pos+1, self.sprites, self.block_group, self.wall_group, self.textures, self)

        return chunks
    def gen_textures(self, texturedata, file_path, size) -> dict:
        atlas_img = pygame.transform.scale(pygame.image.load(file_path).convert_alpha(), size)

        textures = {}
        for name, data in texturedata.items():
            textures[name] = pygame.Surface.subsurface(atlas_img, pygame.Rect(
                data.position[0]*TILESIZE,
                data.position[1]*TILESIZE,
                data.size[0],
                data.size[1]
            ))
        return textures
    def gen_spritesheet_textures(self, texture_data):
        textures = {}
        for name, data in texture_data.items():
            textures[name] = pygame.transform.scale(pygame.image.load(data.file_path).convert_alpha(), data.size)
        return textures
    def gen_inventory_textures(self, texturedata, file_path, size) -> dict:
        atlas_img = pygame.transform.scale(pygame.image.load(file_path).convert_alpha(), size)

        textures = {}
        for name, data in texturedata.items():
            textures[name] = pygame.Surface.subsurface(atlas_img, pygame.Rect(
                data.position[0]*TILESIZE,
                data.position[1]*TILESIZE,
                data.size[0],
                data.size[1]
            ))
            if textures[name].get_width() > TILESIZE or textures[name].get_height() > TILESIZE:
                textures[name] = pygame.transform.scale_by(textures[name], 1/(max(textures[name].get_width(), textures[name].get_height())/TILESIZE))
        return textures
    def update(self):


        self.item_group.update()
        self.sprites.update()
        self.inventory.update()
        self.drop_group.update()

        # chunking

        self.prev_player_chunk_pos = self.player_chunk_pos
        self.player_chunk_pos = self.player.rect.x//Scene.chunkpixelsize

        if self.prev_player_chunk_pos < self.player_chunk_pos:
            newPos = self.player_chunk_pos+1
            to_be_delete_Pos = self.prev_player_chunk_pos-1
            if newPos in self.loaded_chunks:
                self.loaded_chunks[newPos].add_chunk()
            else:
                if newPos in self.all_chunks:
                    self.loaded_chunks[newPos] = self.all_chunks[newPos]
                else:
                    self.loaded_chunks[newPos] = Chunk(newPos, self.sprites, self.block_group, self.wall_group, self.textures, self)
                self.loaded_chunks[newPos].add_chunk()
                print(len(self.block_group.sprites()))
            self.loaded_chunks[to_be_delete_Pos].remove_chunk()

        if self.prev_player_chunk_pos > self.player_chunk_pos:
            newPos = self.player_chunk_pos-1
            to_be_delete_Pos = self.prev_player_chunk_pos+1
            if newPos in self.loaded_chunks:
                self.loaded_chunks[newPos].add_chunk()
            else:
                if newPos in self.all_chunks:
                    self.loaded_chunks[newPos] = self.all_chunks[newPos]
                else:
                    self.loaded_chunks[newPos] = Chunk(newPos, self.sprites, self.block_group, self.wall_group, self.textures, self)
                self.loaded_chunks[newPos].add_chunk()
            self.loaded_chunks[to_be_delete_Pos].remove_chunk()

        if self.prev_player_chunk_pos != self.player_chunk_pos:
            self.player.active_chunk = self.loaded_chunks[self.player_chunk_pos]
            self.player.active_chunks = self.loaded_chunks
    def draw(self):
        self.screen.fill('lightblue')
        self.background_group.draw(self.screen, self.player)
        self.wall_group.draw(self.screen, self.player)
        self.item_group.draw(self.screen, self.player)
        self.drop_group.draw(self.screen, self.player)
        self.sprites.draw(self.screen, self.player)

        offset = pygame.math.Vector2()
        offset.x = (self.screen.get_width() / 2 - self.player.rect.centerx)
        offset.y = (self.screen.get_height() / 2 - self.player.rect.centery)

        pos = self.player.get_block_pos(self.player.get_adjusted_mouse_position())
        sprite_offset = pygame.math.Vector2()
        sprite_offset.x = offset.x + pos[0]
        sprite_offset.y = offset.y + pos[1]

        surf = pygame.Surface((TILESIZE, TILESIZE))
        surf.fill('gray')
        surf.set_alpha(128)
        self.screen.blit(surf, sprite_offset)
        if self.player.breaking_block:
            self.breaking_block.speed = self.player.active_block_hardness * self.player.strength
            self.breaking_block.update()
            self.screen.blit(self.breaking_block.get_frame(), sprite_offset)
        else:
            self.breaking_block.active_frame = 0
        for chest in self.chest_group:
            if chest.open:
                chest.draw_tiles(self.app.screen)
        self.inventory.draw()
    def load_chests(self):
        if os.path.getsize(f'worlddata/{self.world_key}/chestdata.json') > 0:
            with open(f'worlddata/{self.world_key}/chestdata.json', 'r') as f:
                data = json.load(f)
                for index, chest_data in data.items():
                    chest = StorageBlock([self.item_group, self.block_group, self.chest_group], self.textures['chest'], position=chest_data['position'], name="chest")
                    chest.slots = chest_data['data']
    def load_chunks(self):
        if os.path.getsize(f'worlddata/{self.world_key}/chunkdata.json') > 0:
            with open(f'worlddata/{self.world_key}/chunkdata.json', 'r') as f:
                data = json.load(f)
                for index, chunk_data in data.items():
                    chunk_blocks = []
                    for block in chunk_data['data']:
                        groups = [self.group_list[group] for group in items[block['name']].groups]
                        block_type = items[block['name']].use_type
                        special_flags = None
                        if 'special_flags' in block and block['special_flags'] == "tree":
                            print('treeeeee')
                            groups = [self.wall_group, self.block_group]
                            block_type = WallBlock
                            special_flags = "tree"
                        flipped = 0
                        if 'flipped' in block:
                            flipped = block['flipped']
                        tile = block_type(groups, self.textures[block['name']], block['position'], name=block['name'], flipped=flipped, hardness=items[block['name']].hardness, durability=items[block['name']].durability, special_flags=special_flags)
                        chunk_blocks.append(tile)

                    chunk = Chunk(chunk_data['position'], self.sprites, self.block_group, self.wall_group, self.textures, self, chunk_blocks)
                    if chunk_data['position'] < self.player_chunk_pos - 1 or chunk_data['position'] > self.player_chunk_pos + 1:
                        chunk.remove_chunk()
    def save_chunks(self):
        print(self.all_chunks)
        chunk_data = {}
        for index, chunk in self.all_chunks.items():
            block_data = []
            for block in chunk.chunk_blocks:
                if block.name != "chest":
                    if block.special_flags == "tree":
                        block_data.append({'name':block.name, 'position':block.rect.bottomleft, 'flipped':block.flipped, 'special_flags':'tree'})
                    else:
                        block_data.append({'name':block.name, 'position':block.rect.bottomleft, 'flipped':block.flipped,})
            chunk_data[index] = {'position':chunk.chunk_pos, 'data':block_data}
        
        with open(f'worlddata/{self.world_key}/chunkdata.json', 'w') as f:
            json.dump(chunk_data, f)
    def save_chests(self):
        chest_data = {}
        for index, chest in enumerate(self.chest_group):
            chest_data[index] = {'position':chest.rect.bottomleft, 'data':chest.slots}
        with open(f'worlddata/{self.world_key}/chestdata.json', 'w') as f:
            json.dump(chest_data, f)
    def get_block_pos(self, position):
        return (int((position[0]//TILESIZE)*TILESIZE), int((position[1]//TILESIZE)*TILESIZE))
    def close(self):
        self.inventory.close()
        self.save_chests()
        self.save_chunks()
            
class Chunk:
    def __init__(self, chunk_pos, visible_sprites, blocks, wall_group, textures, scene: Scene, chunk_blocks: list[Tile] = None):
        self.scene = scene
        self.scene.all_chunks[chunk_pos] = self
        self.chunk_pos = chunk_pos
        self.generated = False
        self.visible_sprites = visible_sprites
        self.wall_group = wall_group
        self.blocks = blocks
        self.textures = textures
        self.biome_id = random.randint(0,1)

        if chunk_blocks:
            self.chunk_blocks = chunk_blocks
        else:
            self.chunk_blocks: list[Tile] = []
            self.gen_chunk()
        
        print(type(self.chunk_blocks))
    def gen_chunk(self):
        print('generated new chunk !!!')

        self.generated = True
        self.heightmap = self.gen_heightmap(Scene.seed, range(self.chunk_pos*Scene.chunksize, self.chunk_pos*Scene.chunksize+Scene.chunksize), 0.05, 5)

        # gen blocks
        for x in range(len(self.heightmap)):
            for y in range(self.heightmap[x]):
                block_position = (Scene.chunkpixelsize*self.chunk_pos+ x*TILESIZE, Scene.chunkheight*TILESIZE - y*TILESIZE)
                blocktype = 'grass'
                if y < self.heightmap[x]-1:
                    blocktype = 'dirt'
                if y < self.heightmap[x]-5 + random.randint(-2, 2):
                    blocktype = 'stone'
                if blocktype == 'stone' and random.randint(0,15) < 2:
                    blocktype = 'coal'
                    if y < 15:
                        if random.randint(0,5) > 2:
                            blocktype = 'iron'
                    if y < 8:
                        if random.randint(0,20) > 17:
                            blocktype = "diamond"
                if y == self.heightmap[x]-1 and random.randint(0,20) == 1:
                    self.spawn_tree(block_position)
                
                self.chunk_blocks.append(Tile([self.visible_sprites, self.blocks], image=self.textures[blocktype], position= block_position, name=blocktype, hardness=items[blocktype].hardness, durability=items[blocktype].durability))
    def gen_heightmap(self, seed, x_range, scale, height_val):
        noise_generator = OpenSimplex(seed=seed)
        heightmap = []
        for x in x_range:
            noise_value = noise_generator.noise2(x * scale, 0)
            height = int((noise_value + 1) * height_val + 30)  # Map noise value to desired range
            heightmap.append(height)
        return heightmap
    def remove_chunk(self):
        for block in self.chunk_blocks:
            self.visible_sprites.remove(block)
            self.blocks.remove(block)
    def add_chunk(self):
        for block in self.chunk_blocks:
            for group in block.in_groups:
                group.add(block)
    def add_block(self, block):
        self.chunk_blocks.append(block)
    def remove_block(self, block):
        if block in self.chunk_blocks:
            self.chunk_blocks.remove(block)
    def spawn_tree(self, position: tuple):
        for i, row in enumerate(tree):
            for j, col in enumerate(row):
                if col != 0:
                    block_type = 'leaves'
                    x = position[0]+j*TILESIZE - (len(tree[0])//2)*TILESIZE
                    y = position[1]+i*TILESIZE - (len(tree))*TILESIZE
                    if col == 2:
                        block_type = 'wood'
                    self.chunk_blocks.append(WallBlock([self.wall_group, self.blocks], image=self.textures[block_type], position=(x,y), name=block_type, special_flags="tree"))
