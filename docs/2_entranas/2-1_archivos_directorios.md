Todo el mundo quiere saltar directamente a la sala de operaciones, sin saber siquiera qué es un bisturí. Bien, en esta sección reconoceremos primero como hay que construir los pilares que sostienen cualquier experiencia didáctica de _Swirlify_. 

!!! warning "Alto"

    _Antes de avanzar es importante diferenciar dos conceptos, swirl y Swirlify. Por un lado **swirl** es el paquete de R que el aprendiz installa y su trabajo es correr en la consola, leer los archivos de la lección, presentar las preguntas, evaluar respuestas; **Swirlify**, como ya hemos venido diciendo, es el paquete donde los creadores e instructores redactamos los archivos lesson.yaml, initLesson.R, dependson.txt... Dicho de otra forma Swirlify crea la enfermedad (la lección) y swirl la padece (el aprendiz la toma)._


# 2.1 Estructura de archivos y directorios de Swirlify. 
___
En ***Swirlify***, la organización de carpetas y archivos tiene que seguir un estándar estricto para garantizar que la lección sea ejecutada, correctamente validada mediante `test_lesson()` y empaquetada para llegar a los aprendices (Swirl Development Team, s.f.).             

Así, un curso de _Swirlify_ contiene una carpeta raíz con el nombre del curso, dentro de la cual se ubica una carpeta por cada lección, junto con archivos globales de control.  

Dibujemos esto con crayolas:

```bash
Mi_Curso/
├── MANIFEST                   ← Define el orden de las lecciones (OBLIGATORIO si hay >2 lecciones)
├── datos_compartidos/         ← Carpeta para datasets globales a múltiples lecciones (OPCIONAL)
│   ├── dataset_global1.csv
│   └── dataset_global2.rds
└── Mi_Leccion_1/              ← Carpeta específica de la lección
    ├── lesson.yaml            ← Contenido, preguntas y respuestas (OBLIGATORIO)
    ├── initLesson.R           ← Código R de preparación previa (OBLIGATORIO)
    ├── dependson.txt          ← Paquetes de R necesarios (OBLIGATORIO)
    ├── customTests.R          ← Tests de validación personalizados (OBLIGATORIO)
    ├── datos.csv              ← Archivos de datos específicos de la lección (OPCIONAL)
    ├── grafico_figura.R       ← Scripts de generación de figuras (OPCIONAL)
    └── scripts/               ← Subcarpeta para preguntas tipo 'script' (OPCIONAL)
        ├── mi_script.R        ← Plantilla que edita el aprendiz
        └── mi_script-correct.R← Solución correcta del script
```

A continuación, se describe el kit de herramienta, los archivos que son de relevancia para cualquier curso de _Swirlify_.

### 2.1.1 Jerarquía Obligatoria

#### A. `lesson.yaml`
Este es el corazón de la lección en  _Swirlify_. Es el archivo de metadatos y configuración donde se define la estructura de la lección, el orden de los módulos, las preguntas, las pistas (_hint_), el código que se evalúa y los mensajes que ve el usuario (tanto los aplausos vacíos cuando aciertan como los lamentos cuando fallan). Básicamente, es una serie de filas estructuradas en formato YAML que _R_ traduce en la experiencia interactiva.

- **Requisito YAML:** Sensible a la indentación; usa espacios, si usas (tabs) en lugar de espacios, o si la alineación está mal por un milímetro, todo se viene abajo.
- **El manejo de comillas y caracteres especiales**: Como los textos de las preguntas y respuestas van dentro de YAML, un apóstrofe mal escapado o unas comillas mal cerradas arruinan el análisis sintáctico del archivo (`yaml::yaml.load_file` se va a quejar y con toda razón).
- **La correspondencia entre clases (Class:)**: Cada bloque en el `lesson.yaml` tiene un tipo de clase (ej. `cmd_question`, `text, mult_question`). Si se declara mal a la clase, lección colapsa.

