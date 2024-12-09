drop database pokemon;

-- Crear la base de datos
CREATE DATABASE IF NOT EXISTS Pokemon;
USE Pokemon;

-- Tabla de regiones
CREATE TABLE IF NOT EXISTS region (
    id INT AUTO_INCREMENT PRIMARY KEY,
    Nombre VARCHAR(50) UNIQUE NOT NULL
);

-- Tabla de tipos
CREATE TABLE IF NOT EXISTS tipos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    Nombre VARCHAR(50) UNIQUE NOT NULL
);

-- Tabla de Pokémon
CREATE TABLE IF NOT EXISTS pokedex (
    id INT AUTO_INCREMENT PRIMARY KEY,
    Numero_de_pokedex INT UNIQUE NOT NULL,
    Nombre_de_pokemon VARCHAR(50) NOT NULL,
    Region_id INT,
    FOREIGN KEY (Region_id) REFERENCES region(id)
);

-- Tabla intermedia para relacionar Pokémon y tipos
CREATE TABLE IF NOT EXISTS pokemon_tipos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    pokemon_id INT,
    tipo_id INT,
    FOREIGN KEY (pokemon_id) REFERENCES pokedex(id),
    FOREIGN KEY (tipo_id) REFERENCES tipos(id),
    UNIQUE (pokemon_id, tipo_id)
);

SELECT * FROM pokedex;

