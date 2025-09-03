import tkinter as tk
from tkinter import messagebox
import mysql.connector
import inventario  # Importamos la app de inventario

# -------- CONEXIÓN MYSQL --------
def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",       # tu usuario MySQL
        password="root",   # tu contraseña MySQL
        database="inventario_db"
    )

# -------- VALIDAR LOGIN --------
def validar_login(username, password):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE usuario=%s AND password=%s", (username, password))
    usuario = cursor.fetchone()
    conn.close()
    return usuario is not None

# -------- LOGIN --------
class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Login - Inventario")
        self.root.geometry("300x200")

        tk.Label(root, text="Usuario:").pack(pady=5)
        self.entry_user = tk.Entry(root)
        self.entry_user.pack(pady=5)

        tk.Label(root, text="Contraseña:").pack(pady=5)
        self.entry_pass = tk.Entry(root, show="*")
        self.entry_pass.pack(pady=5)

        tk.Button(root, text="Iniciar Sesión", command=self.login).pack(pady=10)

    def login(self):
        user = self.entry_user.get()
        pwd = self.entry_pass.get()

        if validar_login(user, pwd):
            messagebox.showinfo("Bienvenido", f"Hola {user}")
            self.root.destroy()  # cerrar ventana login
            inventario.iniciar_app()  # abrir inventario
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")

# -------- INICIO --------
if __name__ == "__main__":
    root = tk.Tk()
    app = LoginWindow(root)
    root.mainloop()
