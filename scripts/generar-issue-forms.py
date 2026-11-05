#!/usr/bin/env python3
"""
Genera los 4 Issue Forms (YAML) del laboratorio ElectroHogar.

Cada formulario es INDEPENDIENTE: cubre una caracteristica front-stage de
ISO/IEC 25010 y audita UN SOLO problema por Issue.

Se escribe el YAML a mano (string) porque yaml.dump genera alias (*id001)
que el renderer de GitHub rechaza con "Alias parsing was not enabled".
"""
import os

BASE = os.path.dirname(os.path.abspath(__file__))
DESTINO = os.path.join(BASE, '..', '.github', 'ISSUE_TEMPLATE')
os.makedirs(DESTINO, exist_ok=True)

URL_LAB = 'https://krizrome.github.io/intro-si-iso25010-lab/'

CAMPOS_ESTUDIANTE = '''  - type: input
    id: estudiante
    attributes:
      label: Nombre completo del estudiante
      placeholder: Juan Perez Rojas
    validations:
      required: true

  - type: input
    id: correo
    attributes:
      label: Correo institucional
      placeholder: juan.perez@educa.edu.pe
    validations:
      required: true

  - type: input
    id: sistema_auditado
    attributes:
      label: Sistema auditado
      value: ElectroHogar
    validations:
      required: true
'''


def bloque_evidencia(requerido=True):
    req = 'true' if requerido else 'false'
    return '''  - type: textarea
    id: evidencia
    attributes:
      label: Evidencia
      description: Que observaste o mediste que demuestra el problema. Escribe en tus propias palabras.
      placeholder: "Al escribir una sola letra en el buscador, la pagina se queda pegada medio segundo"
    validations:
      required: %s

  - type: upload
    id: captura
    attributes:
      label: Capturas de pantalla
      description: Adjunta la imagen que demuestra el problema. PNG o JPG hasta 10 MB.
    validations:
      required: false
''' % req


VERIFICACION = '''  - type: checkboxes
    id: verificacion
    attributes:
      label: Verificacion antes de enviar
      options:
        - label: Abri el sitio y confirme que el problema sigue presente
          required: true
        - label: Documento un solo problema en este Issue
          required: true
        - label: Adjunte la evidencia que lo demuestra
          required: false
'''


def encabezado(nombre, descripcion, titulo, etiqueta):
    return '''name: %s
description: %s
title: "%s"
labels: ["hallazgo", "%s"]
body:
  - type: markdown
    attributes:
      value: |
        Reporta UN SOLO problema de %s.

        El sitio auditado es: %s

        Requisitos: el problema debe ser visible por el usuario final (front-stage).
        Cada hallazgo se reporta en un Issue independiente.

''' % (nombre, descripcion, titulo, etiqueta, etiqueta, URL_LAB)


