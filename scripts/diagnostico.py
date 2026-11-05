#!/usr/bin/env python3
"""Diagnostico: errores de consola y estado real de los scripts en la pagina."""
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    b = p.chromium.launch()
    page = b.new_context(viewport={'width': 1440, 'height': 900}).new_page()
    errores = []
    page.on('console', lambda m: errores.append(('CONSOLE:' + m.type, m.text)))
    page.on('pageerror', lambda e: errores.append(('PAGEERROR', str(e))))
    page.goto('http://127.0.0.1:8765/index.html', wait_until='load')
    page.wait_for_timeout(2000)

    print('--- errores de consola ---')
    for t, txt in errores:
        print(' ', t, '|', txt[:200])
    if not errores:
        print('  (ninguno)')

    print('\n--- estado de scripts ---')
    est = page.evaluate("""() => ({
        analyticsHub: typeof window.analyticsHub,
        clavesHub: window.analyticsHub ? Object.keys(window.analyticsHub).slice(0,30) : null,
        tiempoBloqueo: window.analyticsHub ? window.analyticsHub.tiempoBloqueo : 'sin hub',
        campanas: window.analyticsHub && window.analyticsHub.indiceCampanas
                  ? window.analyticsHub.indiceCampanas.length : 0,
        EH_LEGACY: typeof window.EH_LEGACY,
        duracionLegacy: window.EH_LEGACY ? window.EH_LEGACY.duracion : null
    })""")
    for k, v in est.items():
        print('  %-16s %s' % (k, v))

    print('\n--- scripts en el DOM ---')
    for s in page.evaluate("""() => Array.from(document.scripts).map(s => ({
        src: s.src.split('/').pop(), defer: s.defer, async: s.async,
        bloqueante: !s.defer && !s.async && !s.type.includes('module')
    }))"""):
        print(' ', s)

    b.close()
