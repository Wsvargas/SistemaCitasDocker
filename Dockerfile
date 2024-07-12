# Dockerfile en la raíz del proyecto (Citas)

# Utiliza una imagen base oficial de Python
FROM python:3.12-slim

# Establece el directorio de trabajo en el contenedor
WORKDIR /app

# Copia los archivos de requisitos en el directorio de trabajo
COPY requirements.txt .

# Instala las dependencias necesarias
RUN pip install --no-cache-dir -r requirements.txt

# Copia el contenido de la aplicación en el directorio de trabajo
COPY . .

# Expone el puerto en el que se ejecutará la aplicación
EXPOSE 5000

# Define el comando para ejecutar la aplicación cuando el contenedor se inicie
CMD ["flask", "run", "--host=0.0.0.0"]
