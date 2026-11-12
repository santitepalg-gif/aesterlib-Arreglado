# Remap de astemirlib_re (Mojmap -> SRG) para Forge 1.20.1

1. Crea un repo en GitHub y sube todo esto.
2. Copia tu jar a `input/astemirlib.jar` (renombrado exactamente asi).
3. Ve a la pestaña **Actions** -> "Remap astemirlib_re" -> **Run workflow**.
4. Al terminar, descarga el artifact `astemirlib_re-REMAPPED` y ponlo en `mods` (quita el jar viejo).

Si al abrir Minecraft sale otro error `@Shadow ... was not located`, añade esa linea a `EXTRA` en `tools/fix_refmap.py` y vuelve a correr.
