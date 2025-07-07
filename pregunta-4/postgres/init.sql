-- Inicialización de tabla de usuarios
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE
);

-- Inicialización de tabla de productos
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    quantity INTEGER NOT NULL DEFAULT 0
);

-- Insertar datos de ejemplo para usuarios
INSERT INTO users (name, email) VALUES
('Juan Perez', 'juan.perez@email.com'),
('Maria Garcia', 'maria.garcia@email.com'),
('Carlos Rodriguez', 'carlos.rodriguez@email.com');

-- Insertar datos de ejemplo para productos
INSERT INTO products (name, quantity) VALUES
('Laptop Dell', 15),
('Mouse Logitech', 50),
('Teclado Mecánico', 25),
('Monitor Samsung', 8);
