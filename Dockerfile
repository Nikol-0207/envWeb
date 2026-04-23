FROM python:3.10-slim

WORKDIR /app

# Copiamos e instalamos dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el resto del proyecto
COPY . .

EXPOSE 5000

# Ejecutamos app.py
CMD ["python", "app.py"]
