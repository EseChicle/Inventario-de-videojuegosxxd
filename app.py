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

class Inventario(tk.TK):
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
        
