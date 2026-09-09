import java.util.ArrayList;

public class MemoriaDinamica {

    public static void main (String[] args) {

        //arrasy list de cadena abstracto 
    ArrayList<String> frutas = new ArrayList<>();
        frutas.add("Mango");
        frutas.add("Manzana");
        frutas.add("Banana");
        frutas.add("Uvas");
        System.out.println(frutas); //imprime el contenido de toda la arraylist
        frutas.remove(0); //empieza a mostrar como es el manejo de la memoria dinámica
        frutas.remove(1);
        frutas.add("Sandia");
        System.out.println(frutas);
    }      
}
