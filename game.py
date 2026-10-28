import random

TYPE_CYCLE = ["fire", "plant", "electric", "water"]


def effectiveness(attacker_type, defender_type):
    a, d = TYPE_CYCLE.index(attacker_type), TYPE_CYCLE.index(defender_type)
    if d == (a + 1) % len(TYPE_CYCLE):
        return 1.35, "It's super effective!"
    if d == (a - 1) % len(TYPE_CYCLE):
        return 0.75, "It's not very effective..."
    return 1.0, None


# name, type, hp, atk, moves
ROSTER = [
    ("Pikachu", "electric", 35, 52, (("Dash", 0.9), ("Thunder Shock", 1.0))),
    ("Charmander", "fire", 39, 52, (("Scratch", 0.9), ("Ember", 1.2))),
    ("Bulbasaur", "plant", 45, 49, (("Tackle", 0.9), ("Vine Whip", 1.1))),
    ("Squirtle", "water", 44, 48, (("Tackle", 0.8), ("Water Gun", 1.1))),
]


class Pokemon:
    def __init__(self, name, type_, hp, atk, moves):
        self.name, self.type, self.moves = name, type_, moves
        self.hp = self.max_hp = hp
        self.atk = atk // 3

    @property
    def alive(self):
        return self.hp > 0

    def roll_damage(self, move, multiplier=1.0):
        base = int(self.atk * self.moves[move][1] * multiplier)
        return max(1, base + random.randint(-5, 5))

    def to_dict(self):
        return {
            "name": self.name,
            "type": self.type,
            "hp": self.hp,
            "max_hp": self.max_hp,
            "moves": [m[0] for m in self.moves],
        }


def roster_info():
    return [{"name": n, "type": t, "hp": hp} for n, t, hp, *_ in ROSTER]


def random_cpu_pick(avoid_name):
    return random.choice([i for i, s in enumerate(ROSTER) if s[0] != avoid_name])


def cpu_choose_move():
    return 0 if random.random() < 1 / 3 else 1


class Battle:

    def __init__(self, players):
        self.players = players
        self.turn = 0
        self.winner = None

    def _attack(self, move):
        name, attacker, _ = self.players[self.turn]
        foe = self.players[1 - self.turn][1]

        multiplier, note = effectiveness(attacker.type, foe.type)
        damage = attacker.roll_damage(move, multiplier)
        old_hp = foe.hp
        foe.hp = max(0, foe.hp - damage)

        event = {
            "attacker": self.turn,
            "trainer": name,
            "pokemon": attacker.name,
            "type": attacker.type,
            "move": attacker.moves[move][0],
            "damage": damage,
            "note": note,
            "old_hp": old_hp,
            "new_hp": foe.hp,
            "fainted": not foe.alive,
            "foe": foe.name,
        }
        if not foe.alive:
            self.winner = self.turn
        else:
            self.turn = 1 - self.turn
        return event

    def play(self, move):
        attacker = self.players[self.turn][1]
        if self.winner is not None:
            raise ValueError("The battle is over.")
        if self.players[self.turn][2]:
            raise ValueError("It's the computer's turn.")
        if not 0 <= move < len(attacker.moves):
            raise ValueError("Unknown move.")

        events = [self._attack(move)]
        while self.winner is None and self.players[self.turn][2]:
            events.append(self._attack(cpu_choose_move()))
        return events

    def to_dict(self):
        return {
            "players": [
                {"name": n, "pokemon": p.to_dict(), "is_cpu": cpu}
                for n, p, cpu in self.players
            ],
            "turn": self.turn,
            "winner": self.winner,
        }