```yaml
- Class: meta
  Course: Nombre del Curso
  Lesson: Nombre de la Lección
  Author: Tu Nombre Completo
  Type: Standard
  Organization: Tu Organización
  Version: 2.5
```  
!!! quote "Swirlify (Swirl Development Team)"

    _"Una **clase** en Swirlify es el tipo de bloque estructural que define cómo se comportará un paso específico dentro de tu archivo lesson.yaml. Le dice al motor de swirl exactamente qué herramienta debe utilizar, qué interfaz mostrar en la consola de R (texto plano, una pregunta interactiva, la evaluación de código de R, una opción múltiple, etc.) y cómo debe evaluar la respuesta del aprendiz"._

Existen todas estas clases, son nueve en total: `meta`, `text`, `multi_question`, `cmd_question`, `figure`, `video`, `exact_question`, `range_question`, `script`.    

!!! danger "Peligro"

    _Siempre, sin excepciones, sin excusas y sin berrinches, debemos insertar un bloque con la clase **meta** al inicio absoluto de cada archivo lesson.yaml. Si omitimos la clase, estaremos intentando operar a un paciente sin anestesia ni expediente clínico: el sistema se desploma, rechaza el archivo y te arroja un error._


#### B. `initLesson.R`
Cuando _swirl_ ejecuta una lección, a veces necesita preparar el terreno en la sesión de _R_ del aprendiz antes de que empiece a responder preguntas: cargar conjuntos de datos específicos, definir variables personalizadas, o limpiar el entorno para que el paciente no arrastre errores de diagnósticos anteriores.  

```r
# Función auxiliar obligatoria para resolver la ruta del curso
.get_course_path <- function(){
  tryCatch(swirl:::swirl_courses_dir(),
           error = function(c) {file.path(find.package("swirl"), "Courses")}
  )
}

# Cargar dataset de la lección
mis_datos <- read.csv(file.path(.get_course_path(), 
                                "Mi_Curso", 
                                "Mi_Leccion_1", 
                                "datos.csv"))
```    

Como este archivo es un script de _R_ común y corriente, significa que en teoría se puede introducir cualquier código que soporte el lenguaje. Pero el hecho de que **podamos hacerlo no significa que debdebamos hacerlo**.

!!! example "Ejemplo"

    _(p.ej. )Imagina que a un colega tuyo (imprudentemente) se le ocurre la brillante idea de incluir una línea dentro de `initLesson.R` que borre todos los archivos del directorio de trabajo del usuario para "empezar limpio", o bien, que intente instalar un paquete pesado de CRAN en cada inicio de lección._

!!! Nota

    _Las recomendaciones de los manuales de enseñanza (como los de RStudio Education y Carpentries) dictan que el entorno del aprendiz debe mantenerse limpio, predecible y libre de efectos secundarios destructivos. Si nos ponemoss de creativos y rompemos el espacio de trabajo global, el sistema colapsa._

Estos son algunos límites y prohibiciones que debemos tener en cuenta dentro de este archivo:  

- **No modificar las opciones globales de _R_ de forma permanente (`options()` o `par()`)**: Si cambiamos la configuración global del sistema o los gráficos de forma agresiva sin restaurarla, arruinaremos la sesión de _R_ del usuario para el resto de su día. Si alteras algo temporalmente, asegúrate de limpiarlo al salir.

- **Evitar instalar paquetes desde internet dentro del script (`install.packages()`)**: Jamás, bajo ninguna circunstancia, ejecutemos comandos de instalación automática de paquetes aquí. Si el usuario no tiene internet, si el repositorio falla o si el cortafuegos bloquea la descarga (como en muchas escuelas), la lección entera muere. Las dependencias deben estar instaladas antes de arrancar.

- **No ejecutar código destructivo o de modificación del disco duro del usuario**: Olvidémonos de borrar archivos (`file.remove()`), modificar directorios raíz o sobreescribir datos críticos del sistema operativo del usuario. El script debe limitarse a preparar variables y cargar conjuntos de datos locales de la lección.

