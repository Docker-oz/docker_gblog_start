# 1.2 La mente del aprendiz 🧠
______
Ha llegado el momento de hablar sobre los **modelos mentales** y su importancia. Quizás esta sea la parte que más me interesa dejar clara, ya que mucho de lo que compartiré en ***Swirlify*** tiene sus bases en todo esto.

!!! nota
    _Antes de diseñar clases o cursos, debemos tener muy en cuenta la manera en que construimos nuestro aprendizaje. No obstante, quiero hacer una aclaración: por ningún motivo pretendo decir que lo compartido en estas líneas sea la única forma de poder dar buenas clases o cursos, ni mucho menos la panacea para los modelos instruccionales de cursos. Es, simplemente, un punto de vista muy particular basado en lo que me ha dado resultado en el contenido de mis capacitaciones._

**_-"¿Qué es un modelo mental?"-_**... De acuerdo con Wilson (2019) es una representación simplificada del dominio de un problema que permite razonar y resolver situaciones, aunque no sea técnicamente perfecta (como imaginar átomos como bolas y resortes). Dicho de otra manera, es un truco que usa tu cerebro para entender algo muy complejo sin tener que saber cada detalle técnico. **¡NO!** es una copia fotográfica de la realidad; **¡NO!** es la verdad absoluta, pero funciona para resolver problemas rápidos. Por eso, el desafío más delicado no es transmitir datos, sino construir una estructura donde esos datos vivan: los _Novatos_ no tienen un modelo mental denso; los _Expertos_, sí.

Así entonces, la mente no es solo un receptor pasivo de información, sino un sistema que busca activamente construir modelos mentales.

!!! quote "Wilson (2019)"

       _"La **Máquina Nocional** es un tipo de modelo mental específico que propone Greg Wilson, utilizado para aprender o presentar un problema en programación. Es la abstracción idealizada del hardware y el entorno de ejecución que explica cómo la computadora toma el código (sintaxis) y le da significado (semántica), ejecutando acciones paso a paso"._


### 1.2.1 Gestión de la Carga Cognitiva

Uno de los factores de éxito de una máquina nocional radica en cómo se gestiona la **Carga Cognitiva** del aprendiz. Se trata de entender un poco sobre la fisiología de la mente y cómo trabaja cuando intentamos aprender o entender algo. Mientras que la _Memoria a Largo Plazo_ ofrece un almacenamiento masivo pero lento, la _Memoria a Corto Plazo_ es un cuello de botella rápido pero pequeño. La información (visual o verbal) solo se vuelve conocimiento si logra cruzar de una a otra sin causar una sobrecarga.

Por tanto, no hay que limitarnos solo a _trasmitir_ información, sino a aplicar la **regla de oro (7±2)** como lo menciona Greg Wilson para gestionar la carga cognitiva de los aprendices. El objetivo es evitar que la información nueva desplace a la anterior, asegurando que cada concepto tenga un lugar sólido donde vivir.

!!! quote "Wilson (2019)"

    _“La memoria de trabajo es limitada y solo puede retener aproximadamente 7 (más o menos 2) elementos a la vez. Si sobrepasamos este número saturamos la carga cognitiva del aprendiz. Investigaciones recientes indican que este número pude se más bajo como 4 (más o menos 1)”._

!!! example "Ejemplo"

    _(p.ej.) Sin una máquina nocional explícitamente diseñada por el facilitador, el Novato no deja su mente en blanco; la llena con basura cognitiva, no puede predecir qué hará el código ni depurarlo (debug). Solo puede adivinar y realizar cambios aleatorios esperando que funcione, lo cual refuerza malos hábitos. Finalmente, el costo más humano es la desmotivación._

La ausencia de sesiones de aprendizaje basadas en la gestión de la carga cognitiva, el aula (física o virtual) se vuelve un sistema de selección excluyente, no construimos el andamiaje adecuado y no estamos enseñando; estamos filtrando a las personas por sus capacidades previas en lugar de desarrollarlas.

!!! quote "Wilson (2019)"

    _“Cuando un estudiante se enfrenta a una carga cognitiva mal gestionada y falla, rara vez culpa al mal diseño instruccional; se culpa a sí mismo. Esto alimenta el **Síndrome del Impostor** y la creencia de que no tiene el gen para esto, afectando desproporcionadamente a grupos subrepresentados”_

### 1.2.2 Ejemplo de la ausencia de una Máquina Nocional
La Máquina Nocional es, desde mi perspectiva como facilitador, la herramienta más crítica para desmitificar la programación para los _Novatos_ o para aprender algo que implica utilizar un lenguaje de programación. Más que una lección técnica, representa el andamiaje psicológico indispensable para el aprendizaje.

