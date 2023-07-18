import pygame

class EventHandler:
    def __init__(self) -> None:
        EventHandler.events = pygame.event.get()
    @staticmethod
    def poll_events() -> None:
        EventHandler.events = pygame.event.get()
    @staticmethod
    def keydown(key):
        for e in EventHandler.events:
            if e.type == pygame.KEYDOWN:
                if e.key == key:
                    return True
        return False
    @staticmethod
    def is_closed_requested() -> bool:
        for e in EventHandler.events:
            if e.type == pygame.QUIT:
                return True
        return False
    def scroll_wheel_up() -> bool:
        for e in EventHandler.events:
            if e.type == pygame.MOUSEBUTTONDOWN:
                if e.button == 4:
                    return True
        return False
    def scroll_wheel_down() -> bool:
        for e in EventHandler.events:
            if e.type == pygame.MOUSEBUTTONDOWN:
                if e.button == 5:
                    return True
        return False
    def clicked(button: int = 1): # 1 = left, 2 = right
        for e in EventHandler.events:
            if e.type == pygame.MOUSEBUTTONDOWN:
                if e.button == button:
                    return True
        return False