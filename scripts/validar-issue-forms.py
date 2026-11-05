#!/usr/bin/env python3
"""
Validador estructural de los Issue Forms (YAML) de GitHub.

Comprueba lo que GitHub realmente rechaza:
  - options DEBEN estar dentro de attributes
  - cada option de dropdown/checkbox DEBE ser string (un ':' sin comillas
    lo convierte en dict y GitHub lo rechaza)
  - label obligatorio en input/textarea/dropdown/checkboxes/upload
  - value obligatorio en markdown
  - ids unicos y snake_case
  - checkboxes NO deben llevar validations.required (GitHub lo ignora)
  - sin alias YAML (*id001) y sin **bold** al inicio de linea

Salida: exit code 0 = OK, 1 = hay errores.
"""
import glob
import os
import re
import sys

import yaml

RAIZ = os.path.dirname(os.path.abspath(__file__))
PATRON = os.path.join(RAIZ, '..', '.github', 'ISSUE_TEMPLATE', 'hallazgo-*.yml')


def main():
    rutas = sorted(glob.glob(PATRON))
    if not rutas:
        print('No se encontraron formularios en %s' % PATRON)
        return 1

    errores = []
    print('Validando %d Issue Forms\n' % len(rutas))

    for ruta in rutas:
        nombre = os.path.basename(ruta)
        crudo = open(ruta, encoding='utf-8').read()
        try:
            t = yaml.safe_load(crudo)
        except Exception as e:
            errores.append('%s: YAML no parsea -> %s' % (nombre, e))
            continue

        # --- alias YAML (GitHub usa Psych estricto: aliases deshabilitados) ---
        if re.search(r'^\s*-\s+\*\w+', crudo, re.M) or re.search(r':\s+\*\w+$', crudo, re.M):
            errores.append('%s: contiene alias YAML (*id001)' % nombre)
        # --- **bold** al inicio de linea dentro de un block scalar ---
        for i, linea in enumerate(crudo.split('\n'), 1):
            if re.match(r'^\s*\*\w', linea):
                errores.append('%s linea %d: "*" al inicio de linea (riesgo de alias)' % (nombre, i))
            s = linea.strip()
            if s.startswith('&') or s.startswith('!') or s.startswith('@'):
                errores.append('%s linea %d: caracter especial "%s" al inicio de linea' % (nombre, i, s[0]))

        # --- estructura ---
        ids = []
        total_campos = 0
        for i, s in enumerate(t.get('body', [])):
            total_campos += 1
            tipo = s.get('type')
            sid = s.get('id')
            a = s.get('attributes', {}) or {}
            if sid:
                ids.append(sid)
                if not re.fullmatch(r'[a-z0-9_]+', sid):
                    errores.append('%s body[%d]: id "%s" no es snake_case' % (nombre, i, sid))

            if tipo in ('dropdown', 'checkboxes'):
                if 'options' not in a:
                    errores.append('%s body[%d] (%s): "options" debe estar DENTRO de attributes' % (nombre, i, sid))
                    continue
                for j, o in enumerate(a['options']):
                    if tipo == 'dropdown':
                        # En dropdown cada option DEBE ser un string plano.
                        if not isinstance(o, str):
                            errores.append('%s body[%d] (%s): option %d es %s, no string -> '
                                           'GitHub lo rechaza (un ":" sin comillas lo vuelve dict)'
                                           % (nombre, i, sid, j, type(o).__name__))
                    else:
                        # En checkboxes cada option DEBE ser {label, required}.
                        if isinstance(o, str):
                            errores.append('%s body[%d] (%s): option %d es string; en checkboxes '
                                           'debe ser {label: ..., required: ...}' % (nombre, i, sid, j))
                        elif not isinstance(o, dict):
                            errores.append('%s body[%d] (%s): option %d es %s, no dict'
                                           % (nombre, i, sid, j, type(o).__name__))
                        else:
                            if 'label' not in o:
                                errores.append('%s body[%d] (%s): option %d sin "label"'
                                               % (nombre, i, sid, j))
                            if 'required' not in o:
                                errores.append('%s body[%d] (%s): option %d sin "required"'
                                               % (nombre, i, sid, j))
            if tipo in ('input', 'textarea', 'dropdown', 'checkboxes', 'upload') and 'label' not in a:
                errores.append('%s body[%d] (%s): falta "label"' % (nombre, i, sid))
            if tipo == 'markdown' and 'value' not in a:
                errores.append('%s body[%d] (%s): falta "value"' % (nombre, i, sid))
            if tipo == 'checkboxes' and (s.get('validations') or {}).get('required'):
                errores.append('%s body[%d] (%s): checkboxes con validations.required '
                               '(GitHub lo ignora en silencio)' % (nombre, i, sid))
            if tipo == 'dropdown' and len(a.get('options', [])) > 8:
                errores.append('%s body[%d] (%s): %d opciones (>8 se vuelve ruido para el alumno)'
                               % (nombre, i, sid, len(a['options'])))

        if len(ids) != len(set(ids)):
            errores.append('%s: ids duplicados' % nombre)

        for clave in ('name', 'description'):
            if not t.get(clave):
                errores.append('%s: falta "%s" en la cabecera' % (nombre, clave))
        if not t.get('title'):
            errores.append('%s: falta "title"' % nombre)
        elif not t['title'].startswith('['):
            errores.append('%s: el title no lleva el prefijo [Caracteristica]' % nombre)
        if not t.get('labels'):
            errores.append('%s: sin labels (se usara el default "hallazgo")' % nombre)

        print('  OK  %-38s campos=%d  ids=%d' % (nombre, total_campos, len(ids)))

    print('\n' + '=' * 70)
    if errores:
        print('ERRORES (%d):' % len(errores))
        for e in errores:
            print('  - %s' % e)
        return 1
    print('OK: los %d formularios pasan la validacion de esquema de GitHub' % len(rutas))
    return 0


if __name__ == '__main__':
    sys.exit(main())
