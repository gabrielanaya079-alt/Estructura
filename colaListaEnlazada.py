from abc import ABC, abstractmethod


class Order:
    def __init__(self, qtty, cliente):
        self.__cliente = cliente
        self.__qtty = qtty

    def get_qtty(self):
        return self.__qtty

    def get_cliente(self):
        return self.__cliente

    def print(self):
        print("    Cliente: " + str(self.get_cliente()))
        print("    Cantidad: " + str(self.get_qtty()))
        print("    ------------")

class QueueInterface(ABC):
    @abstractmethod
    def size(self):
        """Devuelve el número de elementos en la cola."""

    @abstractmethod
    def is_empty(self):
        """True si la cola está vacía, False en otro caso."""

    @abstractmethod
    def front(self):
        """Devuelve el primer elemento SIN quitarlo. None si está vacía."""

    @abstractmethod
    def enqueue(self, info):
        """Añade un nuevo elemento al final de la cola."""

    @abstractmethod
    def dequeue(self):
        """Devuelve el primer elemento y LO QUITA. None si está vacía."""

class Node:
    def __init__(self, info):
        self.__info = info    
        self.__next = None    

    def get_info(self):
        return self.__info

    def get_next(self):
        return self.__next

    def set_next(self, next_node):
        self.__next = next_node

class Queue(QueueInterface):
    def __init__(self):
        self.__top = None     
        self.__last = None    
        self.__size = 0

    def size(self):
        return self.__size

    def is_empty(self):
        return self.__size == 0

    def front(self):
        if self.is_empty():
            return None
        return self.__top.get_info()

    def enqueue(self, info):
        new_node = Node(info)
        if self.is_empty():
            self.__top = new_node
        else:
            self.__last.set_next(new_node)
        self.__last = new_node
        self.__size += 1

    def dequeue(self):
        if self.is_empty():
            return None
        info = self.__top.get_info()
        self.__top = self.__top.get_next()
        self.__size -= 1
        if self.__top is None:      
            self.__last = None
        return info

    def print_info(self):
        print("********* QUEUE DUMP *********")
        print("  Size: " + str(self.size()))
        node = self.__top
        i = 1
        while node is not None:
            print("  ** Elemento " + str(i))
            node.get_info().print()
            node = node.get_next()
            i += 1
        print("******************************")

    def get_nth(self, pos):
        if pos < 1 or pos > self.__size:
            return None
        node = self.__top
        for _ in range(pos - 1):
            node = node.get_next()
        return node.get_info()

class TestQueue:
    @staticmethod
    def main():
        queue = Queue()

        print(">>> Cola recién creada")
        queue.print_info()

    
        pedidos = [
            Order(20, "cust1"),
            Order(30, "cust2"),
            Order(40, "cust3"),
            Order(50, "cust3"),
        ]
        for p in pedidos:
            print(f">>> enqueue({p.get_cliente()}, {p.get_qtty()})")
            queue.enqueue(p)
            queue.print_info()

        # Probar front (no elimina)
        print(">>> front()")
        primero = queue.front()
        primero.print()
        queue.print_info()

        # Probar dequeue (elimina)
        print(">>> dequeue()")
        sacado = queue.dequeue()
        sacado.print()
        queue.print_info()

        print(">>> dequeue()")
        sacado = queue.dequeue()
        sacado.print()
        queue.print_info()

        # Probar get_nth con 4 elementos: volvemos a llenar la cola
        print(">>> Prueba de get_nth con 4 elementos")
        queue2 = Queue()
        for p in [Order(10, "A"), Order(20, "B"), Order(30, "C"), Order(40, "D")]:
            queue2.enqueue(p)
        queue2.print_info()

        print(">>> get_nth(3)")
        tercero = queue2.get_nth(3)
        if tercero is not None:
            tercero.print()

        print(">>> get_nth(9)  (posición no válida)")
        print(queue2.get_nth(9))   # None

        print(">>> La cola no cambió:")
        queue2.print_info()


if __name__ == "__main__":
    TestQueue.main()