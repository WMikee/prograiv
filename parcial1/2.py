import os

class Empleado:
    def __init__(self, nombre: str, id: int, salario_base: float, anios_experiencia: int):
        self.nombre = nombre
        self.id = id
        self.salario_base = salario_base
        self.anios_experiencia = anios_experiencia

    def calcular_salario(self) -> float:
        if 0 <= self.anios_experiencia <= 2:
            bono = 0.05
        elif 3 <= self.anios_experiencia <= 5:
            bono = 0.10
        else:
            bono = 0.15
        return self.salario_base * (1 + bono)

    def __str__(self) -> str:
        return (f"ID: {self.id} | Nombre: {self.nombre} | "
                f"Base: {self.salario_base:.2f} | Años Exp: {self.anios_experiencia} | "
                f"Salario Total: {self.calcular_salario():.2f}")

    def to_file(self) -> str:
        return f"{self.id},{self.nombre},{self.salario_base},{self.anios_experiencia}"

    def from_file(linea: str):
        partes = linea.strip().split(",")
        return Empleado(partes[1], int(partes[0]), float(partes[2]), int(partes[3]))


class GestorEmpleados:
    def __init__(self):
        self.empleados = []

    def agregar_empleado(self, empleado: Empleado):
        self.empleados.append(empleado)

    def eliminar_empleado(self, id: int):
        for empleado in self.empleados:
            if empleado.id == id:
                self.empleados.remove(empleado)

    def buscar_empleado(self, id: int):
        for e in self.empleados:
            if e.id == id:
                return e
        return None

    def editar_empleado(self, id: int):
        empleado = self.buscar_empleado(id)
        if empleado:
            print("Deja en blanco si no deseas modificar un campo.")
            nuevo_nombre = input(f"Nombre ({empleado.nombre}): ")
            nuevo_salario = input(f"Salario Base ({empleado.salario_base}): ")
            nuevos_anios = input(f"Años de Experiencia ({empleado.anios_experiencia}): ")

            if nuevo_nombre.strip():
                empleado.nombre = nuevo_nombre
            if nuevo_salario.strip():
                empleado.salario_base = float(nuevo_salario)
            if nuevos_anios.strip():
                empleado.anios_experiencia = int(nuevos_anios)
        else:
            print("Empleado no encontrado.")

    def mostrar_empleados(self):
        if not self.empleados:
            print("No hay empleados registrados.")
        for e in self.empleados:
            print(e)

    def guardar_empleados(self, archivo: str):
        with open(archivo, "w", encoding="utf-8") as f:
            for e in self.empleados:
                f.write(e.to_file() + "\n")

    def cargar_empleados(self, archivo: str):
        if not os.path.exists(archivo):
            return
        with open(archivo, "r", encoding="utf-8") as f:
            for linea in f:
                _empleado = Empleado("", 0, 0, 0)
                self.empleados.append(_empleado.from_file(linea))


def menu():
    gestor = GestorEmpleados()
    archivo = "empleados.txt"
    gestor.cargar_empleados(archivo)

    while True:
        print("\n--- Sistema de Gestión de Empleados ---")
        print("1. Agregar empleado")
        print("2. Eliminar empleado")
        print("3. Buscar empleado por ID")
        print("4. Editar empleado")
        print("5. Mostrar empleados")
        print("6. Guardar empleados")
        print("7. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            nombre = input("Nombre: ")
            id = int(input("ID: "))
            salario_base = float(input("Salario Base: "))
            anios = int(input("Años de experiencia: "))
            empleado = Empleado(nombre, id, salario_base, anios)
            gestor.agregar_empleado(empleado)
            print("Empleado agregado exitosamente.")

        elif opcion == "2":
            id = int(input("Ingrese ID del empleado a eliminar: "))
            gestor.eliminar_empleado(id)
            print("Empleado eliminado si existía.")

        elif opcion == "3":
            id = int(input("Ingrese ID del empleado a buscar: "))
            empleado = gestor.buscar_empleado(id)
            print(empleado if empleado else "Empleado no encontrado.")

        elif opcion == "4":
            id = int(input("Ingrese ID del empleado a editar: "))
            gestor.editar_empleado(id)

        elif opcion == "5":
            gestor.mostrar_empleados()

        elif opcion == "6":
            gestor.guardar_empleados(archivo)
            print("Empleados guardados en archivo.")

        elif opcion == "7":
            gestor.guardar_empleados(archivo)
            print("Datos guardados.")
            break

        else:
            print("Opción inválida.")


if __name__ == "__main__":
    menu()
