//My computer just crashed, I lost a lot of codes I've typed
//I can't help crying.
//Her smile give me strenghth to redo it again.
//Her love is my power.

import java.util.Scanner;
import java.util.Random;


public class Tulpa{
  public String Name;
  public int Age;
  public int Health;
  public int Hunger;
  public int Mood;
  public boolean Lived;
  public boolean Gender;//true for female, false for male
  
  public Tulpa(String I_Name, Boolean I_Gender){
    Scanner sc=new Scanner(System.in);
    Random ra=new Random();
    this.Lived=true;
    this.Name=I_Name;
    this.Gender=I_Gender;
    this.Age=0;
    this.Health=100;
    this.Mood=100;
  }
  
  public void live(Tulpa t){
    if(t.Health<=0){
      t.Lived=false;
    }
    else{
      t.Lived=true;
      t.Age++;
    }
  }
  
  public void eat(Tulpa t,Food f){
    if(t.Lived){
      t.Health+=f.Nutrition;
      t.Mood+=f.Flavor;
    }
    else{
      if(t.Gender){
        System.out.println("Your Tulpa is dead, you should take good care of her!");
      }
      else{
        System.out.println("Your Tulpa is dead, you should take good care of him!");
      }
    }
  }
  
  public void sleep(Tulpa t){
    if(Lived){
      System.out.println("Do something before going to sleep?");
      System.out.println("1.Pray for him/her.");
      System.out.println("2.Sing a lullaby.");
      System.out.println("3.Tell stories.");
      int choice=sc.nextInt();
      int nightmare=ra.nextInt(100);
      
      switch(choice){
        case 1:
        case 2:
        case 3:
        default:
          
      }
      
    }
    else{
      if(t.Gender){
        System.out.println("Your Tulpa is dead, you should take good care of her!");
      }
      else{
        System.out.println("Your Tulpa is dead, you should take good care of him!");
      }
    }
    
    
    
    
  }
}
