import javax.swing.JOptionPane;

public class MemoriaEstatica {
//asignamos y no cambia durante la ejecución del programa.
    public static void main(String[] args) {

        int calificaciones [] = new int[5];

        for(int i=0; i<5; i++)
        {
            calificaciones[i] = Integer.parseInt(JOptionPane.showInputDialog(null, "Captura la " + "calificacion: "));
        }
    }
}