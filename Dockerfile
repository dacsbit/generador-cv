# Imagen liviana con Python
FROM python:3.12-slim

# Dependencias de sistema que WeasyPrint necesita para renderizar
# (Pango, Cairo, GDK-Pixbuf, fuentes)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libcairo2 \
    libgdk-pixbuf-2.0-0 \
    libffi-dev \
    shared-mime-info \
    fonts-dejavu-core \
    fonts-liberation \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Instalar dependencias Python primero (aprovecha cache de Docker)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del proyecto
COPY . .

# Por defecto genera el CV usando data.yaml -> CV.pdf
ENTRYPOINT ["python3", "generar_cv.py"]
CMD []
