public class Persona{
  public int growth;
  public String tag[];
  public void action(){
    
  
  
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
