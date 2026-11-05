#!/usr/bin/env python3
"""
Verifica en un navegador real los 12 defectos front-stage del laboratorio
ElectroHogar (ISO/IEC 25010 - hemisferio front-stage).

Cada check imprime PASS/FAIL con la evidencia medida en el navegador.
"""
import json
import os
import sys
from playwright.sync_api import sync_playwright

BASE = 'http://127.0.0.1:8765'
RAIZ = os.path.dirname(os.path.abspath(__file__))
CAPTURAS = os.path.join(RAIZ, 'capturas')
os.makedirs(CAPTURAS, exist_ok=True)

resultados = []


def check(codigo, nombre, ok, detalle):
    resultados.append({'codigo': codigo, 'nombre': nombre, 'ok': bool(ok), 'detalle': detalle})
    print('%-6s %-56s %s  | %s' % (codigo, nombre[:56], 'PASS' if ok else 'FAIL', detalle))


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        ctx = browser.new_context(viewport={'width': 1440, 'height': 900})
        page = ctx.new_page()

        # ================= RENDIMIENTO (3) =================
        page.goto(BASE + '/index.html', wait_until='load')
        page.wait_for_timeout(1500)

        # R01 - imagenes sin lazy-loading + peso excesivo
        r01 = page.evaluate("""() => {
            const imgs = Array.from(document.images);
            return { total: imgs.length,
                     conLazy: imgs.filter(i => i.getAttribute('loading') === 'lazy').length,
                     natural: imgs.map(i => i.naturalWidth).filter(w => w > 0).slice(0,3) };
        }""")
        check('R01', 'Rendimiento: imagenes sin lazy-loading y sobredimensionadas',
              r01['conLazy'] == 0 and r01['total'] >= 8 and max(r01['natural'] or [0]) >= 2000,
              'imagenes=%d | con loading=lazy: %d | ancho real px: %s' % (
                  r01['total'], r01['conLazy'], r01['natural']))

        # R02 - scripts de terceros bloqueantes en <head>
        r02 = page.evaluate("""() => Array.from(document.head.querySelectorAll('script[src]'))
            .map(s => ({ src: s.getAttribute('src'), defer: s.hasAttribute('defer'),
                         async: s.hasAttribute('async') }))""")
        sin = [b for b in r02 if not b['defer'] and not b['async']]
        check('R02', 'Rendimiento: script de terceros bloquea el primer pintado',
              len(sin) >= 1,
              'scripts sin defer/async en <head>: %s' % ', '.join(b['src'] for b in sin))

        # R03 - trabajo de CPU sincrono en cada carga
        r03 = page.evaluate("""() => {
            const hub = window.analyticsHub || {};
            const leg = window.EH_LEGACY || {};
            return { bloqueo: leg.tiempoBloqueo,
                     campanas: hub.indiceCampanas ? hub.indiceCampanas.length : 0,
                     hashes: leg.indiceHashes ? Object.keys(leg.indiceHashes).length : 0 };
        }""")
        check('R03', 'Rendimiento: tarea de CPU sincrona bloquea el hilo principal',
              (r03['bloqueo'] is not None and r03['bloqueo'] >= 30)
              and r03['hashes'] >= 5000,
              'bloqueo medido=%s ms | hashes precalculados=%d | campanas en RAM=%d' % (
                  r03['bloqueo'], r03['hashes'], r03['campanas']))

        # ================= USABILIDAD (4) =================
        # U01 - filtro de precio con logica invertida
        page.fill('#precio-desde', '500')
        page.fill('#precio-hasta', '2000')
        page.wait_for_timeout(500)
        u01 = page.evaluate("""() => {
            const precios = Array.from(document.querySelectorAll('.precio'))
                .map(e => parseFloat(e.textContent.replace(/[^0-9.]/g,'')))
                .filter(n => !isNaN(n));
            return { precios: precios, total: document.querySelectorAll('.tarjeta').length };
        }""")
        dentro = [x for x in u01['precios'] if 500 <= x <= 2000]
        check('U01', 'Usabilidad: el filtro de precio esta invertido',
              len(dentro) == 0 and u01['total'] > 0,
              'rango pedido 500-2000 -> mostrados=%d | precios mostrados=%s | ninguno cae en el rango' % (
                  u01['total'], u01['precios']))

        # U02 - busqueda sin resultados no informa
        page.fill('#precio-desde', '')
        page.fill('#precio-hasta', '')
        page.wait_for_timeout(400)
        page.fill('#q-busqueda', 'producto-inexistente-xyz')
        page.wait_for_timeout(600)
        u02 = page.evaluate("""() => {
            const visibles = Array.from(document.querySelectorAll('.tarjeta'))
                .filter(t => t.style.display !== 'none').length;
            const msg = document.body.innerText.match(/No se encontraron[\\s\\S]{0,80}/);
            return { visibles: visibles, mensaje: msg ? msg[0] : null };
        }""")
        check('U02', 'Usabilidad: la busqueda no avisa cuando no hay resultados',
              u02['visibles'] == 0 and not u02['mensaje'],
              'visibles=%d | mensaje de "sin resultados" presente: %s' % (
                  u02['visibles'], bool(u02['mensaje'])))

        # U03 - el campo de contrasena no oculta los caracteres
        page.goto(BASE + '/cuenta.html', wait_until='load')
        page.wait_for_timeout(700)
        u03 = page.evaluate("""() => {
            const p = document.getElementById('login-password');
            const r = document.getElementById('reg-password');
            return { login: p ? p.getAttribute('type') : null, registro: r ? r.getAttribute('type') : null };
        }""")
        check('U03', 'Usabilidad: la contrasena se muestra en texto plano',
              u03['login'] == 'text' and u03['registro'] == 'text',
              'input[type] login=%r registro=%r (deberia ser "password")' % (u03['login'], u03['registro']))

        # U04 - sin confirmacion al quitar  [variante adicional, no cuenta como 1 de los 12]
        page.evaluate("() => localStorage.setItem('eh_carrito_v1', JSON.stringify([{id:1,nombre:'Audifonos Bluetooth SoulBeat X2',marca:'SoulBeat',precio:149,imagen:'assets/productos/audifonos.jpg',cantidad:1}]))")
        page.goto(BASE + '/carrito.html', wait_until='load')
        page.wait_for_timeout(800)
        u04 = page.evaluate("""() => {
            const toast = document.querySelector('[role=alert], .toast, .notificacion, .snackbar');
            const dlg = document.querySelector('[role=dialog], .modal, .confirmacion');
            return { toast: !!toast, dialogo: !!dlg };
        }""")
        check('U04*', '[variante] quitar un articulo no da confirmacion ni aviso',
              not u04['toast'] and not u04['dialogo'],
              'toast=%s dialogo=%s (la fila desaparece en silencio)' % (u04['toast'], u04['dialogo']))

        # ================= COMPATIBILIDAD (3) =================
        # C01 - contraste insuficiente
        page.goto(BASE + '/index.html', wait_until='load')
        page.wait_for_timeout(900)
        c01 = page.evaluate("""() => {
            function lum(rgb){ const c=rgb.map(v=>{v/=255;return v<=0.03928?v/12.92:Math.pow((v+0.055)/1.055,2.4);});
                               return 0.2126*c[0]+0.7152*c[1]+0.0722*c[2]; }
            function parse(s){ const m=s.match(/rgba?\\(([^)]+)\\)/); if(!m) return null;
                               const p=m[1].split(',').map(x=>parseFloat(x)); return p.slice(0,3); }
            function bgOf(el){ let n=el;
              while(n && n!==document.documentElement){ const cs=getComputedStyle(n);
                const a=cs.backgroundColor.match(/rgba?\\([^)]*,\\s*([\\d.]+)\\)/);
                if(cs.backgroundColor!=='rgba(0, 0, 0, 0)' && (!a||parseFloat(a[1])>0.9)) return parse(cs.backgroundColor);
                n=n.parentElement; } return [255,255,255]; }
            function ratio(el){ const fg=parse(getComputedStyle(el).color); if(!fg) return null;
              const l1=lum(fg), l2=lum(bgOf(el)); return (Math.max(l1,l2)+0.05)/(Math.min(l1,l2)+0.05); }
            const out={};
            ['.tarjeta-marca','.precio-antes','.ayuda'].forEach(s=>{ const el=document.querySelector(s);
              if(el) out[s]=Math.round(ratio(el)*100)/100; });
            return out;
        }""")
        bajos = {k: v for k, v in c01.items() if v < 4.5}
        check('C01', 'Compatibilidad: contraste insuficiente en texto secundario',
              len(bajos) >= 2,
              'ratios de contraste (minimo WCAG AA = 4.5:1) -> %s' % json.dumps(c01))

        # C02 - no hay diseño responsive
        ancho = page.evaluate("() => getComputedStyle(document.body).minWidth")
        page.set_viewport_size({'width': 390, 'height': 780})
        page.wait_for_timeout(500)
        sw = page.evaluate("() => document.documentElement.scrollWidth")
        check('C02', 'Compatibilidad: ancho fijo, no se adapta a pantallas pequenas',
              ancho == '1200px' and sw >= 1200,
              'body{min-width:%s} | scrollWidth en pantalla de 390px = %dpx (desbordamiento)' % (ancho, sw))

        # C03 - tipografia sin fallback web
        c03 = page.evaluate("""() => {
            const b = getComputedStyle(document.body);
            return { fuentes: b.fontFamily,
                     externas: document.querySelectorAll('link[rel=stylesheet][href^=http]').length,
                     preconnect: document.querySelectorAll('link[rel=preconnect]').length };
        }""")
        check('C03', 'Compatibilidad: tipografia del sistema, sin fallback web',
              c03['externas'] == 0 and c03['preconnect'] == 0,
              'font-family=%s | hojas externas=%d | preconnect=%d' % (
                  c03['fuentes'][:55], c03['externas'], c03['preconnect']))

        # ================= FUNCIONALIDAD (2) =================
        # F01 - boton de quitar sin nombre accesible
        page.set_viewport_size({'width': 1440, 'height': 900})
        page.goto(BASE + '/carrito.html', wait_until='load')
        page.wait_for_timeout(900)
        f01 = page.evaluate("""() => {
            const b = document.querySelector('.btn-quitar');
            if (!b) return null;
            const r = b.getBoundingClientRect();
            return { texto: b.textContent.trim(), aria: b.getAttribute('aria-label'),
                     title: b.getAttribute('title'), w: Math.round(r.width), h: Math.round(r.height) };
        }""")
        check('F01', 'Funcionalidad: boton de quitar sin etiqueta accesible',
              f01 and not f01['aria'] and not f01['title'] and f01['texto'] == '×' and f01['w'] < 24,
              'quitar -> texto=%r aria-label=%s title=%s tamano=%sx%s px' % (
                  f01['texto'], f01['aria'], f01['title'], f01['w'], f01['h']))

        # F02 - acepta numero de tarjeta invalido
        page.goto(BASE + '/checkout.html', wait_until='load')
        page.wait_for_timeout(900)
        page.fill('#nombre', 'Juan Perez')
        page.fill('#email', 'juan@mail.com')
        page.select_option('#metodo-pago', 'tarjeta')
        page.select_option('#ciudad', 'lima')
        page.select_option('#envio', 'estandar')
        page.fill('#direccion', 'Av. Siempre Viva 742')
        page.fill('#numero-tarjeta', '123')
        page.fill('#titular-tarjeta', 'JUAN PEREZ')
        page.fill('#fecha-vencimiento', '01/20')
        page.fill('#cvv', '1')
        page.click('button[type=submit]')
        page.wait_for_timeout(700)
        f02 = page.evaluate("""() => {
            const ok = document.getElementById('aviso-ok');
            const form = document.getElementById('form-panel');
            return { visible: ok && getComputedStyle(ok).display !== 'none',
                     texto: ok ? ok.textContent.trim() : '',
                     formOculto: form && getComputedStyle(form).display === 'none' };
        }""")
        check('F02', 'Funcionalidad: acepta una tarjeta invalida (123) y confirma el pedido',
              f02['visible'],
              'tarjeta "123" + CVV "1" -> %s | pedido confirmado: %s' % (
                  'formulario oculto' if f02['formOculto'] else 'formulario visible', f02['texto'][:60]))

        # F03 - el total del carrito no refleja la cantidad
        page.goto(BASE + '/carrito.html', wait_until='load')
        page.wait_for_timeout(900)
        page.click('button[data-delta="1"]')
        page.wait_for_timeout(600)
        f03 = page.evaluate("""() => {
            const t = document.getElementById('total-general');
            const a = document.getElementById('num-articulos');
            return { total: t ? t.textContent.trim() : null, articulos: a ? a.textContent.trim() : null };
        }""")
        check('F03', 'Funcionalidad: el total no se actualiza al cambiar la cantidad',
              f03['total'] == 'S/ 149.00' and f03['articulos'] == '2',
              'tras pulsar "+" (2 unidades de S/ 149.00) -> articulos=%s total=%s (deberia ser S/ 298.00)' % (
                  f03['articulos'], f03['total']))

        # F04* - el mensaje de error no senala que campo falla  [variante adicional]
        page.goto(BASE + '/checkout.html', wait_until='load')
        page.wait_for_timeout(900)
        page.click('button[type=submit]')
        page.wait_for_timeout(500)
        f04 = page.evaluate("""() => {
            const a = document.getElementById('aviso-form');
            const nombre = document.getElementById('nombre');
            const email = document.getElementById('email');
            const ciudad = document.getElementById('ciudad');
            function marcado(el){ const cs=getComputedStyle(el);
              return cs.borderColor + '|' + cs.outlineStyle + '|' + cs.outlineWidth; }
            return { visible: a && getComputedStyle(a).display !== 'none',
                     texto: a ? a.textContent.trim() : '',
                     estiloNombre: marcado(nombre),
                     estiloCiudad: marcado(ciudad),
                     foco: document.activeElement ? document.activeElement.id : null,
                     conAriaInvalid: document.querySelectorAll('[aria-invalid=true]').length };
        }""")
        check('F04*', '[variante] el error del formulario no marca que campo fallo',
              f04['visible'] and 'Revisa el formulario' in f04['texto']
              and f04['conAriaInvalid'] == 0 and f04['foco'] in (None, ''),
              'mensaje=%r | aria-invalid en campos=%d | campo enfocado=%s | borde nombre=%s' % (
                  f04['texto'], f04['conAriaInvalid'], f04['foco'], f04['estiloNombre']))

        # ================= EVIDENCIA / CAPTURAS =================
        page.goto(BASE + '/index.html', wait_until='load')
        page.wait_for_timeout(1600)
        page.screenshot(path=os.path.join(CAPTURAS, '01-catalogo.png'))
        page.goto(BASE + '/carrito.html', wait_until='load')
        page.wait_for_timeout(900)
        page.screenshot(path=os.path.join(CAPTURAS, '02-carrito.png'))
        page.goto(BASE + '/checkout.html', wait_until='load')
        page.wait_for_timeout(900)
        page.screenshot(path=os.path.join(CAPTURAS, '03-checkout.png'))
        page.goto(BASE + '/cuenta.html', wait_until='load')
        page.wait_for_timeout(800)
        page.screenshot(path=os.path.join(CAPTURAS, '04-cuenta.png'))

        browser.close()

    fallaron = [r for r in resultados if not r['ok']]
    print('\n' + '=' * 96)
    print('TOTAL: %d checks | PASS: %d | FAIL: %d' % (
        len(resultados), len(resultados) - len(fallaron), len(fallaron)))
    if fallaron:
        print('\nFALLARON:')
        for r in fallaron:
            print('  - %s %s :: %s' % (r['codigo'], r['nombre'], r['detalle']))
    print('=' * 96)
    with open(os.path.join(RAIZ, 'capturas', 'resultados-verificacion.json'), 'w') as f:
        json.dump(resultados, f, indent=2, ensure_ascii=False)
    return 1 if fallaron else 0


if __name__ == '__main__':
    sys.exit(main())
