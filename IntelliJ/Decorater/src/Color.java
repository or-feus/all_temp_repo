public class Color {
    public static int _red;
    public static int _green;
    public static int _blue;

    public Color(int red, int green, int blue) {
        this._red = red;
        this._green = green;
        this._blue = blue;
    }

    public Color Change(Color other) {
        return new Color(other._red, other._green, other._blue);
    }

    public void colorPrint(){
        System.out.println(this._red + "z: " + this._green + " " + this._blue);
    }
}