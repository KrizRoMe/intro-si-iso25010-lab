# ElectroHogar — Laboratorio de auditoría ISO/IEC 25010 (front-stage)

Tienda en línea ficticia con **12 problemas intencionales** que deben ser
identificados y documentados por los alumnos del curso
**Introducción a los Sistemas de Información**.

El sitio funciona: es un e-commerce real (catálogo, detalle de producto,
carrito, checkout y cuenta). Los defectos están **solo en el hemisferio
front-stage**, es decir, en lo que el usuario final ve y sufre.

---

## 🎯 Qué se evalúa

La norma **ISO/IEC 25010** define la calidad del producto software en 9
características. Este laboratorio se enfoca **exclusivamente en las 4
características que el usuario final puede verificar sin ver el código**:

| Característica | Pregunta que responde |
|---|---|
| **Usabilidad** | ¿Es intuitivo y fácil de operar? |
| **Funcionalidad** | ¿Hace exactamente lo que promete? |
| **Rendimiento** | ¿Responde rápido bajo carga? |
| **Compatibilidad** | ¿Funciona en diferentes navegadores y pantallas? |

> El hemisferio **back-stage** (seguridad, fiabilidad, mantenibilidad,
> portabilidad) queda fuera de este laboratorio: se evalúa con acceso al
> código o a la infraestructura, no desde la interfaz.

### Los 12 problemas del sitio

| # | Código | Característica | Problema |
|---|---|---|---|
| 1 | R01 | Rendimiento | Imágenes de 2600×1950 px (~2 MB cada una) sin `loading="lazy"`: se descargan las 8 antes de pintar |
| 2 | R02 | Rendimiento | `app-legacy.js` se carga **bloqueante** en el `<head>` sin `defer` ni `async` |
| 3 | R03 | Rendimiento | Trabajo de CPU **síncrono** en cada carga: matriz de 220×220 SKUs + 6000 hashes precalculados |
| 4 | U01 | Usabilidad | El filtro de precio está **invertido**: descarta los productos que **sí** están en el rango |
| 5 | U02 | Usabilidad | La búsqueda que no encuentra nada **oculta las tarjetas y no avisa** ("no se encontraron productos" nunca aparece) |
| 6 | U03 | Usabilidad | El campo de contraseña es `type="text"`: la clave se ve en texto plano |
| 7 | C01 | Compatibilidad | Texto secundario con contraste **1.84:1 a 1.98:1** (WCAG AA exige 4.5:1) |
| 8 | C02 | Compatibilidad | `body { min-width: 1200px }`: en móvil hay desbordamiento horizontal de 1200 px |
| 9 | C03 | Compatibilidad | Tipografía del sistema sin `font-display` ni fallback web; el render cambia por SO |
| 10 | F01 | Funcionalidad | El botón de quitar del carrito es una "×" de 16×16 px **sin `aria-label` ni `title`** |
| 11 | F02 | Funcionalidad | Acepta un número de tarjeta inválido (`123`) y **confirma el pedido** sin validar |
| 12 | F03 | Funcionalidad | El total del carrito **no se actualiza** al cambiar la cantidad (2 × S/ 149 sigue marcando S/ 149) |

Además hay **variantes secundarias** documentables (búsqueda sin botón ni
Enter, quitar producto sin confirmación, el banner de cookies tapa el botón
de pago, el error del formulario no marca qué campo falló).

---

## 🚀 Cómo usar el sitio

El laboratorio está publicado y funciona desde el navegador:

**<https://krizrome.github.io/intro-si-iso25010-lab/>**

Rutas disponibles:

| Página | URL |
|---|---|
| Inicio y catálogo | `/index.html` |
| Detalle de producto | `/producto.html?id=3` |
| Carrito | `/carrito.html` |
| Finalizar compra | `/checkout.html` |
| Mi cuenta | `/cuenta.html` |

### Para probarlo en local

```bash
python3 -m http.server 8765
# abrir http://127.0.0.1:8765/index.html
```

---

## 📋 Entrega: un Issue por problema

Hay **un solo formulario** de reporte. Al ingresarlo, el alumno elige en un
**selector desplegable** el tipo de hallazgo encontrado (la característica de
ISO/IEC 25010) y documenta **UN SOLO problema** por Issue.

| Selector | Opciones |
|---|---|
| **Tipo de hallazgo** (característica ISO 25010) | Rendimiento · Usabilidad · Compatibilidad · Funcionalidad |

**Directo al formulario** (evita el menú de selección):

<https://github.com/KrizRoMe/intro-si-iso25010-lab/issues/new?template=hallazgo.yml>

### Estructura del reporte

El formulario pide 16 campos, siempre en el mismo orden:

