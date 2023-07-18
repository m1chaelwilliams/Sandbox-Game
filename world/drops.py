import pygame
from globals import *
from inventory.inventory import Inventory

class Drop(pygame.sprite.Sprite):
    def __init__(self, name: str, quantity: int, position: tuple, textures: dict[str, pygame.Surface], groups: list[pygame.sprite.Group], block_group) -> None:
        super().__init__(groups)
        print(len(groups[0].sprites()))
        self.name = name
        self.quantity = quantity
        self.block_group = block_group

        # image
        self.image = textures[self.name]
        self.image = pygame.transform.scale_by(self.image, 0.5)
        self.rect = self.image.get_rect(topleft = (position[0]-TILESIZE//4, position[1]-TILESIZE//4))

        # vars
        self.velocity = pygame.math.Vector2()
        self.lifespan = 1000
        self.grounded = False
        self.active = False

        self.seated_block = None
        self.column = []
        self.first_collision = False
    def pickup(self, inventory: Inventory):
        self.quantity = inventory.add_item(self.name, self.quantity)
        if self.quantity < 1:
            self.kill()
    def move(self):
        if not self.grounded:
            self.velocity.y += 0.3
            self.rect.y += self.velocity.y
            if not self.first_collision:
                self.check_collisions()
            else:
                self.check_column_collision()
    def update(self):
        self.lifespan -= 1
        if self.lifespan < 0:
            self.kill()
        self.active = True
        self.move()
        if self.seated_block:
            if not self.seated_block.active:
                self.grounded = False
    def check_collisions(self):
        for block in self.block_group:
            if block.rect.centerx == self.rect.centerx:
                self.column.append(block)
        self.first_collision = True
    def check_column_collision(self):
        for block in self.column:
            if block.active and block.rect.colliderect(self.rect):
                if self.velocity.y > 0:
                    self.rect.bottom = block.rect.top
                    self.velocity.y = 0
                    self.grounded = True
                    self.seated_block = block