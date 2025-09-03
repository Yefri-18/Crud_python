import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector
from openpyxl import Workbook
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import qrcode
from PIL import Image, ImageTk

# -------- CONEXIÓN MYSQL --------
def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",      # cámbialo por tu usuario
        password="root",  # cámbialo por tu contraseña
        database="inventario_db"
    )

# -------- CRUD + QR --------
def insertar_producto(nombre, categoria, cantidad, precio):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO productos (nombre, categoria, cantidad, precio) VALUES (%s, %s, %s, %s)",
                   (nombre, categoria, cantidad, precio))
    conn.commit()
    producto_id = cursor.lastrowid
    conn.close()

    # Generar QR
    datos = f"ID: {producto_id}\nNombre: {nombre}\nCategoría: {categoria}\nCantidad: {cantidad}\nPrecio: {precio}"
    qr = qrcode.make(datos)
    qr_filename = f"qr_producto_{producto_id}.png"
    qr.save(qr_filename)

    return producto_id, qr_filename

def obtener_productos():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()
    conn.close()
    return productos

def eliminar_producto(id_producto):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM productos WHERE id=%s", (id_producto,))
    conn.commit()
    conn.close()

def actualizar_producto(id_producto, nombre, categoria, cantidad, precio):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("UPDATE productos SET nombre=%s, categoria=%s, cantidad=%s, precio=%s WHERE id=%s",
                   (nombre, categoria, cantidad, precio, id_producto))
    conn.commit()
    conn.close()

# -------- EXPORTAR A EXCEL --------
def exportar_excel():
    productos = obtener_productos()
    if not productos:
        messagebox.showwarning("Atención", "No hay productos para exportar")
        return
    
    wb = Workbook()
    ws = wb.active
    ws.title = "Productos"
    ws.append(["ID", "Nombre", "Categoría", "Cantidad", "Precio"])  # encabezados

    for p in productos:
        ws.append(p)

    wb.save("productos.xlsx")
    messagebox.showinfo("Éxito", "Datos exportados a productos.xlsx")

# -------- EXPORTAR A PDF --------
def exportar_pdf():
    productos = obtener_productos()
    if not productos:
        messagebox.showwarning("Atención", "No hay productos para exportar")
        return
    
    c = canvas.Canvas("productos.pdf", pagesize=letter)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(200, 750, "Reporte de Inventario")
    c.setFont("Helvetica", 10)

    x, y = 50, 700
    c.drawString(x, y, "ID")
    c.drawString(x+50, y, "Nombre")
    c.drawString(x+200, y, "Categoría")
    c.drawString(x+350, y, "Cantidad")
    c.drawString(x+420, y, "Precio")

    y -= 20
    for p in productos:
        c.drawString(x, y, str(p[0]))
        c.drawString(x+50, y, str(p[1]))
        c.drawString(x+200, y, str(p[2]))
        c.drawString(x+350, y, str(p[3]))
        c.drawString(x+420, y, str(p[4]))
        y -= 20
        if y < 50:
            c.showPage()
            y = 750

    c.save()
    messagebox.showinfo("Éxito", "Datos exportados a productos.pdf")

# -------- FUNCIONES DE INTERFAZ --------
def mostrar_qr(qr_filename):
    """Muestra el QR en una ventana emergente de Tkinter"""
    top = tk.Toplevel()
    top.title("Código QR generado")
    try:
        img = Image.open(qr_filename)
        img = img.resize((200, 200))
        img_tk = ImageTk.PhotoImage(img)

        lbl = tk.Label(top, image=img_tk)
        lbl.image = img_tk
        lbl.pack(padx=10, pady=10)

        tk.Label(top, text=f"QR guardado en: {qr_filename}").pack(pady=5)
    except:
        tk.Label(top, text="Error al cargar el QR").pack(pady=10)

def agregar_producto():
    nombre = entry_nombre.get()
    categoria = entry_categoria.get()
    cantidad = entry_cantidad.get()
    precio = entry_precio.get()

    if nombre and cantidad.isdigit() and precio.replace('.', '', 1).isdigit():
        producto_id, qr_filename = insertar_producto(nombre, categoria, int(cantidad), float(precio))
        actualizar_lista()
        limpiar_formulario()
        mostrar_qr(qr_filename)
        messagebox.showinfo("Éxito", f"Producto agregado con ID {producto_id}")
    else:
        messagebox.showerror("Error", "Datos inválidos")

def actualizar_lista():
    for row in tree.get_children():
        tree.delete(row)
    for prod in obtener_productos():
        qr_filename = f"qr_producto_{prod[0]}.png"
        tree.insert("", "end", values=(prod[0], prod[1], prod[2], prod[3], prod[4], qr_filename))

def seleccionar_producto(event):
    item = tree.selection()
    if item:
        valores = tree.item(item, "values")
        entry_id.config(state="normal")
        entry_id.delete(0, tk.END)
        entry_id.insert(0, valores[0])
        entry_id.config(state="readonly")
        entry_nombre.delete(0, tk.END)
        entry_nombre.insert(0, valores[1])
        entry_categoria.delete(0, tk.END)
        entry_categoria.insert(0, valores[2])
        entry_cantidad.delete(0, tk.END)
        entry_cantidad.insert(0, valores[3])
        entry_precio.delete(0, tk.END)
        entry_precio.insert(0, valores[4])

