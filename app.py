import sqlite3 
import tkinter as tk
from tkinter import ttk, messagebox

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