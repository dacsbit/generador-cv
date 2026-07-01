#!/usr/bin/env python3
"""
Generador de CV en PDF.
Lee data.yaml, lo inyecta en templates/cv.html con Jinja2,
y convierte el resultado a PDF con WeasyPrint.

Uso:
    python3 generar_cv.py
    python3 generar_cv.py --data otro_data.yaml --out otro_nombre.pdf
"""

import argparse
import sys
from pathlib import Path

import yaml
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML

BASE_DIR = Path(__file__).parent


def generar_cv(data_path: Path, template_name: str, output_path: Path):
    if not data_path.exists():
        print(f"❌ No se encontró el archivo de datos: {data_path}")
        sys.exit(1)

    with open(data_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    env = Environment(loader=FileSystemLoader(BASE_DIR / "templates"))
    template = env.get_template(template_name)
    html_renderizado = template.render(**data)

    # Guardamos también el HTML renderizado, útil para revisar/depurar en el navegador
    html_debug_path = output_path.with_suffix(".html")
    with open(html_debug_path, "w", encoding="utf-8") as f:
        f.write(html_renderizado)

    HTML(string=html_renderizado, base_url=str(BASE_DIR)).write_pdf(str(output_path))

    print(f"✅ CV generado: {output_path}")
    print(f"   (HTML de depuración: {html_debug_path})")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Genera un CV en PDF a partir de un YAML + plantilla HTML.")
    parser.add_argument("--data", default="data.yaml", help="Archivo YAML con los datos del CV")
    parser.add_argument("--template", default="cv.html", help="Nombre de la plantilla dentro de templates/")
    parser.add_argument("--out", default="CV.pdf", help="Nombre del archivo PDF de salida")
    args = parser.parse_args()

    generar_cv(BASE_DIR / args.data, args.template, BASE_DIR / args.out)
