public class Main {
    public static void main(String[] args) {
        Color zz = new Color(1, 2, 3);
        Color dd = zz;
        Color bb = new Color(2, 3, 4);
        Color cc = zz.Change(bb);
        System.out.println(dd == zz);
    }
}
