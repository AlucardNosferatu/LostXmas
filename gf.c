//forked from https://github.com/HyungJu/GirlFriend
#include <stdio.h>
typedef struct friend F;
struct friend{
  char* name;
  int age;
  F* Lover;
};

int main() {
  F Scrooge;
  Scrooge.age=24;
  Scrooge.name="Scrooge";
  F Carol;
  Carol.age=24;
  Carol.name="Carol";
  Scrooge.Lover=&Carol;
  Carol.Lover=&Scrooge;
  printf("%s loves %s very very very much.",Carol.Lover->name,Scrooge.Lover->name);
  return 0;
}
