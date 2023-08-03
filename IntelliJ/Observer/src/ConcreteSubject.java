import java.util.ArrayList;
import java.util.List;

public class ConcreteSubject  implements Subject{

    private List<Observer> observers;

    public ConcreteSubject(){
        observers = new ArrayList<Observer>();
    }

    public void removeObserver(Observer o) {
        observers.remove(o);
    }

    public void registerObserver(Observer o) {
        observers.add(o);
    }

    public void notifyObservers(){
        for (Observer o : observers) o.update();
    }
}
