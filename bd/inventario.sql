CREATE DATABASE inventario_db;
USE inventario_db;

-- Tabla de productos
CREATE TABLE productos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    categoria VARCHAR(50),
    cantidad INT NOT NULL,
    precio DECIMAL(10,2) NOT NULL
);

-- Opcional: usuarios (si quieres login)
CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL
);

-- Opcional: movimientos de stock (entradas/salidas)
CREATE TABLE movimientos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    producto_id INT,
    tipo ENUM('entrada','salida'),
    cantidad INT NOT NULL,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (producto_id) REFERENCES productos(id)
);
CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE,
    password VARCHAR(100) NOT NULL
);
INSERT INTO usuarios (usuario, password) VALUES ('admin', '1234');