1. **Nombre completo** — tu identidad
2. **Sistema auditado** — ya viene con `ElectroHogar`
3. **Tipo de hallazgo** — selector: Rendimiento / Usabilidad / Compatibilidad / Funcionalidad
4. **Página** donde se observa el problema (selector)
5. **Aspecto que falla** — selector con el mecanismo general del fallo
6. **Elemento que falla** — el elemento concreto, no la página entera
7. **Cómo se manifiesta el fallo** — con tus propias palabras
8. **Cómo reproducirlo** — pasos numerados
9. **Evidencia** — qué mediste u observaste
10. **Capturas de pantalla** — adjunto de la evidencia
11. **Severidad** (selector) y **Usuario afectado** (selector)
12. **Solución propuesta** y **conclusión técnica**
13. **Verificación** — tres casillas de cierre

La primera línea del Issue (el título) lleva el prefijo `[Hallazgo]`.

---

## 🧪 Herramientas para la auditoría

No hace falta instalar nada: todo se hace en el navegador.

- **DevTools → Network** — ver el peso de cada imagen y si cargan todas al inicio
- **DevTools → Performance** — ver el tiempo de bloqueo del hilo principal
- **DevTools → Elements** — inspeccionar `min-width`, `type="text"`, `aria-label`
- **DevTools → Console** — ejecutar `window.EH_LEGACY.tiempoBloqueo` para medir el bloqueo
- **DevTools → Rendering → Contrast ratio** — comprobar los colores del texto
- **Redimensionar la ventana** a menos de 900 px — ver el desbordamiento horizontal

---

## 📁 Estructura del repositorio

```
.
├── index.html              # Inicio y catálogo
├── producto.html           # Detalle de producto
├── carrito.html            # Carrito de compras
├── checkout.html           # Finalizar compra
├── cuenta.html             # Iniciar sesión / crear cuenta
├── css/estilos.css         # Hoja de estilos (IIC: 065A82 / 1C7293 / 60A5FA)
├── js/
│   ├── datos.js            # Catálogo de productos
│   ├── app.js              # Lógica del sitio
│   ├── app-legacy.js       # Paquete heredado — bloqueante (defecto R02/R03)
│   └── analitica-pesada.js # Analítica de terceros — CPU síncrona (defecto R03)
├── assets/productos/       # 8 JPEG de ~2 MB sin optimizar (defecto R01)
├── docs/INSTRUCCIONES.md   # Guía paso a paso del alumno
├── scripts/                # Utilidades de verificación y generación
└── .github/ISSUE_TEMPLATE/ # El formulario único de reporte
```

---

## ✅ Verificación del laboratorio

### Defectos del sitio

El script `scripts/verificar-defectos.py` abre el sitio en un navegador real
(Chromium) y comprueba los 14 defectos con evidencia medida:

```bash
python3 -m http.server 8765 &
python3 scripts/verificar-defectos.py

# o contra el sitio ya publicado:
LAB_BASE="https://krizrome.github.io/intro-si-iso25010-lab" python3 scripts/verificar-defectos.py
```

```
R01    Rendimiento: imagenes sin lazy-loading          PASS  | imagenes=8 | con loading=lazy: 0 | ancho real px: 2600
R02    Rendimiento: script de terceros bloquea         PASS  | scripts sin defer/async: js/app-legacy.js
R03    Rendimiento: tarea de CPU sincrona              PASS  | bloqueo=27 ms | hashes=6000
U01    Usabilidad: filtro de precio invertido           PASS  | ninguno de los mostrados cae en el rango
U02    Usabilidad: busqueda sin aviso de vacio         PASS  | visibles=0 | mensaje ausente
U03    Usabilidad: contrasena en texto plano           PASS  | input[type]=text
C01    Compatibilidad: contraste insuficiente          PASS  | ratios: 1.98 / 1.98 / 1.84 (minimo AA = 4.5)
C02    Compatibilidad: ancho fijo sin responsive        PASS  | scrollWidth=1200px en pantalla de 390px
C03    Compatibilidad: tipografia sin fallback web      PASS  | hojas externas=0
F01    Funcionalidad: boton sin etiqueta accesible      PASS  | texto='×' aria-label=None tamano=16x16
F02    Funcionalidad: acepta tarjeta invalida           PASS  | tarjeta "123" -> pedido confirmado
F03    Funcionalidad: total no refleja la cantidad      PASS  | 2 unidades -> total sigue en S/ 149.00
TOTAL: 14 checks | PASS: 14 | FAIL: 0
```

### Issue Forms

```bash
python3 scripts/validar-issue-forms.py
```

```
OK  hallazgo-compatibilidad.yml    campos=16  ids=15
OK  hallazgo-funcionalidad.yml     campos=16  ids=15
OK  hallazgo-rendimiento.yml       campos=16  ids=15
OK  hallazgo-usabilidad.yml        campos=16  ids=15
OK: los 4 formularios pasan la validacion de esquema de GitHub
```

Las capturas de evidencia quedan en `scripts/capturas/`.

---

## 📚 Curso

**Introducción a los Sistemas de Información (INTRO SI) — Instituto Isabel La Católica**

Este laboratorio acompaña la sesión sobre el modelo de calidad **ISO/IEC 25010**
y su modelo de dos hemisferios (front-stage / back-stage).

---

## Licencia

Material educativo. Los problemas del sitio son intencionales y forman parte
del ejercicio de auditoría.
