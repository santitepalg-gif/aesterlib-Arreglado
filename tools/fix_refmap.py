#!/usr/bin/env python3
"""Despues del remapeo: añade al refmap los @Shadow que el autor no registro (p. ej. GuiGraphics.flush).
Si en el siguiente log sale otro "@Shadow ... was not located", agregalo a EXTRA y vuelve a correr el workflow."""
import glob, json, re, shutil, sys, zipfile

JAR = sys.argv[1]
MIXIN_PKG = 'com/astemir/astemirlib/re/client/mixin/'

# (clase mixin, nombre del shadow, clase objetivo de Minecraft, nombre mojmap, descriptor)
EXTRA = [
    (MIXIN_PKG + 'render/MixinGuiGraphics', 'flush',
     'net/minecraft/client/gui/GuiGraphics', 'flush', '()V'),
]

def load_tsrg():
    files = glob.glob('build/**/*.tsrg', recursive=True)
    best = {}
    for f in files:
        cls = None
        for line in open(f, encoding='utf8', errors='ignore'):
            if not line.startswith('\t') and not line.startswith(' '):
                p = line.split()
                cls = p[0] if p else None
                continue
            p = line.split()
            if cls is None or not p:
                continue
            if len(p) == 3 and p[1].startswith('('):      # metodo: nombre desc srg
                best[(cls, p[0], p[1])] = p[2]
            elif len(p) == 2:                              # campo: nombre srg
                best[(cls, p[0], None)] = p[1]
    return best

def main():
    tsrg = load_tsrg()
    if not tsrg:
        print('AVISO: no encontre archivos .tsrg en build/, no se parcheo el refmap'); return
    refmap_name = 'astemirlib_re.refmap.json'
    zin = zipfile.ZipFile(JAR)
    refmap = json.loads(zin.read(refmap_name))
    changed = False
    for mixin, shadow, target, mojname, desc in EXTRA:
        srg = tsrg.get((target, mojname, desc))
        if not srg:
            print(f'AVISO: no encontre {target}.{mojname}{desc} en los mapeos'); continue
        value = f'L{target};{srg}{desc}'
        for section in (refmap.get('mappings', {}), *[v for v in refmap.get('data', {}).values()]):
            if isinstance(section, dict) and 'mappings' in section: section = section['mappings']
            if isinstance(section, dict):
                section.setdefault(mixin, {})[shadow] = value
        print('refmap:', mixin.split('/')[-1], shadow, '->', value); changed = True
    if not changed: return
    tmp = JAR + '.tmp'
    with zipfile.ZipFile(tmp, 'w', zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = json.dumps(refmap, indent=2).encode() if item.filename == refmap_name else zin.read(item.filename)
            zout.writestr(item, data)
    zin.close(); shutil.move(tmp, JAR)

main()
