#include <cstdlib>
#include <ctime>
#include <iostream>
#include <string>
using namespace std;

enum types { fire = 0, water, electric, plant };

string typeIcon(int t) {
  switch (t) {
  case fire:
    return "󰈸";
  case water:
    return "󰖌";
  case electric:
    return "󱐋";
  case plant:
    return "";
  default:
    return "?";
  }
}

class PokeBase {
public:
  int type;
  string name;
  int hp;
  int atk;

  PokeBase(types t, string n, int h, int a) {
    type = t;
    name = n;
    hp = h;
    atk = a / 3;
  }

  virtual int atk1() = 0;
  virtual int atk2() = 0;
  virtual void atkshow() = 0;

  void damage(int dmg) {
    hp -= dmg;
    if (hp < 0)
      hp = 0;
  }

  bool alive() const { return hp > 0; }

  string label() const { return typeIcon(type) + " " + name; }
};

class Pikachu : public PokeBase {
public:
  Pikachu() : PokeBase(electric, "Pikachu", 35, 52) {}
  int atk1() { return (int)(atk * 0.9f); }
  int atk2() { return (int)(atk * 1.0f); }
  void atkshow() {
    cout << "  1. Dash\n";
    cout << "  2. Thunder Shock\n";
  }
};

class Charmander : public PokeBase {
public:
  Charmander() : PokeBase(fire, "Charmander", 39, 52) {}
  int atk1() { return (int)(atk * 0.9f); }
  int atk2() { return (int)(atk * 1.2f); }
  void atkshow() {
    cout << "  1. Scratch\n";
    cout << "  2. Ember\n";
  }
};

class Bulbasaur : public PokeBase {
public:
  Bulbasaur() : PokeBase(plant, "Bulbasaur", 45, 49) {}
  int atk1() { return (int)(atk * 0.9f); }
  int atk2() { return (int)(atk * 1.1f); }
  void atkshow() {
    cout << "  1. Tackle\n";
    cout << "  2. Vine Whip\n";
  }
};

class Squirtle : public PokeBase {
public:
  Squirtle() : PokeBase(water, "Squirtle", 44, 48) {}
  int atk1() { return (int)(atk * 0.8f); }
  int atk2() { return (int)(atk * 1.1f); }
  void atkshow() {
    cout << "  1. Tackle\n";
    cout << "  2. Water Gun\n";
  }
};

void line() { cout << "\n  ────────────────────────\n"; }

int input() {
  int m;
  cout << "  > ";
  cin >> m;
  if (m != 1 && m != 2)
    m = 1;
  return m;
}

PokeBase *makePokemon(int choice) {
  switch (choice) {
  case 1:
    return new Pikachu();
  case 2:
    return new Charmander();
  case 3:
    return new Bulbasaur();
  case 4:
    return new Squirtle();
  default:
    return new Pikachu();
  }
}
int crit(int d) { return d - 5 + (rand() % 11); }

void showRoster() {
  cout << "  1. 󱐋  Pikachu    (HP: 35)\n";
  cout << "  2. 󰈸  Charmander (HP: 39)\n";
  cout << "  3.   Bulbasaur  (HP: 45)\n";
  cout << "  4. 󰖌  Squirtle   (HP: 44)\n";
}

int selectPokemon(const string &playerName) {
  int choice;
  cout << "\n" << playerName << ", choose your Pokemon:\n";
  showRoster();
  cout << "  > ";
  cin >> choice;
  if (choice < 1 || choice > 4)
    choice = 1;
  return choice;
}

void battle(PokeBase &p1, PokeBase &p2, const string &name1,
            const string &name2, bool vsComputer) {

  cout << "\n    BATTLE START  \n";
  cout << "  " << name1 << "'s " << p1.label() << " vs " << name2 << "'s "
       << p2.label() << "\n";

  while (p1.alive() && p2.alive()) {
    line();
    cout << "  " << name2 << "'s " << p2.label() << "   HP: " << p2.hp
         << "\n\n";
    cout << "  " << name1 << "'s " << p1.label() << "   HP: " << p1.hp << "\n";
    line();

    cout << "\n" << name1 << ", choose your move:\n";
    p1.atkshow();
    int m = input();

    int dmg = (m == 1) ? p1.atk1() : p1.atk2();
    dmg = crit(dmg);
    cout << "\n  " << p1.name << " attacked! Dealt " << dmg << " damage.\n";
    p2.damage(dmg);
    if (!p2.alive())
      break;

    cout << "\n";
    if (vsComputer) {
      m = (rand() % 3 == 0) ? 1 : 2;
      cout << "  " << name2 << "'s " << p2.name << " is thinking...\n";
    } else {
      cout << name2 << ", choose your move:\n";
      p2.atkshow();
      m = input();
    }

    dmg = (m == 1) ? p2.atk1() : p2.atk2();
    dmg = crit(dmg);
    cout << "  " << p2.name << " attacked! Dealt " << dmg << " damage.\n";
    p1.damage(dmg);
  }

  line();
  if (p1.alive())
    cout << "  " << name1 << "'s " << p1.name << " wins!  \n";
  else
    cout << "  " << name2 << "'s " << p2.name << " wins!  \n";
  line();
}

int main() {
  srand(time(0));

  cout << "   POKE FIGHT\n";
  cout << "  ────────────────────────\n\n";

  int mode;
  cout << "Select mode:\n";
  cout << "  1. 1 Player vs Computer\n";
  cout << "  2. 2 Players\n";
  cout << "  > ";
  cin >> mode;
  bool vsComputer = (mode == 1);

  string name1;
  cout << "\nPlayer 1, enter your name: ";
  cin >> name1;

  int choice1 = selectPokemon(name1);
  PokeBase *p1 = makePokemon(choice1);

  string name2;
  PokeBase *p2;

  if (vsComputer) {
    name2 = "CPU";
    int cpuChoice;
    do {
      cpuChoice = (rand() % 4) + 1;
    } while (cpuChoice == choice1);
    p2 = makePokemon(cpuChoice);
    cout << "\n  CPU chose " << p2->label() << "!\n";
  } else {
    cout << "\nPlayer 2, enter your name: ";
    cin >> name2;
    int choice2 = selectPokemon(name2);
    p2 = makePokemon(choice2);
  }

  battle(*p1, *p2, name1, name2, vsComputer);

  delete p1;
  delete p2;
  return 0;
}
