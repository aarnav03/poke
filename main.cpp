#include <iostream>

using namespace std;

enum types { fire = 0, water, electric, plant };
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
  bool alive() {
    if (hp > 0)
      return true;
    else
      return false;
  }
};
class pika : public PokeBase {
public:
  pika() : PokeBase(electric, "Pikachu", 35, 52) {}
  int atk1() { return atk * 0.9; }
  int atk2() { return atk * 1.0; }
  void atkshow() {
    cout << "Dash \n";
    cout << "Thunder Shock \n";
  }
};
class charmander : public PokeBase {
public:
  charmander() : PokeBase(fire, "Charmander", 39, 52) {}
  int atk1() { return atk * 0.9; }
  int atk2() { return atk * 1.2; }
  void atkshow() {
    cout << "Scratch \n";
    cout << "Ember \n";
  }
};
class bulba : public PokeBase {
public:
  bulba() : PokeBase(plant, "Bulbasaur", 45, 49) {}
  int atk1() { return atk * 0.9; }
  int atk2() { return atk * 1.1; }
  void atkshow() {
    cout << "1. Tackle \n";
    cout << "2. Vine Whip \n";
  }
};
class sqrt : public PokeBase {
public:
  sqrt() : PokeBase(water, "Squirtle", 44, 48) {}
  int atk1() { return atk * 0.8; }
  int atk2() { return atk * 1.1; }
  void atkshow() {
    cout << "1. Tackle \n";
    cout << "2. Water Gun \n";
  }
};

void battle(PokeBase &p1, PokeBase &p2) {
  int t = 1;
  while (p1.alive() && p2.alive()) {

    cout << p1.name << "hp " << p1.hp << endl;
    cout << p2.name << "hp" << p2.hp << endl;
    cout << "Choose attack: " << endl;
    p1.atkshow();
    cout << endl;
    int m, dmg;
    cin >> m;
    if (m == 1)
      dmg = p1.atk1();
    else
      dmg = p1.atk2();
    cout << p1.name << " attacks for " << dmg << endl;
    p2.damage(dmg);
    if (!p2.alive())
      break;
    // p2 stuff
    cout << "P2 choose \n";
    p2.atkshow();
    cin >> m;
    if (m == 1)
      dmg = p2.atk1();
    else
      dmg = p2.atk2();

    cout << "p2 attacks for " << dmg << endl;
    p1.damage(dmg);
  }

  if (p1.alive())
    cout << "Player 1 wins ";
  else
    cout << "Player 2 wins";
}

int main() {
  pika p1;
  sqrt p2;
  battle(p1, p2);
}
