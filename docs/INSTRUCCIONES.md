# Instrucciones para el alumno — Auditoría ISO/IEC 25010 (front-stage)

**Curso:** Introducción a los Sistemas de Información (INTRO SI)
**Sitio auditado:** <https://krizrome.github.io/intro-si-iso25010-lab/>

---

## 1. Qué vas a hacer

El sitio **ElectroHogar** es una tienda en línea que funciona, pero tiene
**12 problemas intencionales** escondidos. Tu tarea es encontrarlos y
documentarlos.

Los problemas se evalúan con el modelo de calidad **ISO/IEC 25010**, y
solamente con el **hemisferio front-stage**: lo que el usuario final ve y
sufre. No necesitas ver el código, ni entrar a la base de datos, ni
configurar servidores.

---

## 2. Las 4 características que vas a auditar

| Característica | Significado | Pregunta que te harás |
|---|---|---|
| **Usabilidad** | Usabilidad | ¿Es intuitivo y fácil de usar? |
| **Funcionalidad** | Funcionalidad | ¿Hace exactamente lo que promete? |
| **Rendimiento** | Rendimiento | ¿Responde rápido? |
| **Compatibilidad** | Compatibilidad | ¿Funciona en mi navegador y mi pantalla? |

---

## 3. Reglas de la entrega

1. **Un Issue por problema.** Si encuentras 3 problemas, abres 3 Issues.
2. **Cada Issue audita UN SOLO problema.** No mezcles varios en un mismo reporte.
3. **Usa el formulario que corresponde** a la característica del problema.
4. **Verifica antes de reportar.** El problema debe seguir presente cuando lo abras de nuevo.
5. **Escribe con tus propias palabras.** Las respuestas redactadas por IA se detectan y se penalizan.
6. **Adjunta la evidencia.** Una captura de pantalla de DevTools vale más que un párrafo.
7. **No reportes problemas del back-stage** (seguridad del servidor, base de datos, código interno). Esos no se evalúan aquí.

---

## 4. Cómo abrir tu reporte

Hay **un solo formulario** para todos los hallazgos. Cuando lo abres, lo
primero que aparece es un **selector** donde eliges el **tipo de hallazgo**
que encontraste.

### Opción A — desde el repositorio (recomendada)

Abre la pestaña **New issue** del repositorio:

<https://github.com/KrizRoMe/intro-si-iso25010-lab/issues/new>

Te aparecerá el formulario **Reporte de Hallazgo (front-stage)**. Es el único,
así que no hay que elegir entre varias opciones.

### Opción B — enlace directo

<https://github.com/KrizRoMe/intro-si-iso25010-lab/issues/new?template=hallazgo.yml>

> **Abre el laboratorio en otra pestaña** antes de llenar el formulario. La
> evidencia tiene que venir del sitio real.

---

## 5. Qué pide el formulario

Son 16 campos, siempre en el mismo orden:

### Identificación
- **Nombre completo** — tal como figura en el curso
- **Sistema auditado** — ya viene con `ElectroHogar`

### Clasificación (aquí eliges el tipo de hallazgo)
- **Tipo de hallazgo — característica ISO/IEC 25010** ← **este es el selector**
  - Rendimiento
  - Usabilidad
  - Compatibilidad
  - Funcionalidad
- **Página donde se observa el problema** (selector)
- **Aspecto que falla** (selector con el mecanismo general del fallo)

### El hallazgo
- **Elemento que falla** — el elemento concreto, no "toda la página"
- **Cómo se manifiesta el fallo** — qué le pasa al usuario, con tus propias palabras
- **Cómo reproducirlo** — pasos numerados, para que otro alumno lo vea igual

### Evidencia
- **Evidencia** — qué mediste u observaste
- **Capturas de pantalla** — adjunta la imagen que lo demuestra

### Evaluación y solución
- **Severidad** (selector) y **Usuario afectado** (selector)
- **Solución propuesta** — un cambio concreto y verificable
- **Conclusión técnica** — veredicto final en una o dos líneas

### Cierre
- Tres casillas de verificación antes de enviar.

---

## 6. Ejemplo de cómo se ve un buen reporte

> **Tipo de hallazgo:** Funcionalidad
>
> **Elemento que falla:** El campo de número de tarjeta en la página Finalizar compra.
>
> **Cómo se manifiesta el fallo:** Pongo 123 en el número de tarjeta y el sitio me confirma el pedido igual, como si el dato fuera válido. El usuario cree que todo está en orden y se lleva un cargo sin tarjeta real.
>
> **Cómo reproducirlo:**
> 1. Entrar a "Finalizar compra".
> 2. Llenar nombre, dirección, ciudad y tipo de envío.
> 3. Elegir "Tarjeta de crédito o débito" como método de pago.
> 4. Escribir `123` en el número de tarjeta y `1` en el CVV.
> 5. Presionar "Confirmar pedido".
> 6. Aparece "Pedido confirmado. Número de pedido EH-2026-004312".
>
> **Evidencia:** Adjunto la captura del pedido confirmado con la tarjeta 123. El formulario no marca ningún campo en rojo ni avisa que el dato es inválido.
>
> **Solución propuesta:** Validar el número de tarjeta con una expresión regular (16 dígitos, pasar Luhn) antes de confirmar, y mostrar el error junto al campo, no solo arriba del formulario.
>
> **Conclusión técnica:** El formulario no valida los datos de pago y acepta cualquier texto como número de tarjeta válido.

---

## 7. Herramientas para buscar los problemas

No tienes que instalar nada. Todo se hace desde el navegador:

| Para encontrar | Usa |
|---|---|
| Problemas de **rendimiento** | DevTools → **Network**: mira el peso de cada imagen y si cargan todas de golpe. DevTools → **Performance**: mira el tiempo de bloqueo. En la consola escribe `window.EH_LEGACY.tiempoBloqueo` |
| Problemas de **compatibilidad** | DevTools → **Elements**: busca atributos y estilos. DevTools → **Rendering** → *Contrast ratio*. Reduce la ventana del navegador a menos de 900 px de ancho |
| Problemas de **usabilidad** | Usa el sitio como usuario: busca, filtra, escribe mal, presiona sin querer. Pregúntate "¿qué esperaba que pasara y qué pasó?" |
| Problemas de **funcionalidad** | Completa el flujo real: agregar al carrito, cambiar cantidad, pagar. Contrasta lo que el sitio promete con lo que hace |

**Pistas de navegación** (sin decirte la respuesta):

- El catálogo tiene buscador y filtros de precio.
- El carrito permite cambiar cantidades.
- El checkout pide datos de tarjeta y de envío.
- En "Mi cuenta" hay un formulario de inicio de sesión.
- En cualquier página hay un banner de cookies abajo.

---

## 8. Antes de enviar, revisa

- [ ] ¿Abrí el sitio y confirmé que el problema sigue presente?
- [ ] ¿Escribí **un solo problema** en este Issue?
- [ ] ¿Especifiqué el elemento concreto, no "toda la página"?
- [ ] ¿Dije **cómo reproducirlo** con pasos numerados?
- [ ] ¿Adjunté la evidencia (captura) que lo demuestra?
- [ ] ¿Escribí con mis propias palabras?
- [ ] ¿Mi nombre está correctamente escrito?
- [ ] ¿No reporté algo del back-stage?

---

## 9. Dudas

Si tienes una duda sobre el marco ISO/IEC 25010 o sobre cómo llenar un campo
del formulario, consúltalo durante la sesión. Todo el trabajo se realiza
dentro del horario de clase.