def abrir_qr(event):
    """Cuando haga doble clic en la columna QR, mostrar imagen"""
    item = tree.selection()
    if item:
        valores = tree.item(item, "values")
        qr_filename = valores[5]  # la columna QR
        mostrar_qr(qr_filename)

def eliminar_seleccionado():
    item = tree.selection()
    if item:
        valores = tree.item(item, "values")
        eliminar_producto(valores[0])
        actualizar_lista()
        limpiar_formulario()
        messagebox.showinfo("Éxito", "Producto eliminado")

def modificar_producto():
    id_producto = entry_id.get()
    nombre = entry_nombre.get()
    categoria = entry_categoria.get()
    cantidad = entry_cantidad.get()
    precio = entry_precio.get()

    if id_producto and nombre and cantidad.isdigit() and precio.replace('.', '', 1).isdigit():
        actualizar_producto(id_producto, nombre, categoria, int(cantidad), float(precio))
        actualizar_lista()
        limpiar_formulario()
        messagebox.showinfo("Éxito", "Producto actualizado")
    else:
        messagebox.showerror("Error", "Datos inválidos")

def limpiar_formulario():
    entry_id.config(state="normal")
    entry_id.delete(0, tk.END)
    entry_id.config(state="readonly")
    entry_nombre.delete(0, tk.END)
    entry_categoria.delete(0, tk.END)
    entry_cantidad.delete(0, tk.END)
    entry_precio.delete(0, tk.END)

# -------- INTERFAZ --------
ventana = tk.Tk()
ventana.title("Inventario con MySQL + QR")
ventana.geometry("950x600")
ventana.configure(bg="#f4f4f9")

style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview", background="#ffffff", foreground="black",
                rowheight=25, fieldbackground="#e6f0ff")
style.map("Treeview", background=[("selected", "#4a90e2")])

# -------- FORMULARIO --------
frame_form = tk.LabelFrame(ventana, text="Gestión de Productos", bg="#f4f4f9", font=("Arial", 12, "bold"))
frame_form.pack(pady=10, padx=10, fill="x")

tk.Label(frame_form, text="ID:", bg="#f4f4f9").grid(row=0, column=0, padx=5, pady=5)
entry_id = tk.Entry(frame_form, state="readonly")
entry_id.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_form, text="Nombre:", bg="#f4f4f9").grid(row=1, column=0, padx=5, pady=5)
entry_nombre = tk.Entry(frame_form)
entry_nombre.grid(row=1, column=1, padx=5, pady=5)

tk.Label(frame_form, text="Categoría:", bg="#f4f4f9").grid(row=2, column=0, padx=5, pady=5)
entry_categoria = tk.Entry(frame_form)
entry_categoria.grid(row=2, column=1, padx=5, pady=5)

tk.Label(frame_form, text="Cantidad:", bg="#f4f4f9").grid(row=3, column=0, padx=5, pady=5)
entry_cantidad = tk.Entry(frame_form)
entry_cantidad.grid(row=3, column=1, padx=5, pady=5)

tk.Label(frame_form, text="Precio:", bg="#f4f4f9").grid(row=4, column=0, padx=5, pady=5)
entry_precio = tk.Entry(frame_form)
entry_precio.grid(row=4, column=1, padx=5, pady=5)

btn_frame = tk.Frame(frame_form, bg="#f4f4f9")
btn_frame.grid(row=5, column=0, columnspan=2, pady=10)

ttk.Button(btn_frame, text="Agregar", command=agregar_producto).grid(row=0, column=0, padx=5)
ttk.Button(btn_frame, text="Modificar", command=modificar_producto).grid(row=0, column=1, padx=5)
ttk.Button(btn_frame, text="Eliminar", command=eliminar_seleccionado).grid(row=0, column=2, padx=5)
ttk.Button(btn_frame, text="Limpiar", command=limpiar_formulario).grid(row=0, column=3, padx=5)

# -------- BOTONES EXPORTACIÓN --------
frame_export = tk.Frame(ventana, bg="#f4f4f9")
frame_export.pack(pady=10)

btn_excel = tk.Button(frame_export, text="Exportar a Excel", bg="#2ecc71", fg="white", command=exportar_excel)
btn_excel.grid(row=0, column=0, padx=10)

btn_pdf = tk.Button(frame_export, text="Exportar a PDF", bg="#e74c3c", fg="white", command=exportar_pdf)
btn_pdf.grid(row=0, column=1, padx=10)

# -------- TABLA --------
tree_frame = tk.Frame(ventana, bg="#f4f4f9")
tree_frame.pack(pady=10, padx=10, fill="both", expand=True)

tree = ttk.Treeview(tree_frame, columns=("ID", "Nombre", "Categoría", "Cantidad", "Precio", "QR"), show="headings")
tree.pack(fill="both", expand=True)

for col in ("ID", "Nombre", "Categoría", "Cantidad", "Precio", "QR"):
    tree.heading(col, text=col)

tree.bind("<ButtonRelease-1>", seleccionar_producto)
tree.bind("<Double-1>", abrir_qr)  # doble clic muestra el QR

# -------- INICIAR --------
actualizar_lista()
ventana.mainloop()
