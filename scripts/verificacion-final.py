#!/usr/bin/env python3
"""Verificacion final del entregable completo."""
import json
import subprocess
import urllib.request

PUB = 'KrizRoMe/intro-si-iso25010-lab'
PRIV = 'KrizRoMe/intro-si-iso25010-lab-docente'
SITIO = 'https://krizrome.github.io/intro-si-iso25010-lab/'

ok = True


def chk(nombre, cond, detalle):
    global ok
    if not cond:
        ok = False
    print('  %s %-46s %s' % ('OK  ' if cond else 'FAIL', nombre, detalle))


def gh(args):
    r = subprocess.run(['gh'] + args, capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else ''


def http(url):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'check'})
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, r.read()
    except Exception as e:
        return getattr(e, 'code', 0), b''


print('=' * 78)
print('VERIFICACION FINAL DEL ENTREGABLE')
print('=' * 78)

print('\n[1] REPOSITORIOS')
d = json.loads(gh(['repo', 'view', PUB, '--json', 'name,visibility,url,defaultBranchRef']))
chk('repo publico', d['visibility'] == 'PUBLIC', '%s -> %s' % (d['name'], d['url']))
chk('rama por defecto main', d['defaultBranchRef']['name'] == 'main', d['defaultBranchRef']['name'])
d2 = json.loads(gh(['repo', 'view', PRIV, '--json', 'name,visibility,url']))
chk('repo docente privado', d2['visibility'] == 'PRIVATE', '%s -> %s' % (d2['name'], d2['url']))

print('\n[2] SITIO PUBLICADO')
for ruta in ['', 'index.html', 'producto.html?id=3', 'carrito.html', 'checkout.html', 'cuenta.html',
             'css/estilos.css', 'js/app.js', 'js/app-legacy.js', 'js/analitica-pesada.js',
             'assets/productos/laptop.jpg', 'README.md', 'docs/INSTRUCCIONES.md']:
    code, _ = http(SITIO + ruta)
    chk('ruta %s' % (ruta or '/'), code == 200, 'HTTP %s' % code)

print('\n[3] ISSUE FORMS (debe existir SOLO uno)')
templates = gh(['api', 'repos/%s/contents/.github/ISSUE_TEMPLATE' % PUB, '--jq', '.[].name'])
nombres = [t for t in templates.split() if t.endswith('.yml')]
forms = [t for t in nombres if t != 'config.yml']
chk('exactamente 1 formulario', len(forms) == 1, 'formularios: %s' % (forms or 'ninguno'))
chk('se llama hallazgo.yml', 'hallazgo.yml' in forms, str(forms))
chk('config.yml presente', 'config.yml' in nombres, str(nombres))

print('\n[4] CONFIG.YML (sin enlace de reportes de companeros)')
cfg = gh(['api', 'repos/%s/contents/.github/ISSUE_TEMPLATE/config.yml' % PUB, '--jq', '.content'])
import base64
cfg_txt = base64.b64decode(cfg).decode('utf-8') if cfg else ''
chk('fuerza el formulario (blank_issues_enabled: false)',
    'blank_issues_enabled: false' in cfg_txt, 'ok')
chk('NO tiene enlace a issues de companeros',
    '/issues?q=' not in cfg_txt and 'companeros' not in cfg_txt.lower(), 'sin contact_link a issues')
chk('SI tiene el enlace al sitio del lab',
    'krizrome.github.io/intro-si-iso25010-lab' in cfg_txt, 'contact_link al sitio')

print('\n[5] ETIQUETAS')
labels = gh(['label', 'list', '--repo', PUB, '--limit', '30', '--json', 'name', '--jq', '.[].name'])
chk('etiqueta hallazgo existe', 'hallazgo' in labels, 'quedan: %s' % ' '.join(labels.split()))
obsoletas = [l for l in ['rendimiento', 'usabilidad', 'compatibilidad', 'funcionalidad'] if l in labels]
chk('etiquetas por caracteristica eliminadas', not obsoletas, str(obsoletas))

print('\n[6] SEPARACION PUBLICO / PRIVADO')
pub_files = gh(['api', 'repos/%s/contents/' % PUB, '--jq', '.[].name'])
fuga = [w for w in ['docente', 'RUBRICA', 'RESPUESTAS', 'PROMPT'] if w in pub_files]
chk('sin material docente en el publico', not fuga, ' '.join(pub_files.split()))
priv_files = gh(['api', 'repos/%s/contents/' % PRIV, '--jq', '.[].name'])
for f in ['RESPUESTAS_ESPERADAS.md', 'RUBRICA.md', 'PROMPT_CORRECCION_IA.md', 'calificar.py']:
    chk('docente/%s' % f, f in priv_files, 'presente en el repo privado')

print('\n[7] PAGES')
p = json.loads(gh(['api', 'repos/%s/pages' % PUB]))
chk('pages url', p['html_url'].rstrip('/') == SITIO.rstrip('/'), p['html_url'])
chk('pages source = main', p['source']['branch'] == 'main', str(p['source']))
runs = gh(['run', 'list', '--repo', PUB, '--limit', '3'])
chk('ultimo build pages success', 'success' in runs.split('\n')[0], runs.split('\n')[0][:80])

print('\n' + '=' * 78)
print('RESULTADO FINAL: %s' % ('TODO VERIFICADO' if ok else 'HAY FALLOS'))
print('=' * 78)