A continuación, se propone un ejemplo basado en la literatura _“Teach Tech Together”_. Tiene el fin de ejemplificar una sobrecarga cognitiva producto de su mala gestión, además de la omisión de un modelo mental. Después se presentará el mismo ejemplo pero con una máquina nocional adecuada, que gestione su carga cognitiva sin llegar a la saturación de elementos, además de integrar otras estrategias que soportan el andamieaje cognitivo durante el aprendizaje:

!!! example "Ejemplo"

    _Imagina que alguien intenta enseñar a un grupo de Novatos cual es el estandar de datos "Geoespaciales utilizando R" (**simple feature**) y al mismo tiempo enseñar cómo se utiliza la biblioteca **sf** que gestiona esos datos presentando de golpe este fragmento de código:_

    ```r
    # Abrimos nuesto acrchivo .shp con los datos
    > sf_data <- st_read("puntos.shp")
    > sf_proj <- st_transform(sf_data, 4326)
    > p_buffer <- st_buffer(sf_proj, dist = 100)
    > print(paste("Área total:", sum(st_area(p_buffer)), "m2"))
    ```

    _Debido al **expert blind spot** (punto ciego del experto), el instructor presenta este fragmento de código creyendo que es trivial, pero mientras el experto ve un solo trozo, el Novato que aún no tiene modelos mentales funcionales sobre datos geoespaciales procesa cada carácter de forma aislada, llenando sus 7±2 espacios de memoria de trabajo en segundos._

El desgloce de elementos de la carga cognitiva es el siguiente:

1. **Lectura y Modelos de Archivos Geográficos**: La función `st_read()` asume que el aprendiz entiende qué es un shapefile (y que consta de múltiples archivos `.shp, .dbf, .shx`), además de cómo _R_ maneja las rutas de archivos.

2. **Objeto sf (Simple Features)**: El concepto de un data frame espacial que combina una tabla de atributos convencional con una columna geométrica especial (geometry / sfc).

3. **Sistemas de Referencia de Coordenadas (CRS)**: La función `st_transform()` introduce la diferencia entre coordenadas proyectadas (metros) y geográficas (grados).

4. **Códigos EPSG**: El argumento implícito `4326` exige saber que se refiere al estándar `WGS84`.

5. **Geoprocesamiento / Análisis Espacial**: La función `st_buffer()` introduce operaciones topológicas y la creación de nuevas geometrías alrededor de las existentes.

7. **Unidades de Distancia Espacial**: El argumento `dist = 100` genera ambigüedad si no se comprende en qué unidades está configurado el CRS actual (grados vs. metros).

8. **Vectorización y Operaciones Espaciales**: La función `st_area()` calcula superficies área por área retornando un vector con unidades explícitas (clase units).

9. **Agregación Vectorial**: La función `sum()` sobre un objeto de geometría espacial exige entender que se reduce un vector topológico a un escalar numérico.

10. **Coerción e Interpolación**: El uso de `paste()` para concatenar texto con la salida de un objeto con atributos de unidad espacial (units).

!!! nota

    _Como podemos observar, este es un claro ejemplo del **punto ciego del experto**: cuando un instructor, facilitador o profesional domina profundamente un tema, pierde la capacidad de estructurar el contenido desde la perspectiva de un Novato. De este modo, intenta abordar demasiados conceptos simultáneamente sin ofrecer a los aprendices un marco claro en donde organizar cada uno de estos elementos._

### 1.2.3 Ejemplo de una gestión de carga cognitiva
Ahora, se propone la construcción de una máquina nocional para acercar al mismo grupo de aprendices _Novatos_ a los conceptos *“Geoespaciales utilizando R”*, pero de manera estructurada y describiendo cada uno de los recursos extras de aprendizaje que dan soporte cognitivo a la máquina nocional.

