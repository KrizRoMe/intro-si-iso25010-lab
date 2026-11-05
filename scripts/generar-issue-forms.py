#!/usr/bin/env python3
"""
Genera el Issue Form (YAML) unico del laboratorio ElectroHogar.

Un SOLO formulario para todos los hallazgos: el alumno elige la
caracteristica ISO/IEC 25010 (Rendimiento, Usabilidad, Compatibilidad,
Funcionalidad) en un selector desplegable y audita UN SOLO problema.

Solo 7 campos, los indispensables:
  1. Nombre completo del estudiante
  2. Tipo de hallazgo (selector)
  3. Pagina donde lo observaste (selector)
  4. Que problema encontraste (texto: que falla + a quien afecta + como se reproduce)
  5. Evidencia
  6. Captura de pantalla (adjunto, opcional)
  7. Solucion propuesta

Se escribe el YAML a mano (string) porque yaml.dump genera alias (*id001)
que el renderer de GitHub rechaza con "Alias parsing was not enabled".
"""
import os

BASE = os.path.dirname(os.path.abspath(__file__))
DESTINO = os.path.join(BASE, '..', '.github', 'ISSUE_TEMPLATE')
os.makedirs(DESTINO, exist_ok=True)

URL_LAB = 'https://krizrome.github.io/intro-si-iso25010-lab/'

FORMULARIO = '''name: Reporte de Hallazgo (front-stage)
description: Reporta UN problema de calidad front-stage (ISO/IEC 25010) encontrado en ElectroHogar.
title: "[Hallazgo] "
labels: ["hallazgo"]
body:
  - type: markdown
    attributes:
      value: |
        Reporta **UN SOLO** problema del sitio ElectroHogar: %(url)s

  - type: input
    id: estudiante
    attributes:
      label: Nombre completo del estudiante
      placeholder: Juan Perez Rojas
    validations:
      required: true

  - type: dropdown
    id: tipo_hallazgo
    attributes:
      label: Tipo de hallazgo - caracteristica ISO/IEC 25010
      description: Elige la caracteristica que mejor describa el problema.
      options:
        - Rendimiento
        - Usabilidad
        - Compatibilidad
        - Funcionalidad
    validations:
      required: true

  - type: dropdown
    id: pagina
    attributes:
      label: Pagina donde lo observaste
      options:
        - Inicio y catalogo
        - Detalle de producto
        - Carrito
        - Finalizar compra
        - Mi cuenta
        - Todas las paginas
    validations:
      required: true

  - type: textarea
    id: problema
    attributes:
      label: Que problema encontraste
      description: "Que falla, a quien le afecta y como se reproduce. Un solo problema por Issue."
      placeholder: |
        Que falla: el filtro de precio no me muestra los productos del rango que pido.
        A quien afecta: a cualquiera que quiera comprar por precio.
        Como se reproduce: en Inicio, pongo minimo 500 y maximo 2000, y me salen productos fuera del rango.
    validations:
      required: true

  - type: textarea
    id: evidencia
    attributes:
      label: Evidencia
      description: "Que mediste u observaste que demuestra el problema."
      placeholder: "Ninguno de los 6 productos que me aparece esta dentro del rango 500-2000."
    validations:
      required: true

  - type: upload
    id: captura
    attributes:
      label: Captura de pantalla
      description: "Adjunta la imagen que demuestra el problema. PNG o JPG hasta 10 MB."
    validations:
      required: false

  - type: textarea
    id: solucion
    attributes:
      label: Solucion propuesta
      description: "Un cambio concreto que resolveria el problema."
      placeholder: "Invertir la comparacion del filtro para que muestre los productos dentro del rango."
    validations:
      required: true
''' % {'url': URL_LAB}


def main():
    ruta = os.path.join(DESTINO, 'hallazgo.yml')
    with open(ruta, 'w', encoding='utf-8') as f:
        f.write(FORMULARIO)
    print('escrito: hallazgo.yml (%d bytes)' % len(FORMULARIO))

    # Limpia formularios antiguos que ya no aplican
    for viejo in ('hallazgo-rendimiento.yml', 'hallazgo-usabilidad.yml',
                  'hallazgo-compatibilidad.yml', 'hallazgo-funcionalidad.yml'):
        ruta_vieja = os.path.join(DESTINO, viejo)
        if os.path.exists(ruta_vieja):
            os.remove(ruta_vieja)
            print('eliminado: %s' % viejo)


if __name__ == '__main__':
    main()
