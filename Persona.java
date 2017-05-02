import java.util.Random;

public class Persona{
  
  public int growth;
  public String tag[7];
  public Persona(Tulpa t){
    this.growth=0;
    if(t.Health>=50){
        if(t.Mood>=50){
          this.tag[0]="Optimism";
        }
        else{
          this.tag[0]="Realism";
        }
      }
      else{
        if(t.Mood>=50){
          this.tag[0]="Romantism"
        }
        else{
          this.tag[0]="Pessimism"
        }
      }
    
      
    Random ra=new Random();
  
  
  }
  
  
  
  public void action(Tulpa.t){
    System.out.println("She want to do sth...");
    
  
  
  }
  
  
  public boolean tag_check(String Input_Tag){
    for(int i=0;i<this.tag.length;i++){
      if(this.tag[i].equals(Input_Tag)){
        return true;
      }
    }
    return false;
  }
  
  public void event(){
  
  
  }
  
}