- **Tener cuidado con los tiempos de carga**: Si ponemos a _R_ a leer un archivo CSV de gigabytes o a entrenar un modelo de machine learning complejo cada vez que se inicia la lección, el usuario se aburrirá y cerrará la consola. Hay que mantener la carga ligera y rápida.
    
#### C. `dependson.txt`
En _Swirlify_, este archivo de texto plano enumera las dependencias de paquetes de _R_ necesarios para la lección. Es la lista de medicamentos y herramientas previas que el cirujano necesita tener en su quirófano antes de operar.  

```txt
dplyr
ggplot2
tidyr
``` 
Su único propósito es declarar qué paquetes de CRAN, GitHub u otros repositorios deben estar instalados obligatoriamente en el entorno de _R_ del aprendiz para que la lección no colapse a mitad del proceso. Si una lección requiere funciones de `ggplot2`, `dplyr` o `tidyr`, y el usuario no los tiene instalados, _swirl_ se detendrá de golpe. `dependson.txt` le avisa al sistema (y al usuario) qué debe inyectar en el entorno antes de arrancar.

Al igual que en `initLesson.R`, como buen cirujano, debemos de tener cuidado con lo que recetamos.  

- **No incluyas paquetes base de _R_**: Paquetes como `base`, `stats`, `utils` o `graphics` vienen preinstalados con _R_.    
- **Cuidado con las versiones o fuentes externas**: Por defecto, _Swirlify_ busca los paquetes en CRAN. Si pones un paquete que solo existe en una versión específica de GitHub o que ya fue retirado de los repositorios oficiales, el script de carga fallará estrepitosamente y colapsará la lección.  
- **Mantén la lista al mínimo estricto**: Evitemos colocalr una lista de 50 paquetes "por si acaso". Solo hay que declara aquello que la lección vaya a utilizar de manera imperativa. Menos ruido, menos fallos.  

#### D. `customTests.R`
Si no quieres solamente usar pruebas de validación estándar que vienen por defecto en _swirl_ y quieres evaluar algo verdaderamente retorcido en el código de un aprendiz: _"¿quieres verificar si el aprendiz creó un gráfico con capas específicas en ggplot2?"; "¿si estructuró un objeto de datos de una forma limpía o si calculó una varianza usando una función prohibida?"_... para eso sirve `customTests.R`.  

Este script **opcional** se aloja en la carpeta de la lección. Cada función que definamos aquí puede ser llamada desde el archivo `lesson.yaml` en el campo `AnswerTests` para evaluar las entradas del paciente con la precisión de un bisturí láser.

```r
# Definimos una prueba personalizada para verificar si el usuario creó un objeto llamado 'resultado' y si es un número positivo.
test_resultado_positivo <- function() {
  # Recuperamos el entorno del usuario
  e <- get("e", parent.frame())
  
  # Verificamos si la variable 'resultado' existe en su consola
  if (!"resultado" %in% names(e$val)) {
    return(FALSE)
  }
  
  # Evaluamos la condición clínica: ¿es mayor a cero?
  is.numeric(e$val$resultado) && e$val$resultado > 0
}
```
!!! tip

    _Si creas una prueba personalizada, asegúrate de acompañarla de un buen AnswerHint en el lesson.yaml. De lo contrario, el aprendiz fallará y no tendrá la menor idea de por qué su código fue rechazado._


### 2.1.2 Carpetas y Archivos Especiales de Swirlify

#### A. `MANIFEST`
Pensemos en este archivo como una lista de asistencia. Cuando _swirl_ empaqueta una lección para distribuirla (o cuando _Swirlify_ la prepara para su exportación), el sistema necesita saber exactamente qué archivos forman parte de esa lección (el archivo YAML, scripts auxiliares, conjuntos de datos CSV, imágenes, entre otros). El archivo `MANIFEST` es un simple archivo de texto plano que contiene la lista de todos los archivos que deben incluirse en el paquete comprimido de la lección (`.swirl`). Si un archivo secundario existe en la carpeta pero no está declarado en el `MANIFEST`, _swirl_ lo ignorará por completo y tu lección llegará incompleta al aprendiz.

