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


def resolve_attack(att: Combatant, dfn: Combatant, rng: random.Random) -> Event:
     """One attack: hit roll, damage variance, crit roll. Mutates defender hp."""
     target = "enemy" if dfn.name != "Hero" else "player"
     if rng.random() > clamp(att.acc - dfn.eva, 0.10, 0.95):
          return Event("miss", target, 0, f"{att.name} misses {dfn.name}")
     crit = rng.random() < att.crit
     raw = att.atk * rng.uniform(0.8, 1.2) * (175 if crit else 1.0)
     armor = dfn.defn * (2 if dfn.defending else 1)
     dmg = max(1, round(raw - armor))
     dfn.hp = max (0, dfn.hp - dmg)
     word = "CRITS" if crit else "hits"
     return Event("crit" if crit else "hit", target, dmg, f"{att.name} {word} {dfn.name} for {dmg}")

def wave_budget(wave: int) -> float:
    return 2 + 0.9 * wave ** 1.05

def enemy_scale(wave: int) -> float:
    return 1 + 0.03 * (wave - 1)

class Game:
    def __init__(self, seed: int | None = None):
        self.seed
        self.wave

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