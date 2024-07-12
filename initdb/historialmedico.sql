CREATE DATABASE IF NOT EXISTS historialmedico;
USE historialmedico;

CREATE TABLE IF NOT EXISTS historialesmedicos (
  id_historial int NOT NULL AUTO_INCREMENT,
  id_usuario_paciente int NOT NULL,
  descripcion text,
  fecha_creacion date DEFAULT NULL,
  notas text,
  diagnostico text,
  tratamiento text,
  PRIMARY KEY (id_historial)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO historialesmedicos VALUES (1,2,'Paciente presenta síntomas de gripe.','2024-07-01','Paciente reporta fiebre y dolor de cabeza.','Gripe','Paracetamol 500mg cada 8 horas'),(2,2,'Paciente acude para chequeo anual.','2024-07-01','Se realizan análisis de sangre.','Saludable','Continuar con dieta equilibrada y ejercicio regular'),(5,6,'cansado','2024-01-01','fiebre','agua','apstillas'),(6,3,'rojo','1111-01-01','rojo','rojo','rojo'),(7,4,'salud','0002-02-02','salud','salud','gripe');
