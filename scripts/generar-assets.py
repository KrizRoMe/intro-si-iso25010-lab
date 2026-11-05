#!/usr/bin/env python3
"""
Genera los recursos graficos del laboratorio ElectroHogar.

Los archivos se guardan SIN optimizar a propósito: son el soporte del
problema de RENDIMIENTO "imagenes sin comprimir / sin lazy-loading".
"""
import os
import random
from PIL import Image, ImageDraw

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
SALIDA = os.path.join(BASE, 'assets', 'productos')
os.makedirs(SALIDA, exist_ok=True)

PALETAS = {
    'audifonos':   ((28, 42, 74), (86, 176, 240)),
    'licuadora':   ((120, 60, 30), (232, 168, 76)),
    'laptop':      ((24, 30, 46), (110, 130, 180)),
    'tv':          ((32, 20, 52), (150, 96, 210)),
    'cafetera':    ((74, 34, 26), (214, 120, 84)),
    'teclado':     ((18, 24, 30), (72, 92, 116)),
    'tablet':      ((20, 44, 52), (86, 190, 170)),
    'smartwatch':  ((46, 22, 34), (208, 104, 140)),
    'portada':     ((6, 90, 130), (96, 165, 250)),
}


def dibujar(d, w, h, color_a, color_b, semilla):
    """Rellena el lienzo con un degradado y formas geometricas."""
    rnd = random.Random(semilla)
    for y in range(h):
        t = y / max(1, h - 1)
        c = tuple(int(color_a[i] + (color_b[i] - color_a[i]) * t) for i in range(3))
        d.line([(0, y), (w, y)], fill=c)

    for _ in range(26):
        x = rnd.randint(-w // 4, w)
        y = rnd.randint(-h // 4, h)
        r = rnd.randint(int(w * 0.06), int(w * 0.30))
        alpha = rnd.randint(12, 40)
        d.ellipse([x, y, x + r, y + r], outline=(255, 255, 255, alpha), width=rnd.randint(3, 14))

    d.rectangle([0, int(h * 0.62), w, h], fill=(0, 0, 0, 55))
    d.rectangle([0, int(h * 0.62), w, int(h * 0.62) + 6], fill=(255, 255, 255, 70))


def agregar_ruido(img, cantidad=14, semilla=1):
    """Anade ruido granular: es lo que impide que el JPEG se comprima bien.

    Reproduce el caso real de fotos de producto sin optimizar.
    """
    rnd = random.Random(semilla)
    px = img.load()
    w, h = img.size
    for y in range(h):
        for x in range(w):
            n = rnd.randint(-cantidad, cantidad)
            r, g, b = px[x, y]
            px[x, y] = (
                max(0, min(255, r + n)),
                max(0, min(255, g + n)),
                max(0, min(255, b + n)),
            )


def main():
    # Imagenes de producto: 2600x1950 px, JPEG calidad 92 + ruido
    # -> ~600-900 KB cada una. 8 productos = ~6 MB en una sola pagina.
    productos = ['audifonos', 'licuadora', 'laptop', 'tv', 'cafetera', 'teclado', 'tablet', 'smartwatch']
    for i, nombre in enumerate(productos):
        w, h = 2600, 1950
        img = Image.new('RGB', (w, h), (20, 20, 20))
        d = ImageDraw.Draw(img, 'RGBA')
        a, b = PALETAS[nombre]
        dibujar(d, w, h, a, b, i + 7)
        d.text((60, 60), nombre.upper(), fill=(255, 255, 255, 210))
        agregar_ruido(img, 16, i + 31)
        ruta = os.path.join(SALIDA, nombre + '.jpg')
        img.save(ruta, 'JPEG', quality=92, optimize=False)
        peso = os.path.getsize(ruta) / 1024.0
        print('producto  %-12s %-28s %8.1f KB' % (nombre, os.path.basename(ruta), peso))

    # Portada: 2800x1200 px
    w, h = 2800, 1200
    img = Image.new('RGB', (w, h), (10, 60, 90))
    d = ImageDraw.Draw(img, 'RGBA')
    dibujar(d, w, h, PALETAS['portada'][0], PALETAS['portada'][1], 99)
    agregar_ruido(img, 14, 77)
    ruta = os.path.join(BASE, 'assets', 'portada.jpg')
    img.save(ruta, 'JPEG', quality=92, optimize=False)
    print('portada   %-12s %-28s %8.1f KB' % ('', os.path.basename(ruta), os.path.getsize(ruta) / 1024.0))


if __name__ == '__main__':
    main()
