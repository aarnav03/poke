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
    atk = a;
  }
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
};
class charmander : public PokeBase {
public:
  charmander() : PokeBase(fire, "Charmander", 39, 52) {}
  int atk1() { return atk * 0.9; }
  int atk2() { return atk * 1.2; }
};
class bulba : public PokeBase {
public:
  bulba() : PokeBase(plant, "Bulbasaur", 45, 49) {}
  int atk1() { return atk * 0.9; }
  int atk2() { return atk * 1.1; }
};
class sqrt : public PokeBase {
public:
  sqrt() : PokeBase(water, "Squirtle", 44, 48) {}
  int atk1() { return atk * 0.8; }
  int atk2() { return atk * 1.1; }
};

void battle(PokeBase &p1, PokeBase &p2) {
  while (p1.alive() && p2.alive()) {
    cout << p1.name << p1.hp << endl;
    cout << p2.name << p2.hp << endl;
  }
}

int main() {
  pika p1;
  sqrt p2;
  battle(p1, p2);
}
