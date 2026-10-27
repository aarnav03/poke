import os
import random
import time

RESET = "\033[0m"
LINE = "─" * 55

TYPES = {
    "fire": ("\033[2;31m", "\033[31m", "\033[91m"),
    "water": ("\033[2;34m", "\033[34m", "\033[94m"),
    "electric": ("\033[2;33m", "\033[33m", "\033[93m"),
    "plant": ("\033[2;32m", "\033[32m", "\033[92m"),
}

TYPE_CYCLE = ["fire", "plant", "electric", "water"]


def effectiveness(attacker_type, defender_type):
    a, d = TYPE_CYCLE.index(attacker_type), TYPE_CYCLE.index(defender_type)
    if d == (a + 1) % len(TYPE_CYCLE):
        return 1.35, "It's super effective!"
    if d == (a - 1) % len(TYPE_CYCLE):
        return 0.75, "It's not very effective..."
    return 1.0, None


# name, type, hp, atk,
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


def header(title):
    os.system("cls" if os.name == "nt" else "clear")
    print(f"{LINE}\n{title.center(55)}\n{LINE}\n")


def hp_line(p, hp=None):
    if hp is None:
        hp = p.hp
    else:
        hp = hp
    filled = hp * 25 // p.max_hp

    return f"{p.name:<12} HP [{'█' * filled}{'░' * (25 - filled)}] {hp}/{p.max_hp}"


def animate_hp(p, old_hp):
    for hp in range(old_hp - 1, p.hp - 1, -1):
        print("\r" + hp_line(p, hp), end="", flush=True)
        time.sleep(0.035)
    print()


def attack_animation(p):
    dark, dim, bright = TYPES[p.type]
    for pos in range(30):
        print(f"\r{' ' * pos}{dark}·{dim}▒{bright}███{RESET}\033[K", end="", flush=True)
        time.sleep(0.035)
    print()


def ask_int(prompt, lo, hi):
    while True:
        answer = input(prompt).strip()
        if answer.isdigit() and lo <= int(answer) <= hi:
            return int(answer)
        print(f"Please enter a number from {lo} to {hi}.")


def pick_pokemon(player):
    header("POKÉMON")
    for i, (name, type_, hp, *_) in enumerate(ROSTER, 1):
        print(f"  {i}. {name:<12} {type_.capitalize():<9} HP {hp}")
    print(f"\n{LINE}")
    choice = ask_int(f"\n{player}, choose your Pokémon: ", 1, len(ROSTER))
    return Pokemon(*ROSTER[choice - 1])


def take_turn(name, attacker, defender, is_cpu):
    print(f"\n── {name}'s turn ──")
    if is_cpu:
        time.sleep(0.6)
        move = 0 if random.random() < 1 / 3 else 1
    else:
        for i, (move_name, _) in enumerate(attacker.moves, 1):
            print(f"  {i}. {move_name}")
        move = ask_int("\nChoose move: ", 1, len(attacker.moves)) - 1

    multiplier, note = effectiveness(attacker.type, defender.type)
    damage = attacker.roll_damage(move, multiplier)
    attack_animation(attacker)
    print(f"  {attacker.name} used {attacker.moves[move][0]} for {damage} damage!")
    if note:
        print(f"  {note}")

    old_hp = defender.hp
    defender.hp = max(0, defender.hp - damage)
    animate_hp(defender, old_hp)
    time.sleep(0.7)

    if not defender.alive:
        print(f"\n{defender.name} fainted!")
        time.sleep(1)


def battle(players):
    """players: [(name, pokemon, is_cpu), (name, pokemon, is_cpu)]. Returns winner index."""
    header("BATTLE START")
    for name, mon, _ in players:
        print(f"{name}: {mon.name}")
    time.sleep(1)

    while True:
        for i, (name, mon, is_cpu) in enumerate(players):
            foe = players[1 - i][1]
            header("BATTLE")
            print(hp_line(players[0][1]))
            print(hp_line(players[1][1]))
            print(f"\n{LINE}")
            take_turn(name, mon, foe, is_cpu)
            if not foe.alive:
                return i


def main():
    os.system("")
    header("POKÉMON BATTLE")
    print(f"  1. Player vs Computer\n  2. Player vs Player\n\n{LINE}")
    vs_cpu = ask_int("\nChoose mode: ", 1, 2) == 1

    name1 = input("\nPlayer 1 name: ").strip() or "Player 1"
    p1 = pick_pokemon(name1)

    if vs_cpu:
        name2 = "Computer"
        p2 = Pokemon(*random.choice([s for s in ROSTER if s[0] != p1.name]))
    else:
        name2 = input("\nPlayer 2 name: ").strip() or "Player 2"
        p2 = pick_pokemon(name2)

    players = [(name1, p1, False), (name2, p2, vs_cpu)]
    name, mon, _ = players[battle(players)]

    header("RESULT")
    print(f"  {name} wins!\n  {mon.name} remains standing.\n\n{LINE}")


if __name__ == "__main__":
    main()
