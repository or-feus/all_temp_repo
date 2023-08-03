public class MainObserver implements Observer{

    public ConcreteSubject concreteSubject;
    public Dorothy dorothy;

    public MainObserver(){
        dorothy = new Dorothy();
    }

    public void printapple(){
        System.out.println(dorothy.apple);
    }

    public void update(){
    }
}
