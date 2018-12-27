//forked from https://github.com/henexekrar
#include <cstdlib>
#include <iostream>
#include <string>

using namespace std;

class GirlFriend {

   private:
      string name;
      
      int age; 
      double weight; //in KG
      double height; //in cm
     
      int type; //personalities
      //1 for introversive person
      //-1 for outgoing person
      int thought; //thinking methodologies
      //1 for emotional person
      //-1 for rational person
      int relationship;// Something that you cherish for your whole life.
      int mood;// if you really love her, you should prevent her from crying.
      bool pregnant;
      bool inloved;
      
   public:
      GrilFriend () {
         name = new string("Mikasa");
         age = 17;
         weight = 45;
         height = 163;
         type=1;
         thought=-1;
         relationship=0;
         mood=0;
         pregnant = false;
         inloved=false;
      }
      
      ~GirlFriend() {}     
      void talk (){
         cout << "What do you want to talk?"<< endl;
         cout << "1.Express your love."<< endl;
         cout << "2.Ask for her feelings."<< endl;
         cout << "3.Tell her your affliction"<< endl;
         cout << "4.Share news and anecdotes with her"<< endl;
         cin >> a;
         switch (a){
            case 1:
               if (relationship>=50){
                  cout<<"I love you as well, Darling!"<< endl;
                  relationship++;
                  inloved=true;
               }
               if (relationship<50&&relationship>=25){
                  cout<<"But I haven't known you yet?!"<< endl;
                  relationship--;
               }
               if (relationship<25){
                  cout<<"FUCK OFF YOU WEIRDO"<< endl;
                  relationship=-10;
               }
            case 2:
               if (relationship<25){
                  cout<<"I'm fine, thanks."<< endl;
                  relationship++;
                  if (thought>0){
                     relationship++;
                     mood++;
                  }
               }
               if (relationship<50&&relationship>=25){
                  cout<<"I am quite worrying about the incoming quizz..."<< endl;
                  relationship++;
                  if (thought<0){
                     relationship++;
                     if (mood<0){
                        mood=0;
                     }
                     if (mood>=0){
                        mood++;
                     }
                  }
               }
               if (relationship>=50){
                  if (inloved){
                     cout<<"I love you as well, Darling!"<< endl;
                     relationship++;
                     mood++;
                  }
                  else{
                     cout<<"I've fallen in love with a dull guy..."<< endl;
                     relationship--;
                  }
               }
            case 3:
               if (relationship>=50){
                  if (inloved) {
                     if (thought>=0){
                        cout<<"Come on, I am on your side!"<< endl;
                     }
                     else {
                        cout<<"What you shoud do is......"<< endl;
                        cout<<"if you need any further help, just call me."<< endl;
                     }
                  }
                  else {
                  }
               }
               if (relationship<50&&relationship>=25){
                  cout<<"Oh, God bless you!"<< endl;
                  if (thought>0){
                     relationship++;
                  }
               }
               if (relationship<25){
                  cout<<"So what?"<< endl;
               }
            case 4:
               if (relationship>0){
                  if (mood>0) {
                     cout<<"23333"<<endl;
                     relationship++;
                     mood++;
                  }
                  else{
                     cout<<"That isn't funny at all"<<endl;
                     relationship--;
                  }
               }
            default:cout<<"Pardon?"<< endl;
         }
      }
      void gettingAlongWith (attitude){
         if (type==1) {
         relationship+=(attitude*mood);
         }
         if (type==-1) {
         relationship-=(attitude*mood);
         }
      }
      void resonance () {
         if (thought==1) {
         mood--;
         }
         if (thought==-1) {
         mood++;
         }
      }
      void flirt () {
         if (thought==1) {
         mood++;
         }
         if (thought==-1) {
         mood--;
         }
      }
      void gettingOld () {
         age++;
         cout << name << " is now " << age << " years old!" << endl;
      }
      
      void prprpr () {
         weight = weight * 0.99;
         cout << "You just prprpr with " << name << " and she lost weight." << endl;
         
         if (rand() % 100 == 1) {
            pregnant = true;
            cout << "Oh no " << name << " is pregnant!" << endl;
            cout << "You are a true father from now on." << endl;
         }
      }
      
      void moe () {
         cout << name << " is so moe!" << endl;
      }
};

int main (void) {

   GirlFriend gf = new GirlFriend();
    int attitude = 0;
      //1 for positive
      //-1 for negative
   return 0;
}