# ---------------------------------------------------------------- RENDIMIENTO
RENDIMIENTO = encabezado(
    'Hallazgo de Rendimiento (front-stage)',
    'Reporta UN problema de rendimiento que sufre el usuario en ElectroHogar.',
    '[Rendimiento] ', 'rendimiento') + CAMPOS_ESTUDIANTE + '''  - type: dropdown
    id: pagina
    attributes:
      label: Pagina donde se observa el problema
      options:
        - Inicio y catalogo
        - Detalle de producto
        - Carrito
        - Finalizar compra
        - Mi cuenta
        - Todas las paginas
    validations:
      required: true

  - type: dropdown
    id: subcaracteristica
    attributes:
      label: Que falla exactamente (elige una sola)
      options:
        - Tiempo de respuesta o carga lenta de la pagina
        - "Recursos pesados - imagenes, scripts o fuentes sin optimizar"
        - Trabajo de CPU que bloquea la interaccion
        - Peticiones excesivas al servidor
        - Ninguna de las anteriores (describir en el detalle)
    validations:
      required: true

  - type: textarea
    id: elemento
    attributes:
      label: Elemento que falla
      description: Describe QUE elemento concreto falla, no la pagina entera.
      placeholder: "Las 8 imagenes de producto del catalogo"
    validations:
      required: true

  - type: textarea
    id: fallo
    attributes:
      label: Como se manifiesta el fallo
      description: Que le pasa al usuario. Usa tus propias palabras.
      placeholder: "La pagina tarda mucho en mostrar los productos y el scroll se congela"
    validations:
      required: true

  - type: textarea
    id: reproduccion
    attributes:
      label: Como reproducirlo
      description: Pasos numerados para que otro alumno lo vea igual.
      placeholder: "1. Abrir Inicio  2. Esperar la carga  3. Desplazar la pagina"
    validations:
      required: true

''' + bloque_evidencia() + '''  - type: dropdown
    id: severidad
    attributes:
      label: Severidad
      options:
        - Baja - molesto pero el usuario puede seguir trabajando
        - Media - dificulta la tarea y obliga a esperar
        - Alta - impide o hace muy costoso completar la compra
    validations:
      required: true

  - type: dropdown
    id: impacto_usuario
    attributes:
      label: Que usuario se ve afectado
      options:
        - Todos los usuarios
        - Usuarios con conexion lenta
        - Usuarios en dispositivos moviles
        - Usuarios con equipos antiguos o de bajo rendimiento
    validations:
      required: true

  - type: textarea
    id: solucion
    attributes:
      label: Solucion propuesta
      description: Un cambio concreto y verificable que resolveria el problema.
      placeholder: "Comprimir las imagenes a WebP y agregar loading=lazy a cada imagen"
    validations:
      required: true

  - type: textarea
    id: conclusion
    attributes:
      label: Conclusion tecnica
      description: Veredicto final en una o dos lineas.
      placeholder: "El sitio entrega 15 MB de imagenes sin comprimir antes de mostrar el catalogo"
    validations:
      required: true

''' + VERIFICACION


# ---------------------------------------------------------------- USABILIDAD
USABILIDAD = encabezado(
    'Hallazgo de Usabilidad (front-stage)',
    'Reporta UN problema de usabilidad que dificulta usar ElectroHogar.',
    '[Usabilidad] ', 'usabilidad') + CAMPOS_ESTUDIANTE + '''  - type: dropdown
    id: pagina
    attributes:
      label: Pagina donde se observa el problema
      options:
        - Inicio y catalogo
        - Detalle de producto
        - Carrito
        - Finalizar compra
        - Mi cuenta
        - Todas las paginas
    validations:
      required: true

  - type: dropdown
    id: subcaracteristica
    attributes:
      label: Que falla exactamente (elige una sola)
      options:
        - El usuario no entiende que hacer a continuacion
        - El resultado no corresponde a lo que el usuario pidio
        - Falta informacion o retroalimentacion al usuario
        - El control es dificil de usar o de alcanzar
        - El sistema no se adapta a la forma de trabajar del usuario
        - Ninguna de las anteriores (describir en el detalle)
    validations:
      required: true

  - type: textarea
    id: elemento
    attributes:
      label: Elemento que falla
      description: Describe QUE elemento concreto falla, no la pagina entera.
      placeholder: "El boton de quitar producto del carrito"
    validations:
      required: true

  - type: textarea
    id: fallo
    attributes:
      label: Como se manifiesta el fallo
      description: Que le pasa al usuario. Usa tus propias palabras.
      placeholder: "Escribo laptop en el buscador y sigue mostrando los 8 productos como si nada"
    validations:
      required: true

  - type: textarea
    id: reproduccion
    attributes:
      label: Como reproducirlo
      description: Pasos numerados para que otro alumno lo vea igual.
      placeholder: "1. Entrar a Inicio  2. Poner 500 en precio desde  3. Poner 2000 en precio hasta"
    validations:
      required: true

''' + bloque_evidencia() + '''  - type: dropdown
    id: severidad
    attributes:
      label: Severidad
      options:
        - Baja - molesto pero el usuario puede seguir trabajando
        - Media - dificulta la tarea y obliga a corregir el paso
        - Alta - impide o hace muy costoso completar la compra
    validations:
      required: true

  - type: dropdown
    id: principio
    attributes:
      label: Principio de usabilidad relacionado
      options:
        - Visibilidad del estado del sistema
        - Correspondencia con el mundo real
        - Control y libertad del usuario
        - Consistencia y estandar
        - Prevention of errors (prevenir errores)
        - Reconocer en vez de recordar
        - Flexibilidad y eficiencia de uso
        - No puedo identificarlo con seguridad
    validations:
      required: true

  - type: textarea
    id: solucion
    attributes:
      label: Solucion propuesta
      description: Un cambio concreto y verificable que resolveria el problema.
      placeholder: "Invertir la comparacion del filtro para que muestre los productos dentro del rango"
    validations:
      required: true

  - type: textarea
    id: conclusion
    attributes:
      label: Conclusion tecnica
      description: Veredicto final en una o dos lineas.
      placeholder: "El filtro de precio hace lo contrario de lo que dice: descarta los productos que estan en el rango"
    validations:
      required: true

''' + VERIFICACION