<div style="background-color: #1a1c23; border-radius: 8px; padding: 1.2rem 1.5rem; color: #e6edf3; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; font-size: 0.95em; line-height: 1.6; margin: 1.5em 0; border: 1px solid #30363d;">
 <p style="margin: 0 0 1em 0;">📍 <b>Sesión:</b> 1 | <b>Categoría:</b> 🟢 Teórico |  <b>Tema:</b> El estándar <i>Simple Feature</i> y el paquete <i>sf</i></p> 
  
  <p style="margin: 0 0 1em 0;">🎯 <b>Objetivo:</b> Reconocer qué es el modelo "simple feature" y su implementación en <i>R</i>.</p>
  
  <br/>
  
  <p style="margin: 0 0 0.8em 0;">📌 <b>Interacción 1 de 5</b></p>
  
  <p style="margin: 0 0 0.8em 0;">Antes de meternos con definiciones formales, hay que entender de donde partimos:</p>
  
  <!-- BLOQUE DE RESPUESTA ALINEADO A LA DERECHA 1 -->
  <div style="display: flex; justify-content: flex-end; margin-top: 1em;">
    <div style="background-color: #21262d; border: 1px solid #30363d; border-radius: 8px; padding: 0.8em 1em; max-width: 80%; color: #c9d1d9;">
    <p style="margin: 0; font-size: 0.9em; text-align: right;"><b>Pregunta de abordaje:</b></p>
      <p style="margin: 0.3em 0 0 0; text-align: left;"><i>-"¿Alguna vez has trabajado con datos que tienen ubicación (coordenadas), con un mapa, con un archivo shapefile, con un GPS?"-; no importa si ha sido en R, en EXCEL o en un SIG; incluso si solo has mirando un mapa en el celular: -"¿cómo se ven esos datos"?; ¿son una tabla con columnas?; ¿tienen alguna forma en particualr?-".</i></p>
    </div>
  </div>

  <br/>
  <p style="margin: 0 0 0.8em 0;">📌 <b>Interacción 2 de 5</b></p>
  
  <p style="margin: 0 0 0.8em 0;">Utilizamos Google Maps para buscar una dirección o consultar la información de un lugar.
  
  Si lo pensamos un momento, cada punto en ese mapa hace dos cosas simultáneamente: nos da su ubicación geométrica (dónde está) y guarda un conjunto de atributos o datos (qué es, cuál es su nombre, su dirección o sus horarios). En esencia, une la geometría con la información.</p>

  Eso es exactamente lo que resuelve el estándar <i>Simple Feature</i>, es una manera formal y ampliamente adoptada (viene de una organización llamada OGC, Open Geospatial Consortium) de representar objetos del mundo real como geometría + atributos, de forma que distintas aplicaciones o programas como <b>QGIS, PostGIS, <i>R</i></b>... puedan leer y escribir los mismos datos sin perder información. En <i>R</i>, el paquete que implementa este estándar se llama <i>sf</i> (de simple features).</p>

  <p style="margin: 0;">Con esto en mente:</p>

  <!-- BLOQUE DE RESPUESTA ALINEADO A LA DERECHA 2 -->
  <div style="display: flex; justify-content: flex-end; margin-top: 1em;">
    <div style="background-color: #21262d; border: 1px solid #30363d; border-radius: 8px; padding: 0.8em 1em; max-width: 80%; color: #c9d1d9;">
      <p style="margin: 0; font-size: 0.9em; text-align: right;"><b>Pregunta de seguimiento:</b></p>
      <p style="margin: 0.3em 0 0 0; text-align: left;"><i>-"¿por qué crees que sería útil tener un estándar compartido entre programas, en lugar de que cada software (QGIS, R, ArcGIS) maneje los datos espaciales a su propia manera?"-...</i></p>
    </div>
  </div>
  <br/>
  <p style="margin: 0 0 0.8em 0;">📌 <b>Interacción 3 de 5</b></p>
  
  <p style="margin: 0 0 0.8em 0;">En todo momento debemos de tener muy en cuenta la <b>abstracción de la realidad</b> (p.ej.) <i>-"¿cómo representamos a un pozo como objeto geométrico junto con sus datos?"-</i>, tiene que ser consistente independientemente de qué motor de procesamiento hay detrás. Eso es justamente lo que permite que un archivo creado en el software "A" se abra sin sorpresas en <i>R</i>, o que los resultados de un análisis hecho en <i>R</i> se pueda visualizar después en el software "B".</p>
  
  Vamos un paso más allá con un ejemplo concreto. El paquete <i>sf</i> no solo implementa el estándar simple feature en <i>R</i>, lo hace con ventajas prácticas sobre el paquete que existía antes (llamado <i>sp</i>). Por ejemplo: usa una interfaz directa a librerías estándar de la industria geoespacial (GDAL para lectura/escritura, GEOS para operaciones geométricas), lo que se traduce en lectura y escritura de archivos más rápida. Todas sus funciones empiezan con el prefijo <i>st_</i> (de spatial type), como <i>st_read()</i>, <i>st_area()</i>, <i>st_intersects()</i>, así que en cuanto ves <i>"st_algo()"</i>, sabes que es una función de tipo espacial.</p>

  El prefijo <i>st_</i> te dice "es de <i>sf</i>", y lo que está en el paréntesis te dice qué hace. Es un patrón que se repite en todo el paquete y ese patrón de nombres consistentes es justo una de las ventajas que mencionamos hace un momento.</p>
  
  También es compatible con la filosofía de tidyverse (<i>dplyr, ggplot2</i>), así que un objeto <i>sf</i> se puede filtrar, mutar y graficar casi como si fuera una tabla normal de datos. Es decir: no es solo otro paquete que hace lo mismo, es una reescritura pensada para ser más rápida, más consistente en nombres, y más integrada con el resto del ecosistema de <i>R</i> moderno.</p>
  
  <p style="margin: 0;"></p>

  <!-- BLOQUE DE RESPUESTA ALINEADO A LA DERECHA 3 -->
  <div style="display: flex; justify-content: flex-end; margin-top: 1em;">
    <div style="background-color: #21262d; border: 1px solid #30363d; border-radius: 8px; padding: 0.8em 1em; max-width: 80%; color: #c9d1d9;">
      <p style="margin: 0; font-size: 0.9em; text-align: right;"><b>Pregunta de seguimiento y reforzamiento:</b></p>
      <p style="margin: 0.3em 0 0 0; text-align: left;"><i>Si tuvieras que adivinar, qué tipo de función crees que sería st_length(), -"¿qué esperarías que haga, solo por su nombre?"-...</i></p>
    </div>
  </div>
  <br/>

  <p style="margin: 0 0 0.8em 0;">📌 <b>Interacción 4 de 5</b></p>
  
  <p style="margin: 0 0 0.8em 0;">
  Como ya dijimos antes, la abstracción de la realidad (geometría + atributos) debe ser la misma para todos los programas. Pues bien, dentro de <i>R</i>, ese modelo de <i>Simple Feature</i> no es solamente una clase, sino que <i>sf</i> organiza a los objetos de la realidad en distintos tipos de geometría, según qué tan compleja sea la ubicación que quieres representar:</p>

