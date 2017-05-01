public class Tulpa{
  public String Name;
  public int Age;
  public int Health;
  public int Hunger;
  public int Mood;
  public boolean Lived;
  public boolean Gender;//true for female, false for male
  
  public Tulpa(String I_Name, Boolean I_Gender){
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
    if(Lived){
      Health+=f.Nutrition;
      Mood+=f.Flavor;
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
