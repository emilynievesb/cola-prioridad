class Node:
    """Clase que representa un nodo (paciente) en la lista enlazada."""
    def __init__(self, nombre, edad, sintomas, gravedad):
        self.nombre = nombre
        self.edad = edad
        self.sintomas = sintomas
        self.gravedad = gravedad
        self.subprioridad = self.obtener_subprioridad()
        self.next = None  # Referencia al siguiente nodo en la lista

    def obtener_subprioridad(self):
        """
        Retorna la sub-prioridad según la edad:
          1 -> niños (<12 años)
          2 -> adultos mayores (>=65 años)
          3 -> demás pacientes
        """
        if self.edad < 12:
            return 1
        elif self.edad >= 65:
            return 2
        else:
            return 3

    def __str__(self):
        return (f"Nombre: {self.nombre}, Edad: {self.edad}, "
                f"Síntomas: {self.sintomas}, Gravedad: {self.gravedad}")


class PriorityQueue:
    """Clase que implementa una cola de prioridad utilizando una lista enlazada."""
    def __init__(self):
        self.head = None  # Apunta al primer nodo de la lista

    def esta_vacia(self):
        """Verifica si la cola está vacía."""
        return self.head is None

    def insertar_paciente(self, nombre, edad, sintomas, gravedad):
        """
        Inserta un nuevo paciente en la cola de prioridad de acuerdo con:
          - Gravedad (1 = mayor prioridad, 5 = menor prioridad)
          - En caso de empatar gravedad, se usa la subprioridad (niños < adultos mayores < demás).
        Retorna la posición (1-based) en la que se insertó el paciente.
        """
        nuevo_nodo = Node(nombre, edad, sintomas, gravedad)

        # Si la cola está vacía, el nuevo nodo es la cabeza
        if self.esta_vacia():
            self.head = nuevo_nodo
            return 1

        # Si el nuevo nodo tiene más prioridad que el primer nodo (head), se inserta al inicio
        if self.tiene_mas_prioridad(nuevo_nodo, self.head):
            nuevo_nodo.next = self.head
            self.head = nuevo_nodo
            return 1

        # Recorremos la lista para ubicar el nuevo nodo
        posicion = 1
        actual = self.head
        while actual.next is not None:
            posicion += 1
            # Comparamos el nuevo nodo con el siguiente
            if self.tiene_mas_prioridad(nuevo_nodo, actual.next):
                # Insertamos aquí
                nuevo_nodo.next = actual.next
                actual.next = nuevo_nodo
                return posicion
            actual = actual.next

        # Si llegamos al final, insertamos el nodo al final
        actual.next = nuevo_nodo
        return posicion + 1

    @staticmethod
    def tiene_mas_prioridad(nodo_a, nodo_b):
        """
        Determina si nodo_a tiene mayor prioridad que nodo_b
        basándose en la gravedad y luego en la subprioridad.
        """
        # Primero se compara la gravedad (1 es más prioritario que 5)
        if nodo_a.gravedad < nodo_b.gravedad:
            return True
        elif nodo_a.gravedad > nodo_b.gravedad:
            return False
        else:
            # En caso de que la gravedad sea igual, comparamos la subprioridad
            return nodo_a.subprioridad < nodo_b.subprioridad

    def pasar_siguiente_paciente(self):
        """
        Retira al primer paciente de la cola (máxima prioridad) y lo retorna.
        Si la cola está vacía, retorna None.
        """
        if self.esta_vacia():
            return None
        nodo_a_atender = self.head
        self.head = self.head.next  # Avanzamos la cabeza
        nodo_a_atender.next = None  # Desconectamos el nodo
        return nodo_a_atender

    def mostrar_cola(self):
        """Muestra el contenido actual de la cola de prioridad."""
        if self.esta_vacia():
            print("\nLa cola está vacía.")
            return

        print("\nCOLA DE ATENCIÓN (en orden):")
        actual = self.head
        indice = 1
        while actual is not None:
            print(f"{indice}. {actual}")
            actual = actual.next
            indice += 1


def main():
    cola = PriorityQueue()

    while True:
        print("\n--- MENÚ PRINCIPAL ---")
        print("1. Ingresar Paciente")
        print("2. Pasar siguiente paciente")
        print("3. Mostrar la cola")
        print("4. Salir")

        opcion = input("Seleccione una opción (1-4): ")

        if opcion == "1":
            # Ingresar Paciente
            nombre = input("Nombre completo: ")
            edad = int(input("Edad: "))
            sintomas = input("Síntomas o motivo de consulta: ")
            gravedad = int(input("Gravedad (1-5, siendo 1 la mayor gravedad): "))

            posicion = cola.insertar_paciente(nombre, edad, sintomas, gravedad)
            print(f"\nEl paciente '{nombre}' ha sido ingresado en la posición {posicion}.")
        
        elif opcion == "2":
            # Pasar siguiente paciente
            siguiente = cola.pasar_siguiente_paciente()
            if siguiente is None:
                print("\nNo hay pacientes en la cola.")
            else:
                print("\nSiguiente paciente en ser atendido:")
                print(siguiente)
        
        elif opcion == "3":
            # Mostrar la cola
            cola.mostrar_cola()
        
        elif opcion == "4":
            print("Saliendo del programa...")
            break
        
        else:
            print("Opción inválida. Intente nuevamente.")


if __name__ == "__main__":
    main()