<ol type="a" style="margin: 0 0 1em 1.5em; padding-left: 1em;">
  <li><b>Point:</b> un solo punto (ej. un pozo).</li>
  <li><b>Linestring:</b> una línea (ej. un río, un camino).</li>
  <li><b>Polygon:</b> un área cerrada (ej. el límite de un municipio).</li>
  <li><b>Y sus versiones múltiples:</b> Multipoint, Multilinestring, Multipolygon para cuando un solo "rasgo" (registro) está compuesto de varias piezas geométricas (p.ej. un municipio con dos islas se representaría como un Multipolygon).</li>
</ol>

Aquí es donde entra el vocabulario técnico formal: cada una de estas clases tiene un nombre reservado dentro de <i>sf</i>, y ese nombre determina qué operaciones puedes hacerle (p.ej. <i>st_length()</i> tiene sentido para Linestring, pero no para Polygon).</p>

  <!-- BLOQUE DE RESPUESTA ALINEADO A LA DERECHA 4 -->
  <div style="display: flex; justify-content: flex-end; margin-top: 1em;">
    <div style="background-color: #21262d; border: 1px solid #30363d; border-radius: 8px; padding: 0.8em 1em; max-width: 80%; color: #c9d1d9;">
      <p style="margin: 0; font-size: 0.9em; text-align: right;"><b>Pregunta de seguimiento y reforzamiento:</b></p>
      <p style="margin: 0.3em 0 0 0; text-align: left;"><i>Si tu archivo de pozos en R muestra puntos individuales para cada pozo: -"¿qué tipo de geometría sf crees que le correspondería?; "¿Point o Multipoint?"; "¿Por qué?"-...</i></p>
    </div>
  </div>
</br>
<p style="margin: 0 0 0.8em 0;">📌 <b>Interacción 5 de 5</b></p>
  
  <p style="margin: 0 0 0.8em 0;"> ✅ Qué aprendimos: El estándar simple feature representa objetos del mundo real como geometría + atributos de forma consistente entre programas. El paquete <i>sf</i> lo implementa <i>R</i> con ventajas de velocidad, nomenclatura consistente (<i>st_</i>) e integración con tidyverse. Existen varios tipos de geometría (Point, Linestring, Polygon y sus versiones múltiples) según la complejidad espacial del rasgo.</p>

  🔗 Cómo se conecta con lo que viene: La siguiente sesión profundiza en las ventajas de <i>sf</i> frente a <i>sp</i> con más detalle técnico y vocabulario que se usa constantemente.</p>