# ---------------------------------------------------------------- COMPATIBILIDAD
COMPATIBILIDAD = encabezado(
    'Hallazgo de Compatibilidad (front-stage)',
    'Reporta UN problema de compatibilidad del sitio en el navegador o el dispositivo.',
    '[Compatibilidad] ', 'compatibilidad') + CAMPOS_ESTUDIANTE + '''  - type: dropdown
    id: pagina
    attributes:
      label: Pagina donde se observa el problema
      options:
        - Inicio y catalogo
        - Detalle de producto
        - Carrito
        - Finalizar compra
        - Mi cuenta
        - Todas las paginas
    validations:
      required: true

  - type: dropdown
    id: subcaracteristica
    attributes:
      label: Que falla exactamente (elige una sola)
      options:
        - El contenido no se ve bien en pantallas pequenas
        - El texto tiene poco contraste y no se lee
        - El sitio depende de una tipografia que no siempre esta disponible
        - Falta soporte para technologies del navegador
        - Ninguna de las anteriores (describir en el detalle)
    validations:
      required: true

  - type: textarea
    id: elemento
    attributes:
      label: Elemento que falla
      description: Describe QUE elemento concreto falla, no la pagina entera.
      placeholder: "El precio tachado y la marca de cada producto"
    validations:
      required: true

  - type: textarea
    id: fallo
    attributes:
      label: Como se manifiesta el fallo
      description: Que le pasa al usuario. Usa tus propias palabras.
      placeholder: "Abro el sitio en el celular y tengo que mover la pantalla de lado para ver el precio"
    validations:
      required: true

  - type: textarea
    id: reproduccion
    attributes:
      label: Como reproducirlo
      description: Pasos numerados y, si aplica, el navegador y el tamano de pantalla.
      placeholder: "1. Reducir la ventana del navegador a 390 px de ancho  2. Ver la barra lateral"
    validations:
      required: true

''' + bloque_evidencia() + '''  - type: dropdown
    id: severidad
    attributes:
      label: Severidad
      options:
        - Baja - molesto pero el usuario puede seguir trabajando
        - Media - dificulta la lectura o la navegacion
        - Alta - impide o hace muy costoso completar la compra
    validations:
      required: true

  - type: dropdown
    id: entorno
    attributes:
      label: Entorno donde lo observaste
      options:
        - Computadora de escritorio
        - Celular o tablet
        - Navegador con tamano de ventana reducido
        - Varios dispositivos a la vez
    validations:
      required: true

  - type: textarea
    id: solucion
    attributes:
      label: Solucion propuesta
      description: Un cambio concreto y verificable que resolveria el problema.
      placeholder: "Usar consultas de medios y un color de texto con contraste 4.5:1 o mas"
    validations:
      required: true

  - type: textarea
    id: conclusion
    attributes:
      label: Conclusion tecnica
      description: Veredicto final en una o dos lineas.
      placeholder: "El cuerpo tiene un ancho minimo fijo de 1200 px, por eso en movil hay desplazamiento horizontal"
    validations:
      required: true

''' + VERIFICACION


