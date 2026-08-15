import sqlite3 
import tkinter as tk
from tkinter import ttk, messagebox

#base de datos#
DB_NAME = "inventario.db"
def conectar_db():
    conn = sqlite3.connect(DB_NAME)
    conn.execute(
        """
        CREATE TABLE IF  NOT EXISTS videojuegos(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL
        categoria TEXT,
        cantidad INTEGER NOT NULL DEFAULT 0,
        precio REAL NOT NULL DEFAULT0
        )
        """
    )
    return conn
#ventana principal y carga de productos#

class Inventario(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Videojuegos Nevos")
        self.geometry("1024x768")

        style = ttk.Style(self)
        style.configure(".",font=("Segoe UI", 12))
        style.configure("Treeview", font=("Segoe UI", 11), rowheight=26)
        style.configure("Treeview.Heading", font=("Segoe UI", 11, "bold"))

        self.conn = conectar_db()
        self.id_seleccionado = None

        self._crear_widgets()
        self.cargar_datos()
        
#interfaz visual#
    def _crear_widgets(self):
        form = ttk.LabelFrame(self, text="Datos del juego")
        form.pack(fill="x", padx=10, pady=10)

        ttk.Label(form, text="Título:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.entry_nombre = ttk.Entry(form, width=40)
        self.entry_nombre.grid(row=0, column=1, padx=5, pady=5, columnspan=3, sticky="w")

        ttk.Label(form, text="Cantidad:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.entry_cantidad = ttk.Entry(form, width=30)
        self.entry_cantidad.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(form, text="Precio:").grid(row=1, column=2, padx=5, pady=5, sticky="e")
        self.entry_precio = ttk.Entry(form, width=20)
        self.entry_precio.grid(row=1, column=3, padx=5, pady=5)

        botones = ttk.Frame(form)
        botones.grid(row=2, column=0, columnspan=4, pady=10)

        ttk.Button(botones, text="Agregar", command=self.agregar_producto).pack(side="left", padx=5)
        ttk.Button(botones, text="Actualizar", command=self.actualizar_producto).pack(side="left", padx=5)
        ttk.Button(botones, text="Eliminar", command=self.eliminar_producto).pack(side="left", padx=5)
        ttk.Button(botones, text="Limpiar", command=self.limpiar_formulario).pack(side="left", padx=5)

        busqueda_frame = ttk.Frame(self)
        busqueda_frame.pack(fill="x", padx=10)
        ttk.Label(busqueda_frame, text="Buscar:").pack(side="left")
        self.entry_busqueda = ttk.Entry(busqueda_frame, width=40)
        self.entry_busqueda.pack(side="left", padx=5)
        self.entry_busqueda.bind("<KeyRelease>", lambda e: self._cargar_datos(self.entry_busqueda.get()))

        columnas = ("id", "nombre", "cantidad", "precio", "total")
        self.tabla = ttk.Treeview(self, columns=columnas, show="headings")
        titulos = {
            "id": "ID", "nombre": "Título", "cantidad": "Cantidad", "precio": "Precio", "total": "Total",
        }
        anchos = {"id": 40, "nombre": 320, "cantidad": 90, "precio": 100, "total": 110}
        for col in columnas:
            self.tabla.heading(col, text=titulos[col])
            self.tabla.column(col, width=anchos[col], anchor="center")

        self.tabla.pack(fill="both", expand=True, padx=10, pady=10)
        self.tabla.bind("<<TreeviewSelect>>", self._seleccionar_fila)

        self.label_total = ttk.Label(self, text="Valor total del inventario: $0.00", anchor="w")
        self.label_total.pack(fill="x", padx=10, pady=(0, 10))

        #validacion formulario#
    def _validar_formulario(self):
        nombre = self.entry_nombre.get().strip()
        cantidad = self.entry_cantidad.get().strip()
        precio = self.entry_precio.get().strip()

        if not nombre:
            messagebox.showwarning("Validación", "El título es obligatorio.")
            return None

        try:
            cantidad = int(cantidad)
        except ValueError:
            messagebox.showwarning("Validación", "La cantidad debe ser un número entero.")
            return None

        try:
            precio = float(precio)
        except ValueError:
            messagebox.showwarning("Validación", "El precio debe ser un número.")
            return None

        return nombre, cantidad, precio
    
     #actualizar producto
    def actualizar_producto(self):
        if self.id_seleccionado is None:
            messagebox.showwarning("Selección", "Selecciona un juego de la tabla para actualizar.")
            return
        datos = self._validar_formulario()
        if not datos:
            return
        nombre, cantidad, precio = datos
        self.conn.execute(
            "UPDATE productos SET nombre=?, cantidad=?, precio=? WHERE id=?",
            (nombre, cantidad, precio, self.id_seleccionado),
        )
        self.conn.commit()
        self._cargar_datos()

        #eliminar productos

    def eliminar_producto(self):
        if self.id_seleccionado is None:
            messagebox.showwarning("Selección", "Selecciona un juego de la tabla para eliminar.")
            return
        if messagebox.askyesno("Confirmar", "¿Eliminar el juego seleccionado?"):
            self.conn.execute("DELETE FROM productos WHERE id=?", (self.id_seleccionado,))
            self.conn.commit()
            self._cargar_datos()

            #limpiar formulario

    def limpiar_formulario(self):
        self.entry_nombre.delete(0, tk.END)
        self.entry_cantidad.delete(0, tk.END)
        self.entry_precio.delete(0, tk.END)
        self.id_seleccionado = None
        self.tabla.selection_remove(self.tabla.selection())
        


        


    
