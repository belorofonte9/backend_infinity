# Usamos una imagen base con Python
FROM ubuntu:latest

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos necesarios
COPY requirements.txt .
COPY app2.py .

 # Si necesitas Python y pip e intalar psycopg2
RUN apt-get update && \
    apt-get install python3 python3-pip libpq-dev python3-dev gcc -y --no-install-recommends
    #apk add libpq-dev python3 py3-pip  python3-dev 
    #-y --no-install-recommends 

# Instala dependencias
RUN pip install --no-cache-dir --break-system-package -r requirements.txt 
#RUN pip install -r requirements.txt

# Comando por defecto para ejecutar el script
CMD ["python3", "app2.py"]