# ---------------------------------------------------------------- FUNCIONALIDAD
FUNCIONALIDAD = encabezado(
    'Hallazgo de Funcionalidad (front-stage)',
    'Reporta UN problema de funcionalidad del sitio ElectroHogar.',
    '[Funcionalidad] ', 'funcionalidad') + CAMPOS_ESTUDIANTE + '''  - type: dropdown
    id: pagina
    attributes:
      label: Pagina donde se observa el problema
      options:
        - Inicio y catalogo
        - Detalle de producto
        - Carrito
        - Finalizar compra
        - Mi cuenta
        - Todas las paginas
    validations:
      required: true

  - type: dropdown
    id: subcaracteristica
    attributes:
      label: Que falla exactamente (elige una sola)
      options:
        - La accion no produce el resultado que promete
        - Falta validacion de los datos que se ingresan
        - El control no tiene nombre accesible ni se puede identificar
        - El sistema pierde o no guarda informacion del usuario
        - Ninguna de las anteriores (describir en el detalle)
    validations:
      required: true

  - type: textarea
    id: elemento
    attributes:
      label: Elemento que falla
      description: Describe QUE elemento concreto falla, no la pagina entera.
      placeholder: "El campo de numero de tarjeta en Finalizar compra"
    validations:
      required: true

  - type: textarea
    id: fallo
    attributes:
      label: Como se manifiesta el fallo
      description: Que le pasa al usuario. Usa tus propias palabras.
      placeholder: "Pongo 123 en el numero de tarjeta y el sitio me confirma el pedido como si estuviera bien"
    validations:
      required: true

  - type: textarea
    id: reproduccion
    attributes:
      label: Como reproducirlo
      description: Pasos numerados para que otro alumno lo vea igual.
      placeholder: "1. Entrar a Finalizar compra  2. Llenar los datos  3. Poner 123 en la tarjeta  4. Confirmar"
    validations:
      required: true

''' + bloque_evidencia() + '''  - type: dropdown
    id: severidad
    attributes:
      label: Severidad
      options:
        - Baja - molesto pero el usuario puede seguir trabajando
        - Media - dificulta la tarea y puede generar un error
        - Alta - provoca una perdida o un cobro incorrecto
    validations:
      required: true

  - type: dropdown
    id: impacto_usuario
    attributes:
      label: Que usuario se ve afectado
      options:
        - Todos los usuarios
        - Solo usuarios que compran
        - Usuarios que usan tecnologias de asistencia
        - Usuarios que confianza en el sistema para pagar
    validations:
      required: true

  - type: textarea
    id: solucion
    attributes:
      label: Solucion propuesta
      description: Un cambio concreto y verificable que resolveria el problema.
      placeholder: "Validar el numero de tarjeta con una expresion regular antes de confirmar el pedido"
    validations:
      required: true

  - type: textarea
    id: conclusion
    attributes:
      label: Conclusion tecnica
      description: Veredicto final en una o dos lineas.
      placeholder: "El formulario no valida los datos de la tarjeta y acepta cualquier texto como numero valido"
    validations:
      required: true

''' + VERIFICACION


ARCHIVOS = {
    'hallazgo-rendimiento.yml': RENDIMIENTO,
    'hallazgo-usabilidad.yml': USABILIDAD,
    'hallazgo-compatibilidad.yml': COMPATIBILIDAD,
    'hallazgo-funcionalidad.yml': FUNCIONALIDAD,
}


def main():
    for nombre, contenido in ARCHIVOS.items():
        ruta = os.path.join(DESTINO, nombre)
        with open(ruta, 'w', encoding='utf-8') as f:
            f.write(contenido)
        print('escrito: %s (%d bytes)' % (nombre, len(contenido)))


if __name__ == '__main__':
    main()
