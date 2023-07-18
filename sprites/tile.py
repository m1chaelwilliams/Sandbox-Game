import pygame
from globals import *
from utils.events import EventHandler

class Tile(pygame.sprite.Sprite):
    def __init__(self, groups, image: pygame.Surface, position: tuple, name: str = "default", type="block", flipped=0, durability: int = 20, hardness: int = 1, special_flags = None) -> None:
        super().__init__(groups)
        self.name = name
        self.type = type
        self.in_groups = groups
        self.image = image.copy()
        self.rect = self.image.get_rect(bottomleft = (position[0], position[1]+TILESIZE))
        self.flipped = flipped
        match flipped:
            case 1:
                self.image = pygame.transform.flip(self.image, True, False)
            case 2:
                self.image = pygame.transform.flip(self.image, True, True)
            case 3:
                self.image = pygame.transform.flip(self.image, False, True)
        self.active = True
        self.durability = durability
        self.hardness = hardness
        self.special_flags = special_flags
    def break_block(self, strength) -> bool:
        if strength >= self.hardness:
            self.durability -= 1 * strength
            if self.durability < 1:
                self.active = False
                self.kill()
                return True
        return False
class BackgroundTile(Tile):
    def __init__(self, groups, image: pygame.Surface, position: tuple, name: str = "default", type="block", flipped=0, durability: int = 20, hardness: int = 1, special_flags = None) -> None:
        super().__init__(groups, image, position, name, type, flipped, durability, hardness, special_flags)
        self.image = image.copy()
        self.image.set_alpha(128)
class WallBlock(Tile):
    def __init__(self, groups, image: pygame.Surface, position: tuple, name: str = "default", type="wall", flipped=0, durability: int = 20, hardness: int = 1, special_flags = None) -> None:
        super().__init__(groups, image, position, name, type, flipped, durability, hardness, special_flags)
        self.active = False

# chest
class StorageBlock(Tile):
    def __init__(self, groups, image: pygame.Surface, position: tuple, name: str = "default", type="block", flipped=0, durability: int = 20, hardness: int = 1, special_flags = None) -> None:
        super().__init__(groups, image, position, name, type, flipped, durability, hardness, special_flags)

        self.columns = 10
        self.rows = 3

        self.slot_rects: list[pygame.Rect] = self.gen_tiles()
        self.open = False
        self.slots = []
        for index in range(30):
            self.slots.append({'name':'default', 'quantity':0})
        # self.slots[3] = {'name':'wood_planks', 'quantity':100}

        # misc.
        self.surf = pygame.Surface((TILESIZE*1.5, TILESIZE*1.5))
        self.surf.fill("gray")
        self.surf.set_alpha(128)
        self.delay = 5

        self.active = False
    def toggle(self, player):
        if self.open:
            player.inventory.active_chest = None
        else:
            player.inventory.active_chest = self
        player.inventory.expanded_inventory = not player.inventory.expanded_inventory
        self.open = not self.open
    def gen_tiles(self):
        slots = []

        x_offset = SCREENWIDTH//2 - (self.columns/2)*(TILESIZE*1.5)
        y_offset = SCREENHEIGHT//2 - (self.rows/2)*(TILESIZE*1.5) + TILESIZE*2
        for i in range(self.rows):
            for j in range(self.columns):
                slots.append(pygame.Rect(x_offset + j*TILESIZE*1.5, y_offset + i*TILESIZE*1.5, TILESIZE, TILESIZE))
        return slots
    def draw_tiles(self, display: pygame.Surface):
        for slot in self.slot_rects:
            display.blit(self.surf, (slot.x-TILESIZE//4, slot.y-TILESIZE//4))
            pygame.draw.rect(display, "gray", pygame.Rect(slot.x - TILESIZE//4, slot.y - TILESIZE//4, TILESIZE*1.5, TILESIZE*1.5), 2)
    def update(self):
        self.delay -= 1
        if self.delay < 0:
            if EventHandler.keydown(pygame.K_e):
                self.open = False

class FurnaceBlock(Tile):
    def __init__(self, groups, image: pygame.Surface, position: tuple, name: str = "default", type="block", flipped=0, durability: int = 20, hardness: int = 1, special_flags = None) -> None:
        super().__init__(groups, image, position, name, type, flipped, durability, hardness, special_flags)
        self.active = False
    
class ItemBlock(Tile):
    def __init__(self, groups, image: pygame.Surface, position: tuple, name: str = "default", type="block", flipped=0, durability: int = 20, hardness: int = 1, special_flags = None) -> None:
        super().__init__(groups, image, position, name, type, flipped, durability, hardness, special_flags)
        self.active = False
    def toggle(self, *args, **kwargs):
        self.active = not self.active

class DoorBlock(ItemBlock):
    def __init__(self, groups, image: pygame.Surface, position: tuple, name: str = "default", type="block", flipped=0, durability: int = 20, hardness: int = 1, special_flags = None) -> None:
        super().__init__(groups, image, position, name, type, flipped, durability, hardness, special_flags)
        self.og_img = image
        self.image = pygame.Surface.subsurface(image, pygame.Rect(0,0,TILESIZE, TILESIZE*2))
        self.rect = self.image.get_rect(bottomleft = (position[0], position[1]+TILESIZE))
        self.image_offset = 0
        self.active = True
    def toggle(self, player):
        super().toggle()
        player_position = player.rect.center
        self.image_offset = abs(self.image_offset - 1)
        self.image = pygame.Surface.subsurface(self.og_img, pygame.Rect(self.image_offset * TILESIZE, 0, TILESIZE, TILESIZE*2))
        if player_position[0] > self.rect.x:
            self.image = pygame.transform.flip(self.image, True, False)