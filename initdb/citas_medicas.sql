CREATE DATABASE IF NOT EXISTS citas_medicas;
USE citas_medicas;

CREATE TABLE IF NOT EXISTS usuarios (
  id_usuario int NOT NULL AUTO_INCREMENT,
  nombre varchar(100) NOT NULL,
  username varchar(50) NOT NULL,
  password varchar(255) NOT NULL,
  rol enum('doctor','paciente','administrador') NOT NULL,
  numero_cedula varchar(20) NOT NULL,
  PRIMARY KEY (id_usuario),
  UNIQUE KEY username (username)
);

CREATE TABLE IF NOT EXISTS administradores (
  id_administrador int NOT NULL AUTO_INCREMENT,
  id_usuario int NOT NULL,
  PRIMARY KEY (id_administrador),
  KEY id_usuario (id_usuario),
  CONSTRAINT administradores_ibfk_1 FOREIGN KEY (id_usuario) REFERENCES usuarios (id_usuario)
);

CREATE TABLE IF NOT EXISTS citasmedicas (
  id_cita int NOT NULL AUTO_INCREMENT,
  id_usuario_paciente int NOT NULL,
  id_usuario_doctor int NOT NULL,
  fecha date NOT NULL,
  hora time NOT NULL,
  motivo varchar(255) DEFAULT NULL,
  estado enum('pendiente','confirmada','cancelada') NOT NULL,
  PRIMARY KEY (id_cita),
  KEY id_usuario_paciente (id_usuario_paciente),
  KEY id_usuario_doctor (id_usuario_doctor),
  CONSTRAINT citasmedicas_ibfk_1 FOREIGN KEY (id_usuario_paciente) REFERENCES usuarios (id_usuario),
  CONSTRAINT citasmedicas_ibfk_2 FOREIGN KEY (id_usuario_doctor) REFERENCES usuarios (id_usuario)
);

-- Insert data into usuarios
INSERT INTO usuarios (nombre, username, password, rol, numero_cedula) VALUES
('admin','admin','steven','administrador','1726517541'),
('karo','karo','karo','doctor','1751611540'),
('kris','kris','kris','paciente','1719690487');

-- Insert data into citasmedicas
INSERT INTO citasmedicas (id_usuario_paciente, id_usuario_doctor, fecha, hora, motivo, estado) VALUES
(1,2,'2020-02-02','02:02:00','frio','confirmada');
