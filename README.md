# Generador de Horarios para Estudiantes

**Autora:** Valentina Rojas (z1)
**Tecnología:** Python 3 y JSON

## Propósito

Esta aplicación de consola permite organizar materias y actividades de lunes a viernes. El usuario puede registrar, consultar, modificar y eliminar eventos. Además, puede crear un reporte semanal en formato JSON.

El proyecto usa franjas fijas de dos horas para mantener el horario claro y evitar que dos actividades ocupen el mismo espacio.

## Funciones del programa

1. Registrar una materia o actividad.
2. Ver el horario semanal en una tabla.
3. Modificar una materia o actividad existente.
4. Eliminar una materia o actividad.
5. Generar un reporte semanal en pantalla y en JSON.
6. Salir del programa.

## Franjas disponibles

Las actividades deben usar una de estas franjas:

| Inicio | Fin |
| --- | --- |
| 08:00 | 10:00 |
| 10:00 | 12:00 |
| 12:00 | 14:00 |
| 14:00 | 16:00 |

No se puede registrar más de una actividad en el mismo día y con la misma hora de inicio. Por ejemplo, si ya existe Matemáticas el lunes de 08:00 a 10:00, no se puede registrar otra actividad en esa franja.

## Estructura

```text
Proyecto_Python_Valentina_Rojas_z1/
├── main.py                 # Menú y punto de inicio
├── funciones.py            # Funciones para gestionar el horario
├── horario.json            # Eventos guardados
├── reporte_horario.json    # Reporte generado
└── README.md               # Documentación del proyecto
```

## Cómo ejecutar

1. Abrir una terminal en la carpeta del proyecto.
2. Ejecutar:

```bash
python main.py
```

3. Escribir el número de la opción deseada y seguir las instrucciones en pantalla.

## Cómo viajan los datos

Cuando se registra una actividad, el programa sigue este recorrido:

```text
input del usuario → diccionario → lista horario → horario.json → tabla o reporte
```

Cada actividad se guarda como un diccionario. Por ejemplo:

```json
{
    "materia": "Matemáticas",
    "dia": "Lunes",
    "hora_inicio": "08:00",
    "hora_fin": "10:00",
    "ubicacion": "Aula 101"
}
```

## Conceptos para la presentación

- **Listas:** guardan todos los eventos del horario. Se usa `append()` para agregar y `remove()` para eliminar.
- **Diccionarios:** guardan los datos de una actividad mediante claves como `materia` y `dia`.
- **Condicionales:** `if`, `elif` y `else` deciden qué opción del menú ejecutar o si un dato es válido.
- **Bucles:** `while` mantiene activo el menú; `for` recorre los eventos y los días.
- **Funciones:** agrupan una tarea concreta, por ejemplo `registrar_evento(horario)`.
- **Cadenas:** `input()` recibe texto; `.strip()` elimina espacios innecesarios y `.lower()` permite comparar nombres sin importar mayúsculas.
- **Validación de texto:** la función `normalizar_texto()` quita las tildes antes de comparar. Por eso `MIERCOLES`, `miércoles` y `Miércoles` se entienden como el mismo día; también funciona al buscar materias como `fisica` o `FÍSICA`.
- **JSON:** `json.load()` lee el horario desde un archivo y `json.dump()` guarda los cambios.

## Guía breve para exponer

1. Explicar que `main.py` muestra el menú y `funciones.py` reúne las acciones del horario.
2. Mostrar un registro: se pide nombre, día, horas y ubicación.
3. Explicar el control de choque: se recorre la lista y se compara el día y la hora de inicio.
4. Mostrar que cada cambio se guarda inmediatamente en `horario.json`.
5. Ejecutar la opción de reporte y explicar que se agrupa la información por día. La pausa con ENTER permite leer cada día antes de continuar.

## Simulación y validaciones para practicar

El archivo `horario.json` incluye actividades de ejemplo durante toda la semana. Antes de la presentación, prueba estas entradas y explica el resultado:

| Acción | Entrada de ejemplo | Resultado esperado |
| --- | --- | --- |
| Ver horario | Opción `2` | Muestra actividades y espacios `Libre`. |
| Día con mayúsculas | `LUNES` | El programa lo acepta como `Lunes`. |
| Día sin tilde | `MIERCOLES` | El programa lo acepta como `Miércoles`. |
| Buscar materia | `fisica` y `miercoles` | Encuentra `Física` del miércoles. |
| Franja incorrecta | `09:00` a `11:00` | Muestra un mensaje con las franjas permitidas. |
| Choque de horario | Registrar el lunes de `08:00` a `10:00` | No permite registrar otra actividad en ese bloque. |
| Salir | Opción `6` y ENTER | Vuelve al menú. Solo `Y` confirma la salida. |

## Material de estudio oficial

- [Listas en Python](https://docs.python.org/es/3/tutorial/introduction.html#lists)
- [Diccionarios en Python](https://docs.python.org/es/3/tutorial/datastructures.html#dictionaries)
- [Estructuras de control](https://docs.python.org/es/3/tutorial/controlflow.html)
- [Definir funciones](https://docs.python.org/es/3/tutorial/controlflow.html#defining-functions)
- [Entrada y salida](https://docs.python.org/es/3/tutorial/inputoutput.html)
- [Módulo json](https://docs.python.org/es/3/library/json.html)

