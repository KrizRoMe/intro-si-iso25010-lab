#!/usr/bin/env python3
"""Verifica que los 4 Issue Forms se rendericen correctamente en GitHub."""
import json
import subprocess

REPO = 'KrizRoMe/intro-si-iso25010-lab'
ESPERADOS = {
    1: ('rendimiento', 'Pagina donde se observa el problema'),
    2: ('usabilidad', 'Principio de usabilidad relacionado'),
    3: ('compatibilidad', 'Entorno donde lo observaste'),
    4: ('funcionalidad', 'Que usuario se ve afectado'),
}

print('Verificando renderizado de los 4 Issue Forms en GitHub\n')
ok = True
for num, (caract, campo_esperado) in ESPERADOS.items():
    r = subprocess.run(['gh', 'issue', 'view', str(num), '--repo', REPO, '--json',
                        'body,title,labels,url'],
                       capture_output=True, text=True)
    if r.returncode != 0:
        print('  ERROR  Issue #%d no se pudo leer: %s' % (num, r.stderr.strip()))
        ok = False
        continue
    d = json.loads(r.stdout)
    body = d['body']
    titulo = d['title']
    labels = [l['name'] for l in d['labels']]

    h3 = [l[4:].strip() for l in body.split('\n') if l.startswith('### ')]
    tiene_campo = campo_esperado in h3
    # El label de la caracteristica lo aplica el propio formulario al crear
    # el Issue; aqui verificamos que la caracteristica este entre las
    # etiquetas del Issue creado.
    tiene_label = caract in labels

    estado = 'OK ' if (tiene_campo and tiene_label) else 'FAIL'
    if not (tiene_campo and tiene_label):
        ok = False
    print('  %s Issue #%d  labels=%s' % (estado, num, labels))
    print('        titulo: %s' % titulo)
    print('        campos h3 renderizados: %d' % len(h3))
    print('        campo clave "%s" presente: %s' % (campo_esperado, tiene_campo))
    print('        campos: %s' % ', '.join(h.replace('### ', '') for h in h3[:8]))
    print('        ...')
    print()

print('=' * 70)
print('RESULTADO: %s' % ('los 4 Issue Forms renderizan correctamente' if ok else 'HAY FALLOS'))
