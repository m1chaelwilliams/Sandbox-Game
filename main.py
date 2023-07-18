import pygame
import sys
from globals import *
from world.scene import Scene
from utils.events import EventHandler
from ui.menus import StartMenu, WorldSelect

class Game:
    def __init__(self) -> None:
        pygame.init()
        # self.screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
        self.screen = pygame.display.set_mode((1280, 720))
        Game.SCREENWIDTH = self.screen.get_width()
        Game.SCREENHEIGHT = self.screen.get_height()

        self.clock = pygame.time.Clock()

        self.running = True

        # world key
        self.world_key = ''

        self.scene = Scene(self)
        # state management
        self.states = {
            'overworld':self.scene,
            'start':StartMenu(self),
            'world_select':WorldSelect(self),
        }
        self.active_state = 'start'
    def start(self) -> None:
        self.loop()
        self.close()
    def loop(self) -> None:
        while self.running:
            self.update()
            self.draw()
    def update(self) -> None:
        if self.active_state == "quit":
            self.running = False
        EventHandler.poll_events()
        if EventHandler.is_closed_requested():
            self.running = False
        if EventHandler.keydown(pygame.K_q):
            self.running = False
        if EventHandler.keydown(pygame.K_p): # screenshot
            with open('screenshots/screenshot.txt', 'r') as f:
                num = int(f.readline())
                print(num)
                
            pygame.image.save(self.screen, f'screenshots/save_{num}.png')
            with open('screenshots/screenshot.txt', 'w') as f:
                f.write(str(num + 1))

        self.states[self.active_state].update()
    def draw(self) -> None:
        self.states[self.active_state].draw()
        pygame.display.update()
        self.clock.tick(FPS)
    def close(self) -> None:
        self.states[self.active_state].close()
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.start()