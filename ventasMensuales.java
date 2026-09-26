import java.util.Arrays;

public class ventasMensuales {

    private static final String[] MESES = {
            "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
            "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
    };

    private static final String[] DEPARTAMENTOS = {"Ropa", "Deportes", "Jugueteria"};

    private final double[][] ventas;

    public ventasMensuales() {
       
        this.ventas = new double[MESES.length][DEPARTAMENTOS.length];
    }

    private int obtenerIndiceMes(String mes) {
        String mesNormalizado = capitalizar(mes.trim());
        for (int i = 0; i < MESES.length; i++) {
            if (MESES[i].equals(mesNormalizado)) {
                return i;
            }
        }
        throw new IllegalArgumentException("El mes '" + mes + "' no es válido.");
    }

    private int obtenerIndiceDepartamento(String departamento) {
        String deptoNormalizado = capitalizar(departamento.trim()).replace("í", "i");
        for (int i = 0; i < DEPARTAMENTOS.length; i++) {
            if (DEPARTAMENTOS[i].replace("í", "i").equals(deptoNormalizado)) {
                return i;
            }
        }
        throw new IllegalArgumentException("El departamento '" + departamento + "' no es válido.");
    }

    private String capitalizar(String texto) {
        if (texto.isEmpty()) return texto;
        return texto.substring(0, 1).toUpperCase() + texto.substring(1).toLowerCase();
    }

    // -------- 1. Insertar --------
    public void insertarVenta(String mes, String departamento, double monto) {
        if (monto < 0) {
            throw new IllegalArgumentException("El monto de la venta no puede ser negativo.");
        }
        int fila = obtenerIndiceMes(mes);
        int columna = obtenerIndiceDepartamento(departamento);
        ventas[fila][columna] = monto;
        System.out.printf("[OK] Venta insertada: %s - %s = $%.2f%n", mes, departamento, monto);
    }

    // -------- 2. Buscar --------
    public double buscarVenta(String mes, String departamento) {
        int fila = obtenerIndiceMes(mes);
        int columna = obtenerIndiceDepartamento(departamento);
        double monto = ventas[fila][columna];
        System.out.printf("[BUSQUEDA] %s - %s: $%.2f%n", mes, departamento, monto);
        return monto;
    }

    // -------- 3. Eliminar --------
    public void eliminarVenta(String mes, String departamento) {
        int fila = obtenerIndiceMes(mes);
        int columna = obtenerIndiceDepartamento(departamento);
        double montoAnterior = ventas[fila][columna];
        ventas[fila][columna] = 0;
        System.out.printf("[OK] Venta eliminada: %s - %s (era $%.2f)%n", mes, departamento, montoAnterior);
    }

    // -------- Utilidad extra: mostrar la tabla completa --------
    public void mostrarTabla() {
        StringBuilder encabezado = new StringBuilder(String.format("%-12s", ""));
        for (String depto : DEPARTAMENTOS) {
            encabezado.append(String.format("%12s", depto));
        }
        System.out.println(encabezado);
        System.out.println("-".repeat(encabezado.length()));

        for (int i = 0; i < MESES.length; i++) {
            StringBuilder fila = new StringBuilder(String.format("%-12s", MESES[i]));
            for (int j = 0; j < DEPARTAMENTOS.length; j++) {
                fila.append(String.format("%12.2f", ventas[i][j]));
            }
            System.out.println(fila);
        }
    }

    public static void main(String[] args) {
        ventasMensuales sistema = new ventasMensuales();

        // 1. Insertar ventas
        sistema.insertarVenta("Enero", "Ropa", 1500);
        sistema.insertarVenta("Enero", "Deportes", 2300);
        sistema.insertarVenta("Enero", "Jugueteria", 800);
        sistema.insertarVenta("Febrero", "Ropa", 1750);
        sistema.insertarVenta("Diciembre", "Jugueteria", 5200);

        System.out.println("\n--- Tabla de ventas ---");
        sistema.mostrarTabla();

        // 2. Buscar una venta
        System.out.println("\n--- Búsqueda ---");
        sistema.buscarVenta("Enero", "Deportes");

        // 3. Eliminar una venta
        System.out.println("\n--- Eliminación ---");
        sistema.eliminarVenta("Enero", "Ropa");

        System.out.println("\n--- Tabla después de eliminar ---");
        sistema.mostrarTabla();
    }
}