import xml.etree.ElementTree as ET

class Producto:
    def __init__(self, nombre: str, id: int, precio: float, cantidad: int):
        self.nombre = nombre
        self.id = id
        self.precio = precio
        self.cantidad = cantidad

    def disminuir_inventario(self, cantidad: int):
        if cantidad <= self.cantidad:
            self.cantidad -= cantidad
            return True
        return False

    def aumentar_inventario(self, cantidad: int):
        self.cantidad += cantidad

    def mostrar_informacion(self):
        return f"Producto(ID: {self.id}, Nombre: {self.nombre}, Precio: {self.precio}, Stock: {self.cantidad})"


class Cliente:
    def __init__(self, nombre: str, id: int, saldo: float):
        self.nombre = nombre
        self.id = id
        self.saldo = saldo

    def realizar_compra(self, producto: Producto, cantidad: int):
        costo_total = producto.precio * cantidad
        if self.saldo >= costo_total and producto.cantidad >= cantidad:
            self.saldo -= costo_total
            producto.disminuir_inventario(cantidad)
            return True
        return False

    def mostrar_informacion(self):
        return f"Cliente(ID: {self.id}, Nombre: {self.nombre}, Saldo: {self.saldo})"


class Tienda:
    def __init__(self):
        self.productos = []
        self.clientes = []

    def agregar_producto(self, producto: Producto):
        self.productos.append(producto)

    def agregar_cliente(self, cliente: Cliente):
        self.clientes.append(cliente)

    def realizar_venta(self, id_cliente: int, id_producto: int, cantidad: int):
        cliente = next((c for c in self.clientes if c.id == id_cliente), None)
        producto = next((p for p in self.productos if p.id == id_producto), None)
        if cliente and producto:
            if cliente.realizar_compra(producto, cantidad):
                print(f"Venta realizada: {cliente.nombre} compró {cantidad} de {producto.nombre}")
            else:
                print("No se pudo realizar la venta (saldo o stock insuficiente).")
        else:
            print("Cliente o producto no encontrado.")

    def mostrar_productos(self):
        for p in self.productos:
            print(p.mostrar_informacion())

    def mostrar_clientes(self):
        for c in self.clientes:
            print(c.mostrar_informacion())

    def guardar_datos(self, archivo: str):
        root = ET.Element("tienda")
        productos_elem = ET.SubElement(root, "productos")
        for p in self.productos:
            producto_elem = ET.SubElement(productos_elem, "producto")
            ET.SubElement(producto_elem, "id").text = str(p.id)
            ET.SubElement(producto_elem, "nombre").text = p.nombre
            ET.SubElement(producto_elem, "precio").text = str(p.precio)
            ET.SubElement(producto_elem, "cantidad").text = str(p.cantidad)
        clientes_elem = ET.SubElement(root, "clientes")
        for c in self.clientes:
            cliente_elem = ET.SubElement(clientes_elem, "cliente")
            ET.SubElement(cliente_elem, "id").text = str(c.id)
            ET.SubElement(cliente_elem, "nombre").text = c.nombre
            ET.SubElement(cliente_elem, "saldo").text = str(c.saldo)
        tree = ET.ElementTree(root)
        tree.write(archivo, encoding="utf-8", xml_declaration=True)
        print("Archivo guardado de manera exitosa")

    def cargar_datos(self, archivo: str):
        tree = ET.parse(archivo)
        root = tree.getroot()
        self.productos = []
        self.clientes = []
        for p in root.find("productos").findall("producto"):
            id = int(p.find("id").text)
            nombre = p.find("nombre").text
            precio = float(p.find("precio").text)
            cantidad = int(p.find("cantidad").text)
            self.productos.append(Producto(nombre, id, precio, cantidad))
        for c in root.find("clientes").findall("cliente"):
            id = int(c.find("id").text)
            nombre = c.find("nombre").text
            saldo = float(c.find("saldo").text)
            self.clientes.append(Cliente(nombre, id, saldo))



if __name__ == "__main__":
    tienda = Tienda()
    tienda.agregar_producto(Producto("Manzanas", 1, 0.5, 100))
    tienda.agregar_producto(Producto("Naranjas", 2, 0.7, 50))
    tienda.agregar_cliente(Cliente("Juan", 101, 20.0))
    tienda.agregar_cliente(Cliente("Ana", 102, 15.0))
    print("\n--- Productos ---")
    tienda.mostrar_productos()
    print("\n--- Clientes ---")
    tienda.mostrar_clientes()
    print("\n--- Ventas ---")
    tienda.realizar_venta(101, 1, 10)
    tienda.realizar_venta(102, 2, 30)
    tienda.guardar_datos("tienda.xml")
    print("\nDatos guardados en 'tienda.xml'")
    nueva_tienda = Tienda()
    nueva_tienda.cargar_datos("tienda.xml")
    print("\n--- Datos cargados desde XML ---")
    nueva_tienda.mostrar_productos()
    nueva_tienda.mostrar_clientes()