```txt
lesson.yaml
initLesson.R
depends.on.txt
mis_datos.csv
grafico_diagnostico.png
```
Aspectos críticos que debemos cuidar:  

- **Rutas relativas declaradas**: Los nombres de los archivos en el `MANIFEST` deben coincidir exactamente con lo que hay en la carpeta de la lección. Si escribimos mal una letra o una extensión (ej. `.CSV` en lugar de `.csv`), el empaquetador fallará.  

- **Olvidar actualizarlo**: Cada vez que agreguemos un nuevo dataset, un gráfico o un script de soporte a la lección, debemos registrarlo aquí. Si nos olvidasmos de actualizarlo, el aprendiz intentará cargar un archivo que nunca viajó en el paquete. 

#### B. Carpeta de scripts

En la anatomía de una lección de _Swirlify_, la carpeta llamada textualmente `scripts/` (situada dentro de la carpeta de tu lección) es el depósito donde guardamos archivos de código de _R_ de apoyo que el aprendiz no edita directamente, pero que necesita leer, consultar o ejecutar parcialmente durante la lección.

A diferencia de `initLesson.R` (que se ejecuta de manera invisible y automática al arrancar la lección) o de los ejercicios que el alumno resuelve en la consola, los archivos que metes dentro de la carpeta scripts sirven como plantillas, scripts de ejemplo o fragmentos de código complementarios que el alumno puede abrir en su propio editor de texto (como RStudio) para analizarlos en paralelo mientras avanza en la lección.

_-"¿Es obligatoria?"-_ **Absolutamente NO**. Si la lección es puramente interactiva en la consola o basada en preguntas de opción múltiple y texto, la carpeta scripts brilla por su ausencia y nadie va a morir, todo dependerá del diseño instruccional del facilitador.

!!! example "Ejemplo"

    _(p.ej.) Cuando queremos enseñar buenas prácticas de formato, cómo estructurar un archivo de análisis de datos complejo, o cómo funciona un flujo de trabajo con múltiples funciones que no caben en una sola línea de comando de la consola interactiva._

### 2.1.3 Lógica de Ejecución del Motor (swirl Engine)  
El motor de `swirl` procesa el archivo `lesson.yaml` secuencialmente como un autómata de estados. Es decir, `swirl` funciona como una máquina paso a paso: se detiene en cada bloque de `lesson.yaml`, evalúa lo que el usuario ingresa en la consola, y solo cuando se cumple la condición de validación "avanza de estado",  al siguiente bloque del archivo.  

```txt
[Inicio] -> Ejecuta initLesson.R -> Carga dependson.txt
  │
  ▼
[Lee Bloque YAML] 
  │
  ├── Class: text --------> Muestra mensaje -> Espera [Enter] -> Siguiente
  │
  ├── Class: cmd_question -> Muestra prompt R 
  │                            │
  │                            ▼
  │                      [Estudiante ingresa código]
  │                            │
  │                            ▼
  │                      Evalúa en el Global Environment
  │                            │
  │                            ▼
  │                      Ejecuta AnswerTests (omnitest / customTests)
  │                            │
  │                            ├── TRUE  -> Muestra éxito -> Siguiente
  │                            └── FALSE -> Muestra Hint -> Reintenta
```   
___

**Resumen de Reglas de Nomenclatura Técnica**

1. **Formatos de archivo y directorios:** Utilizar siempre `snake_case` o `PascalCase` (p.ej. `Leccion_1`, `datos_ventas.csv`).

2. **Caracteres prohibidos:** Evitar espacios, tildes, eñes o caracteres especiales en los nombres de carpetas y archivos `.yaml` o `.R`.



