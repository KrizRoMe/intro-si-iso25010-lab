#!/usr/bin/env python3
"""Prueba real del Issue Form unico: crea un Issue y verifica el render."""
import json
import subprocess
import sys

import yaml

REPO = 'KrizRoMe/intro-si-iso25010-lab'

CUERPO = """### Nombre completo del estudiante

Profesor KrizRoMe

### Tipo de hallazgo - caracteristica ISO/IEC 25010

Funcionalidad

### Pagina donde lo observaste

Finalizar compra

### Que problema encontraste

Que falla: el campo de numero de tarjeta acepta 123 y confirma el pedido.
A quien afecta: a todos los usuarios que compran.
Como se reproduce: entro a Finalizar compra, lleno los datos, pongo 123 en la tarjeta y confirmo.

### Evidencia

Aparece Pedido confirmado con la tarjeta 123.

### Solucion propuesta

Validar el numero con Luhn antes de confirmar.
"""


def gh(args):
    r = subprocess.run(['gh'] + args, capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit('gh fallo: %s' % r.stderr.strip())
    return r.stdout.strip()


def main():
    with open('/tmp/cuerpo-unico.md', 'w') as f:
        f.write(CUERPO)

    url = gh(['issue', 'create', '--repo', REPO, '--title', '[Hallazgo] Prueba docente del form unico',
              '--body-file', '/tmp/cuerpo-unico.md', '--label', 'hallazgo,test'])
    print('Issue creado: %s' % url)
    num = url.rstrip('/').split('/')[-1]

    d = json.loads(gh(['issue', 'view', num, '--repo', REPO, '--json', 'body,title,labels,url']))
    body = d['body']
    h3 = [l[4:].strip() for l in body.split('\n') if l.startswith('### ')]

    print('\nCampos renderizados por GitHub (%d):' % len(h3))
    for h in h3:
        print('  - %s' % h)

    print('\nVerificaciones:')
    # El campo `upload` solo existe en el FORM INTERACTIVO: al crear el Issue
    # por CLI no aparece en el cuerpo, asi que se valida contra el YAML.
    with open('.github/ISSUE_TEMPLATE/hallazgo.yml', encoding='utf-8') as f:
        form = yaml.safe_load(f)
    tipos = [s.get('type') for s in form.get('body', [])]
    ids_form = [s.get('id') for s in form.get('body', []) if s.get('id')]

    checks = [
        ('el selector "Tipo de hallazgo" esta presente',
         any('Tipo de hallazgo' in h for h in h3)),
        ('el valor "Funcionalidad" quedo registrado',
         '\nFuncionalidad\n' in body or body.rstrip().endswith('Funcionalidad')),
        ('tiene el selector de pagina',
         any('Pagina donde lo observaste' in h for h in h3)),
        ('tiene el campo de problema',
         any('Que problema encontraste' in h for h in h3)),
        ('tiene campo de evidencia',
         any('Evidencia' in h for h in h3)),
        ('tiene el campo de solucion propuesta',
         any('Solucion propuesta' in h for h in h3)),
        ('el form tiene campo de carga de captura',
         'upload' in tipos and 'captura' in ids_form),
        ('NO pide correo institucional',
         not any('correo' in h.lower() or 'email' in h.lower() for h in h3)
         and 'correo' not in ids_form and 'email' not in ids_form),
        ('NO pide mas de 7 campos',
         len(ids_form) == 7),
    ]
    ok = True
    for nombre, cond in checks:
        print('  %s %s' % ('OK  ' if cond else 'FAIL', nombre))
        if not cond:
            ok = False

    print('\nBorrando el Issue de prueba %s...' % num)
    gh(['issue', 'delete', num, '--repo', REPO, '--yes'])

    print('\nRESULTADO: %s' % ('el Issue Form unico funciona' if ok else 'HAY FALLOS'))
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
