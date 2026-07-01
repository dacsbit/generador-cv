# Generador de CV (HTML → PDF)

## Opción A: Docker (recomendado — no instalas nada en tu sistema)

```bash
# Construir la imagen (una sola vez, o cuando cambies requirements.txt)
docker build -t cv-generator .

# Generar el CV (usa tu data.yaml e img/ locales, y deja el PDF en tu carpeta)
docker run --rm -v "$(pwd):/app" cv-generator
```

Esto monta tu carpeta actual dentro del contenedor, así que lee `data.yaml` y
`img/foto.jpg` tal cual los tengas, y escribe `CV.pdf` de vuelta en tu carpeta.

Para pasar otros argumentos (igual que en local):
```bash
docker run --rm -v "$(pwd):/app" cv-generator --data data_backend.yaml --out CV_backend.pdf
```

## Opción B: Entorno virtual local

### macOS
```bash
brew install pango cairo gdk-pixbuf libffi
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
Si WeasyPrint no encuentra las librerías (`OSError: cannot load library 'libgobject-2.0-0'`):
```bash
echo 'export DYLD_LIBRARY_PATH="$(brew --prefix)/lib:$DYLD_LIBRARY_PATH"' >> ~/.zshrc
source ~/.zshrc
```

### Linux (Debian/Ubuntu/Fedora-based)
```bash
sudo apt install libpango-1.0-0 libcairo2 libgdk-pixbuf2.0-0   # Debian/Ubuntu
# o: sudo dnf install pango cairo gdk-pixbuf2                   # Fedora
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Uso
1. Activa tu entorno virtual (si usas Opción B): `source venv/bin/activate`
2. La primera vez, crea tu archivo de datos real a partir del ejemplo:
   ```bash
   cp data.example.yaml data.yaml
   ```
   `data.yaml` es tuyo, tiene tu información real, y **no se sube a GitHub**
   (está en `.gitignore`). `data.example.yaml` sí se sube — es la plantilla
   genérica que ve cualquiera que clone el repo.
3. Edita `data.yaml` con tu información.
4. Si quieres foto de perfil, colócala en `img/` (ej: `img/foto.jpg`) y referencia
   esa ruta en `data.yaml` → `personal.foto`.
5. Genera el PDF:
```bash
python3 generar_cv.py
```
6. Resultado: `CV.pdf` (y `CV.html` para revisar rápido en el navegador antes de generar el PDF).

## Personalizar el diseño
Todo el diseño vive en `templates/cv.html` (HTML + CSS embebido). Cosas fáciles de cambiar:
- Color de acento: variable `--accent` en el `<style>`.
- Tamaño de página: `@page { size: Letter; }` → cámbialo a `A4` si prefieres.
- Layout de columnas: `.col-main` (62%) y `.col-side` (38%) usan `float`, no flexbox,
  porque WeasyPrint no reparte contenido flex entre páginas correctamente.

## Estructura
```
cv-generator/
├── Dockerfile           <- imagen para correr sin instalar nada localmente
├── .dockerignore
├── .gitignore
├── requirements.txt      <- dependencias Python
├── data.example.yaml    <- plantilla de datos (SÍ se sube a Git)
├── data.yaml             <- tus datos reales (NO se sube, créalo con cp)
├── generar_cv.py         <- script que arma el PDF
├── img/
│   └── foto.jpg          <- tu foto de perfil (opcional)
└── templates/
    └── cv.html           <- plantilla y diseño (SÍ se sube, no tiene datos personales)
```

## Subir a GitHub
El `.gitignore` ya excluye `venv/`, tu `data.yaml` real, los PDF/HTML generados,
y archivos de sistema (`.DS_Store`, etc.). `data.example.yaml` y `templates/cv.html`
sí se suben porque no tienen información personal — son la plantilla reutilizable.

Si NO quieres que tu foto real quede pública en el repo, descomenta la línea
`img/foto.jpg` dentro de `.gitignore` antes de tu primer commit.

```bash
git init
git add .
git commit -m "Generador de CV inicial"
git remote add origin <tu-repo-url>
git push -u origin main
```

Cualquiera que clone el repo simplemente hace `cp data.example.yaml data.yaml`
y personaliza su copia, sin riesgo de subir accidentalmente sus datos.

## Agregar foto de perfil
1. Coloca tu foto (recomendado: cuadrada, mínimo 300x300px, .jpg o .png) dentro
   de la carpeta `img/`.
2. En `data.yaml`, dentro de `personal:`, agrega o descomenta:
   ```yaml
   foto: "img/foto.jpg"
   ```
3. Para quitarla de nuevo, comenta o borra esa línea — la plantilla ya tiene un
   `{% if personal.foto %}` que la oculta automáticamente si no existe.

Nota: si tu título profesional es muy largo, puede envolver a dos líneas y
descuadrar un poco el header — si pasa eso, acórtalo o baja el font-size de
`.subtitle` en `templates/cv.html`.

## Variantes (ej: CV para otra vacante)
```bash
cp data.yaml data_backend.yaml
# edita data_backend.yaml
python3 generar_cv.py --data data_backend.yaml --out CV_backend.pdf
```
