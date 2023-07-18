import pygame
from globals import *

class Animation:
    def __init__(self, spritesheet: pygame.Surface, size: tuple, speed: int = 10) -> None:
        self.frames = []
        print(spritesheet.get_width(), spritesheet.get_height())
        for row in range(int(spritesheet.get_height() / size[1])):
            for col in range(int(spritesheet.get_width() / size[0])):
                self.frames.append(pygame.Surface.subsurface(spritesheet, pygame.Rect(col*size[0], row*size[1], size[0], size[1])))
        self.active_frame = 0
        self.speed = speed
        self.counter = speed
    def update(self) -> None:
        self.counter -= 1
        if self.counter < 0:
            self.counter = self.speed
            self.active_frame += 1
        if self.active_frame > len(self.frames)-1:
            self.active_frame = 0
    def get_frame(self) -> pygame.Surface:
        return self.frames[self.active_frame]

class AnimationManager:
    def __init__(self, animations: dict, active_animation: str) -> None:
        self.animations = animations
        self.active_animation = active_animation
    def get_active_frame(self) -> pygame.Surface:
        return self.animations[self.active_animation].get_frame()
    def set_animation(self, animation: str):
        self.active_animation = animation
        self.animations[self.active_animation].active_frame = 0
    def update(self):
        self.animations[self.active_animation].update()