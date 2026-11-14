import pygame
import random
import math

class Combatant:
    name: str
    max_hp: int
    atk: int
    defn: int
    acc: float = 0.90
    eva: float = 0.05
    crit: float = 0.10
    color: tuple = (200, 200, 200)
    hp: int = 0
    defending: bool = False
    potions: int = 0

    def __post_init__(self):
        if not self.hp:
            self.hp = self.max_hp

    def alive(self) -> bool:
        return self.hp > 0

class Event:
    kind: str
    target: str =""
    value: int = 0
    text: str = ""


ENEMY_TYPES = [
    ("Skeleton", 1, 22, 5, 1, 0.90, 0.10, 0.10, (255, 255, 255), 1),
    ("Wizard", 3, 26, 12, 1, 0.95, 0.15, 0.15, (0, 0, 255), 3),
    ("Orc", 4, 70, 11, 3, 0.80, 0.00, 0.08, (0, 255, 0), 5),
]

def clamp(x, lo, hi):
    return max(lo, min(hi, x))


    def main():
        pygame.init()
        pygame.display.set_caption("RNG Battle")
        resoution = (800, 600)
        screen = pygame.display.set_mode(resoution)
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
        pygame.quit()


    if __name__ == "__main__":
        main()