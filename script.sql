CREATE DATABASE project_benchmark;

CREATE TABLE benchmark (
    id SERIAL PRIMARY KEY,
    nome TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    indirizzo TEXT NOT NULL
);