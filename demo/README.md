# Demo: G-Blog, blog editorial

Maquetas HTML estáticas con los elementos del brand-book GeoZ.

| Página | Propósito |
|---|---|
| `index.html` | Portada (landing): titular G-Blog, ícono destacado, accesos rápidos, G-Academy, recientes y series |
| `presentacion.html` | Página propia sobre el autor |
| `archivo.html` | Todas las entradas, con filtro por parte de la serie |
| `serie-ss-courses.html` | Página de la serie SS-Courses: carta de bienvenida y ruta de lectura |
| `ss-0-…` a `ss-2-2-…` | Los 5 artículos de la serie, generados desde `docs/*.md` |
| `admoniciones.html` | Catálogo de los 12 tipos de admonición de Zensical con íconos del brand-book |

## Serie Self Swirl-Courses (SS-Courses)

0. ¿Qué es Swirlify? (introducción)
1. P1 · Los cimientos cognitivos: 1.1 ¿Quiénes son tus aprendices? · 1.2 La mente del aprendiz
2. P2 · El laboratorio técnico: 2.1 Tuerca, tornillo y archivo · 2.2 Chasis de un curso: GEOCHIP-R

- Logo: `geoz-principal.svg` en tema claro y `geoz-principal-oscuro.svg` en tema oscuro.
- Fuentes: Archivo Black (titulares), IBM Plex Mono (etiquetas y navegación), IBM Plex Serif (texto largo), Nothing You Could Do (solo la firma).
- Estilos: `assets/css/demo.css`. Claro/oscuro con el botón ◐.

## Lecturas y artículo más leído (GoatCounter)

Cada página envía su visita a GoatCounter. Los artículos usan un identificador fijo (`/ss-intro`, `/ss-1-1` … `/ss-2-3`), así el conteo no se pierde si cambia la dirección o el título.

1. Crea la cuenta en GoatCounter, cambia `TU-CODIGO` en las páginas por tu código y activa en Settings la opción para mostrar los conteos en tu sitio.
2. Antes de publicar, corre:

   ```sh
   python3 demo/scripts/actualizar_lecturas.py --codigo TU-CODIGO
   ```

   Escribe "N lecturas" en cada artículo, el total de la serie y pone el más leído en el destacado de la portada (con `--minimo` visitas; 10 por defecto). Para probar sin internet: `--desde demo/data/conteos-ejemplo.json`.
3. Para que el destacado cambie también de ícono, agrega el SVG del artículo en `demo/iconos/<id>.svg.html` (hoy solo existe `ss-1-1`).
