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
        self.seed = seed if seed is not None else random.randrange(1_000_000)
        self.wave = 0
        self.state = "player"
        self.events: list[Event] = []
        self.log: deque[str] = deque(maxlen=6)
        self.kills = 0
        self.player = Combatant("Hero", 60, 11, 2, acc=0.92, eva=0.08, crit=0.12, color=(240, 210, 90), potions=3)
        self.queue: list[Combatant] = []
        self.enemy: Combatant | None = None
        self.rewards: list[tuple[str, callable]] = []
        self.rng = random.Random()
        self.start_wave()

        
    def emit(self, ev: Event):
        self.events.append(ev)
        if ev.text:
            self.log.append(ev.text)

    def start_wave(self):
        self.wave += 1
        spawn_rng = random.Random(f"{self.seed}-spawn{self.wave}")
        self.rng = random.Random(f"{self.seed}-combat-{self.wave}")
        budget = wave_budget(self.wave)
        pool = [t for t in ENEMY_TYPES if t[9] <= self.wave]
        scale = enemy_scale(self.wave)
        self.que = []
        while True:
            affordable = [t for t in pool if t[1] <= budget]
            if not affordable:
                break

            t= spawn_rng.choices(affordable, [1 + t[1] * self.wave / 8 for t in affordable])[0]
            budget -= t[1]
            name, _, hp, atk, dfn, acc, eva, crit, color, _ = t
            self.queue.append(Combatant(name, round(hp * scale), round(atk * scale), round(dfn*scale), acc, eva, crit, color))

        self.enemy = self.queue.pop(0)
        self.player.defending = False
        self.state = "player"
        self.emit(Event("wave_start", "", self.wave, f"-- Wave {self.wave}: {len(self.queue) + 1} enemies --"))

    def enemy_down(self):
        self.kills += 1
        self.emit(Event("death", "enemy", 0, f"{self.enemy.name} defeated"))
        if self.queue:
            self.enemy = self.queue.pop(0)
            self.state = "player"
        else:
            self.emit(Event("wave_clear", "", self.wave, f"Wave {self.wave} cleared!"))
            heal = round(self.player.max_hp * 0.40)
            self.player.hp = min(self.player.max_hp, self.player.hp + heal)
            self.rewards = random.Random(f"{self.seed}-reward-{self.wave}").sample(REWARD, 3)
            self.state = "reward"

    


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