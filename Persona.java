import java.util.Random;

public class Persona{
  
  public int growth;
  public String tag[];
  public Persona(){
    
  
  
  }
  
  
  
  public void action(Tulpa.t){
    System.out.println("She want to do sth...");
    
  
  
  }
  
  
  public boolean tag_check(String Input_Tag){
    for(int i=1;i<this.tag.length;i++){
      if(this.tag[i].equals(Input_Tag)){
        return true;
      }
    }
    return false;
  }
  
  public void event(){
  
  
  }
  
}
