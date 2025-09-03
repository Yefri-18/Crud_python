# 📦 Inventario con Tkinter, MySQL y Códigos QR

Aplicación de escritorio para la gestión de inventario con interfaz gráfica en **Tkinter**, base de datos en **MySQL** y generación automática de **códigos QR** para cada producto.  

---

## 🚀 Características
- CRUD completo (Crear, Leer, Actualizar, Eliminar).  
- Generación de **códigos QR** únicos por producto.  
- Exportación a **Excel (.xlsx)**.  
- Exportación a **PDF (.pdf)**.  
- Interfaz amigable con tabla de productos.  
- Al hacer doble clic en un producto se muestra su **QR**.  

---

## 🛠️ Requisitos

### 🔹 Software necesario
1. **Python 3.8+**  
   Descárgalo desde: [https://www.python.org/downloads/](https://www.python.org/downloads/)  
   > Asegúrate de marcar **“Add Python to PATH”** durante la instalación.

2. **MySQL Server**  
   Descárgalo desde: [https://dev.mysql.com/downloads/mysql/](https://dev.mysql.com/downloads/mysql/)  

3. **MySQL Workbench** (opcional, para administrar la base de datos).  

---

### 🔹 Librerías de Python
Instala las dependencias con:

```bash
pip install mysql-connector-python
pip install openpyxl
pip install reportlab
pip install qrcode[pil]
pip install pillow
