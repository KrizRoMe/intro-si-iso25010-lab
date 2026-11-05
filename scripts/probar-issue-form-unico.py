#!/usr/bin/env python3
"""Prueba real del Issue Form unico: crea un Issue y verifica el render."""
import json
import subprocess
import sys

REPO = 'KrizRoMe/intro-si-iso25010-lab'

CUERPO = """### Nombre completo del estudiante

Profesor KrizRoMe

### Sistema auditado

ElectroHogar

### Tipo de hallazgo - caracteristica ISO/IEC 25010

Funcionalidad

### Pagina donde se observa el problema

Finalizar compra

### Aspecto que falla - elige una sola opcion

Falta informacion, aviso o confirmacion para el usuario

### Elemento que falla

El campo de numero de tarjeta

### Como se manifiesta el fallo

Pongo 123 y el sitio confirma el pedido igual.

### Como reproducirlo

1. Entrar a Finalizar compra
2. Llenar los datos
3. Poner 123 en la tarjeta
4. Confirmar

### Evidencia

Aparece Pedido confirmado con la tarjeta 123.

### Severidad

Alta - impide o hace muy costoso completar la compra

### Que usuario se ve afectado

Solo usuarios que compran o pagan

### Solucion propuesta

Validar el numero con Luhn antes de confirmar.

### Conclusion tecnica

El formulario acepta cualquier texto como tarjeta valida.
"""


def gh(args, inp=None):
    r = subprocess.run(['gh'] + args, capture_output=True, text=True, input=inp)
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
    # El campo `upload` y los `checkboxes` solo existen en el FORM INTERACTIVO.
    # Al crear el Issue por CLI no aparecen en el cuerpo (no hay archivo
    # adjunto ni casillas marcadas), asi que se validan contra el YAML.
    import yaml
    with open('.github/ISSUE_TEMPLATE/hallazgo.yml', encoding='utf-8') as f:
        form = yaml.safe_load(f)
    tipos = [s.get('type') for s in form.get('body', [])]
    ids_form = [s.get('id') for s in form.get('body', []) if s.get('id')]

    checks = [
        ('el selector "Tipo de hallazgo" esta presente',
         any('Tipo de hallazgo' in h for h in h3)),
        ('el valor "Funcionalidad" quedo registrado',
         '\nFuncionalidad\n' in body or body.rstrip().endswith('Funcionalidad')),
        ('NO pide correo institucional',
         not any('correo' in h.lower() or 'email' in h.lower() for h in h3)
         and 'correo' not in ids_form and 'email' not in ids_form),
        ('NO pide principio de usabilidad (se unifico en "Aspecto que falla")',
         not any('Principio' in h for h in h3)),
        ('tiene campo de evidencia',
         any('Evidencia' in h for h in h3)),
        ('el form tiene campo de carga de capturas',
         'upload' in tipos and 'captura' in ids_form),
        ('el form tiene las 3 casillas de verificacion',
         'checkboxes' in tipos and 'verificacion' in ids_form),
        ('tiene el selector de aspecto',
         any('Aspecto que falla' in h for h in h3)),
        ('tiene el selector de severidad',
         any(h == 'Severidad' for h in h3)),
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
