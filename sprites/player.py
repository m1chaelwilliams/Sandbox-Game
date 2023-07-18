from typing import Any
import pygame
from globals import *
from sprites.tile import Tile
from utils.events import EventHandler
from utils.controls import Controller
from world.itemdata import items
from inventory.inventory import Inventory
from world.itemdata import Item, BlockItem
from utils.animations import Animation, AnimationManager
from world.drops import Drop
import math

class Player(Tile):
    def __init__(self, groups, image: pygame.Surface, position: tuple, params) -> None:
        super().__init__(groups, image, position, name="player")

        # app
        self.app = params['app']
        # inventory
        self.inventory: Inventory = params['inventory']
        # self.inventory.add_item('chest')
        # self.inventory.add_item('leaves')
        # params
        self.mass = params['mass']
        self.speed = params['speed']
        # utils
        self.textures = params['textures']
        self.group_list = params['group_list']
        # interactable
        self.block_group = params['block_group']
        self.item_group = self.group_list['item_group']
        self.platform_group = self.group_list['platform_group']
        self.chest_group = self.group_list['chest_group']
        self.drop_group = self.group_list['drop_group']
        # chunk / block management
        self.active_chunk = None
        self.active_chunks = None
        # animations
        self.player_textures = params['player_textures']
        self.animation_manager = AnimationManager({
            'player_static':Animation(self.player_textures['player_static'], (TILESIZE, TILESIZE*2)),
            'player_running':Animation(self.player_textures['player_running'], (TILESIZE, TILESIZE*2)),
            'player_jumping':Animation(self.player_textures['player_jumping'], (TILESIZE, TILESIZE*2)),
        }, 'player_static')

        # vars
        self.velocity = pygame.math.Vector2()
        self.grounded = False
        self.strength = 0
        self.active_block_hardness = 1
        # states
        self.moving = False
        self.left = False
        self.right = False
        self.down = False
        self.breaking_block = False
    def input(self):
        keys = pygame.key.get_pressed()

        if keys[Controller.left]:
            self.velocity.x = -self.speed
            self.moving = True
            self.left = True
            self.right = False
        if keys[Controller.right]:
            self.velocity.x = self.speed
            self.moving = True
            self.right = True
            self.left = False
        if not keys[Controller.left] and not keys[Controller.right]:
            self.velocity.x = 0
            self.moving = False
        if keys[Controller.down]:
            self.down = True
        else:
            self.down = False

        # jumping
        if self.grounded and EventHandler.keydown(Controller.space):
            self.velocity.y = -15
            self.animation_manager.set_animation('player_jumping')

        # animations
        if abs(self.velocity.y) < 1 and self.moving and self.animation_manager.active_animation != "player_running":
            self.animation_manager.set_animation('player_running')
        if not self.moving:
            self.animation_manager.set_animation('player_static')
    def move(self):
        # gravity
        self.velocity.y += self.mass * GRAVITY
        if self.velocity.y > self.mass * TERMINAL_VELOCITY_CONSTANT:
            self.velocity.y = self.mass * TERMINAL_VELOCITY_CONSTANT

        # applying velocity
        self.rect.x += self.velocity.x
        self.check_collisions('horizontal')
        self.rect.y += self.velocity.y
        self.check_collisions('vertical')
    def check_collisions(self, dir: str):
        if dir == "horizontal":
            # block group collision
            for block in self.block_group:
                if block.active:
                    if block.rect.colliderect(self.rect):
                        if self.velocity.x > 0: # moving right
                            self.rect.right = block.rect.left
                        elif self.velocity.x < 0: # moving left
                            self.rect.left = block.rect.right
        elif dir == "vertical":
            collisions = 0
            # block group collision
            for block in self.block_group:
                if block.active:
                    if block.rect.colliderect(self.rect):
                        if self.velocity.y > 0: # moving down
                            self.rect.bottom = block.rect.top
                            collisions += 1
                        elif self.velocity.y < 0:
                            self.rect.top = block.rect.bottom
                            self.velocity.y = 0.1
            # platform collision
            table_collision = 0
            for block in self.platform_group:
                if not self.down and self.velocity.y > 0 and block.rect.top > self.rect.bottom-self.velocity.y-1 and block.rect.colliderect(self.rect):
                    self.rect.bottom = block.rect.top
                    self.velocity.y = 0.1
                    collisions += 1
                if block.name == "crafting_table":
                    if block.rect.colliderect(self.rect):
                        table_collision += 1
            if table_collision > 0:
                if not self.inventory.near_table:
                    self.inventory.near_table = True
                    self.inventory.available_recipes = self.inventory.gen_available_recipes()
                else:
                    self.inventory.near_table = True
            else:
                if self.inventory.near_table:
                    self.inventory.near_table = False
                    self.inventory.available_recipes = self.inventory.gen_available_recipes()
                else:
                    self.inventory.near_table = False
            if collisions > 0:
                self.grounded = True
                self.velocity.y = 0.1
            else:
                self.grounded = False
    def block_handling(self):
        mouse_pos = self.get_adjusted_mouse_position()
        mouse_block_pos = self.get_block_pos(mouse_pos)
        if not self.inventory.expanded_inventory and abs(math.sqrt((self.rect.x - mouse_pos[0])**2 + (self.rect.y - mouse_pos[1])**2)) < TILESIZE*4:
            left_click, middle_click, right_click = pygame.mouse.get_pressed()
            breaking = False
            placing = False
            if left_click:
                breaking = True
            else:
                self.breaking_block = False
            if right_click:
                placing = True
            if breaking:
                collision = 0
                broken = False
                for block in self.block_group:
                    if block.rect.collidepoint(mouse_pos):
                        collision += 1
                        self.active_block_hardness = block.hardness
                        if block.break_block(self.strength):
                            self.drop_item(block.name, 1, block.rect.center)
                            block.kill()
                            block.active = False
                            for chunk in self.active_chunks.values():
                                chunk.remove_block(block)
                            broken = True
                if not broken:
                    for block in self.platform_group:
                        if block.rect.collidepoint(mouse_pos):
                            self.active_block_hardness = block.hardness
                            collision += 1
                            if block.break_block(self.strength):
                                self.drop_item(block.name, 1, block.rect.center)
                                block.kill()
                                block.active = False
                                for chunk in self.active_chunks.values():
                                    chunk.remove_block(block)
                if collision > 0:
                    self.breaking_block = True
                else:
                    self.breaking_block = False
            if placing:
                collision = False
                mouse_pos = self.get_adjusted_mouse_position()
                active_type = items[self.inventory.active_slot.name].type_str
                for block in self.block_group:
                    if block.type == active_type and block.rect.collidepoint(mouse_pos):
                        collision = True  
                for platform in self.platform_group:
                    if active_type == 'platform':
                        if (platform.name == 'wood_platform' or platform.type == 'block') and platform.rect.collidepoint(mouse_pos):
                            collision = True
                    
                if not collision:
                    flipped = self.inventory.flipped
                    if self.inventory.active_slot.name != "default":
                        if not self.rect.colliderect(pygame.Rect(mouse_block_pos[0], mouse_block_pos[1], self.textures[self.inventory.active_slot.name].get_width(), self.textures[self.inventory.active_slot.name].get_height())):
                            block = self.inventory.use_item(self.textures[self.inventory.active_slot.name], self.get_block_pos(mouse_pos), [self.group_list[group] for group in items[self.inventory.active_slot.name].groups], self.active_chunk, flipped)
    def drop_handling(self):
        for drop in self.drop_group:
            if drop.active and drop.rect.colliderect(self.rect):
                if self.inventory.add_item(drop.name, drop.quantity) == drop.quantity:
                    drop.kill()
    def drop_item(self, name: str, quantity: int, position: tuple):
        print('dropping item!!')
        Drop(name, quantity, position, self.textures, [self.drop_group], self.block_group)
    def item_handling(self):
        if EventHandler.clicked(3):
            mouse_pos = self.get_adjusted_mouse_position()
            for item in self.item_group:
                if (item.name != "door" or not self.rect.colliderect(item.rect)) and item.rect.collidepoint(mouse_pos):
                    item.toggle(self)
    def get_adjusted_mouse_position(self) -> tuple:
        mouse_pos = pygame.mouse.get_pos()

        player_offset = pygame.math.Vector2()
        player_offset.x = self.app.SCREENWIDTH / 2 - self.rect.centerx
        player_offset.y = self.app.SCREENHEIGHT / 2 - self.rect.centery

        return (mouse_pos[0] - player_offset.x, mouse_pos[1] - player_offset.y)
    def get_block_pos(self, mouse_pos: tuple):
        return (int((mouse_pos[0]//TILESIZE)*TILESIZE), int((mouse_pos[1]//TILESIZE)*TILESIZE))
    def update(self) -> None:
        self.input()
        self.move()
        self.block_handling()
        self.drop_handling()
        self.item_handling()
        self.animation_manager.update()
        self.image = self.animation_manager.get_active_frame()
        if self.right:
            self.image = pygame.transform.flip(self.image, True, False)
        self.strength = items[self.inventory.active_slot.name].strength