Aquí es donde entra el vocabulario técnico formal: cada una de estas clases tiene un nombre reservado dentro de <i>sf</i>, y ese nombre determina qué operaciones puedes hacerle (p.ej. <i>st_length()</i> tiene sentido para Linestring, pero no para Polygon).</p>

  <!-- BLOQUE DE RESPUESTA ALINEADO A LA DERECHA 4 -->
  <div style="display: flex; justify-content: flex-end; margin-top: 1em;">
    <div style="background-color: #21262d; border: 1px solid #30363d; border-radius: 8px; padding: 0.8em 1em; max-width: 80%; color: #c9d1d9;">
      <p style="margin: 0; font-size: 0.9em; text-align: right;"><b>Verificación de conocimiento:</b></p>
    <ol type="a" style="margin: 0.5em 0 0 1.2em; padding-left: 1em; font-style: italic; text-align: left;">
      <li>En tus propias palabras, ¿cuál es la diferencia entre un objeto Point y un objeto Multipoint?</li>
      <li>¿Por qué el prefijo st_ en los nombres de función es útil para alguien que está aprendiendo el paquete?</li>
    </ol>
    </div>
  </div>

</div>

1.  **El primer paso es establecer nuestros cimientos (el objetivo principal):**

    En esta parte los aprendices _Novatos_ **_"no saben lo que no saben"_**, mucho menos tienen modelos mentales sobre los datos geoespaciales. Por eso, el primer paso es plantear el cimiento de la máquina nocional más adecuado para el curso o capacitación:

    !!! example "Ejemplo"

        _(p.ej.) Introducir los conceptos "Geoespaciales en R" a un grupo de aprendices Novatos, para permitirnos responder: ¿Qué son los datos geoespaciales? y ¿Cómo interviene R en su procesamiento?._

    !!! note "Nota"

        _Debemos resistir la tentación de empezar con la **sintaxis del código**. Primero debemos instalar en sus mentes el objetivo de la Máquina Nocional: la elección del modelo mental más simplificado de cómo la computadora y R perciben el espacio viene después._

2. **Presentación del modelo mental**:

    Para un _Novato_, el nivel de abstracción más efectivo es una **_"Caricatura Funcional"_** de la realidad. No debemos enseñarles sobre bits, ni formatos de archivo complejos (como la estructura interna de un Shapefile), ni sobre cómo <i>R</i> gestiona la memoria física.

    !!! nota

        _El modelo mental propuesto es ***Google Maps*** porque es muy probable que la mayoría ya lo haya usado para buscar una dirección. Es algo muy común._

3. **Gestión de la Carga Cognitiva**:

    Evitamos saturar la carga cognitiva del aprendiz dividiendo esta máquina en cinco partes o interacciones, respetando la **regla de oro (7±2)**: desde **_-"¿qué son los datos geoespaciales?”-_** hasta **_-“¿qué tiene que ver R en todo esto?”-_**.

4. **Evaluación del aprendizaje**:

    Durante las interacciones se presentan preguntas a manera de pequeños retos, que se utilizan para evaluar si la máquina está bien construida o si se utilizó el modelo mental correcto. Esto sirve para ir afinando las siguientes sesiones mientras se avanza en las interacciones hasta concluir la capacitación.

    !!! nota

        _En esta primera sesión, no se abordan otros elementos como las funciones para la gestión interna de archivos en R u operaciones espaciales como **st_buffer(sf_proj, dist = 100)**. Por eso es importante planear el número de sesiones necesarias para ir introduciendo el nuevo conocimiento de manera escalonada._


### Conclusión
___
Greg Wilson concluye que enseñar programación de forma efectiva exige abandonar la intuición y tratar la docencia como una disciplina basada en evidencia, desplazando el enfoque tradicional centrado en la sintaxis hacia la construcción explícita de modelos mentales. Para lograrlo, enfatiza que los instructores deben mitigar conscientemente su propio punto ciego de experto mediante la reducción de la carga cognitiva del aprendiz, utilizando la codificación en vivo (como más adelante se verá), la retroalimentación formativa frecuente y el aprendizaje entre pares para diagnosticar errores conceptuales antes de avanzar a la implementación técnica.

Este enfoque pedagógico también se puede potenciar de manera rigurosa al estructurar las capacitaciones bajo la metodología instruccional del estándar de competencia EC0366 en México, el cual garantiza el diseño sistemático de cursos en línea mediante objetivos medibles, secuencias didácticas validadas y guías de evaluación alineadas. De este modo, la evidencia cognitiva propuesta por Wilson se traduce en una arquitectura instruccional estandarizada que asegura la efectividad del aprendizaje o el cumplimiento de altos criterios de calidad profesional.