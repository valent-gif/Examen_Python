"""Funciones del Generador de Horarios para Estudiantes."""

import json


DIAS = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]
FRANJAS = {
    "08:00": "10:00",
    "10:00": "12:00",
    "12:00": "14:00",
    "14:00": "16:00",
}


def normalizar_texto(texto):
    """Convierte un texto a minúsculas y quita tildes para compararlo."""
    cambios = {
        "á": "a",
        "é": "e",
        "í": "i",
        "ó": "o",
        "ú": "u",
        "ü": "u",
    }
    texto = texto.lower()

    for letra_con_tilde, letra_sin_tilde in cambios.items():
        texto = texto.replace(letra_con_tilde, letra_sin_tilde)

    return texto


def guardar_horario(horario):
    """Guarda la lista de eventos en horario.json."""
    with open("horario.json", "w", encoding="utf-8") as archivo:
        json.dump(horario, archivo, indent=4, ensure_ascii=False)


def pedir_dia(dia_actual=None):
    """Pide un día de lunes a viernes y devuelve None si no es válido."""
    mensaje = "Día (Lunes a Viernes): "
    if dia_actual is not None:
        mensaje = f"Nuevo día [ENTER conserva {dia_actual}]: "

    dia_escrito = input(mensaje).strip()
    if dia_escrito == "" and dia_actual is not None:
        return dia_actual

    for dia_valido in DIAS:
        if normalizar_texto(dia_escrito) == normalizar_texto(dia_valido):
            return dia_valido

    print("Día no válido. Debe ser de Lunes a Viernes.")
    return None


def pedir_horas(hora_inicio_actual=None, hora_fin_actual=None):
    """Pide una franja de dos horas y devuelve una tupla con inicio y fin."""
    print("Franjas disponibles: 08:00-10:00, 10:00-12:00, 12:00-14:00 y 14:00-16:00.")
    inicio = input("Hora de inicio: ").strip()
    fin = input("Hora de fin: ").strip()

    if inicio == "" and fin == "" and hora_inicio_actual is not None:
        return hora_inicio_actual, hora_fin_actual

    if inicio not in FRANJAS or FRANJAS[inicio] != fin:
        print("Franja no válida. Use bloques de dos horas: 08:00-10:00, "
            "10:00-12:00, 12:00-14:00 o 14:00-16:00.")
        return None
    return inicio, fin


def existe_choque(horario, dia, hora_inicio, evento_a_ignorar=None):
    """Devuelve True si ya hay un evento en el mismo día y franja."""
    for evento in horario:
        if evento is evento_a_ignorar:
            continue
        if evento["dia"] == dia and evento["hora_inicio"] == hora_inicio:
            return True
    return False


def registrar_evento(horario):
    print("\n--- REGISTRAR EVENTO ---")
    print("Completa los datos. La ubicación es opcional.")
    materia = input("Nombre de la materia o actividad: ").strip()
    if materia == "":
        print("El nombre no puede estar vacío.")
        return

    dia = pedir_dia()
    if dia is None:
        return

    horas = pedir_horas()
    if horas is None:
        return
    hora_inicio, hora_fin = horas

    if existe_choque(horario, dia, hora_inicio):
        print("Ya existe una actividad en ese día y esa franja horaria.")
        return

    ubicacion = input("Ubicación (ENTER para omitir): ").strip()
    if ubicacion == "":
        ubicacion = "No especificada"

    nuevo_evento = {
        "materia": materia,
        "dia": dia,
        "hora_inicio": hora_inicio,
        "hora_fin": hora_fin,
        "ubicacion": ubicacion,
    }
    horario.append(nuevo_evento)
    guardar_horario(horario)
    print("Evento registrado con éxito.")


def ver_horario_semanal(horario):
    print("\n" + "=" * 91)
    print(f"| {'Hora':<13} | {'Lunes':<12} | {'Martes':<12} | {'Miércoles':<12} | {'Jueves':<12} | {'Viernes':<12} |")
    print("=" * 91)

    for inicio, fin in FRANJAS.items():
        fila = f"| {inicio + '-' + fin:<13} |"
        for dia in DIAS:
            nombre = "Libre"
            for evento in horario:
                if evento["dia"] == dia and evento["hora_inicio"] == inicio:
                    nombre = evento["materia"]
                    break
            fila += f" {nombre[:12]:<12} |"
        print(fila)
    print("=" * 91)


def buscar_evento(horario, materia, dia):
    """Busca un evento por materia y día, sin distinguir mayúsculas."""
    for evento in horario:
        misma_materia = normalizar_texto(evento["materia"]) == normalizar_texto(materia)
        mismo_dia = normalizar_texto(evento["dia"]) == normalizar_texto(dia)
        if misma_materia and mismo_dia:
            return evento
    return None


def modificar_evento(horario):
    print("\n--- MODIFICAR EVENTO ---")
    materia = input("Nombre de la materia o actividad a modificar: ").strip()
    if materia == "":
        print("El nombre no puede estar vacío.")
        return
    dia = pedir_dia()
    if dia is None:
        return

    evento = buscar_evento(horario, materia, dia)
    if evento is None:
        print("No se encontró esa materia en el día indicado.")
        return

    print("\nActividad encontrada:")
    print(f"{evento['materia']} | {evento['dia']} | "
        f"{evento['hora_inicio']}-{evento['hora_fin']} | {evento['ubicacion']}")
    print("Presiona ENTER en un campo para conservar su valor actual.")

    nuevo_nombre = input(f"Nuevo nombre [ENTER conserva {evento['materia']}]: ").strip()
    if nuevo_nombre == "":
        nuevo_nombre = evento["materia"]
    if nuevo_nombre == "":
        print("El nombre no puede estar vacío.")
        return
    nuevo_dia = pedir_dia(evento["dia"])
    if nuevo_dia is None:
        return
    horas = pedir_horas(evento["hora_inicio"], evento["hora_fin"])
    if horas is None:
        return
    nueva_hora_inicio, nueva_hora_fin = horas

    if existe_choque(horario, nuevo_dia, nueva_hora_inicio, evento):
        print("Ya existe una actividad en ese día y esa franja horaria.")
        return

    nueva_ubicacion = input(f"Nueva ubicación [ENTER conserva {evento['ubicacion']}]: ").strip()
    if nueva_ubicacion == "":
        nueva_ubicacion = evento["ubicacion"]

    evento["materia"] = nuevo_nombre
    evento["dia"] = nuevo_dia
    evento["hora_inicio"] = nueva_hora_inicio
    evento["hora_fin"] = nueva_hora_fin
    evento["ubicacion"] = nueva_ubicacion
    guardar_horario(horario)
    print("Evento modificado con éxito.")


def eliminar_evento(horario):
    print("\n--- ELIMINAR EVENTO ---")
    materia = input("Nombre de la materia o actividad a eliminar: ").strip()
    if materia == "":
        print("El nombre no puede estar vacío.")
        return
    dia = pedir_dia()
    if dia is None:
        return

    evento = buscar_evento(horario, materia, dia)
    if evento is None:
        print("No se encontró esa materia en el día indicado.")
        return

    horario.remove(evento)
    guardar_horario(horario)
    print("Evento eliminado con éxito.")


def generar_reporte(horario):
    """Agrupa los eventos por día, los guarda y los muestra con pausas."""
    reporte = []
    for dia in DIAS:
        eventos_del_dia = []
        for evento in horario:
            if evento["dia"] == dia:
                eventos_del_dia.append({
                    "materia": evento["materia"],
                    "hora_inicio": evento["hora_inicio"],
                    "hora_fin": evento["hora_fin"],
                    "ubicacion": evento["ubicacion"],
                })
        reporte.append({"dia": dia, "eventos": eventos_del_dia})

    with open("reporte_horario.json", "w", encoding="utf-8") as archivo:
        json.dump(reporte, archivo, indent=4, ensure_ascii=False)

    print("\n--- REPORTE DEL HORARIO SEMANAL ---")
    for dia in reporte:
        print(f"\n{dia['dia']}:")
        if len(dia["eventos"]) == 0:
            print("- No hay actividades registradas.")
        else:
            for evento in dia["eventos"]:
                print(f"- {evento['materia']} ({evento['hora_inicio']}-{evento['hora_fin']}) en {evento['ubicacion']}")
        input("Presione ENTER para continuar...")

    print("Reporte guardado en reporte_horario.json.")

#No me rendiré, seguiré practicando hasta ser la mejor programadora del mundo.


    #Funcion adicional.
    #Funcinalidad de filtrado por ubicacion, mostrar que materia se ven en esa aula.
    
def filtrar_por_ubicacion(horario):
#Pedir el dato y guardarlo een la variable ubicacion
    print("\n---FILTRAR POR UBICACION---")
    ubicacion = (input("Ingrese el nombre del aula de clase")).strip()
#Valildar if y return si la variable esta vacia
    if ubicacion == "":
        print("La ubicacion no puede estar vacia")
        return
    encontrado = False

    for evento in horario:
        if normalizar_texto(evento["ubicacion"]) == normalizar_texto(ubicacion_buscada):
            if not encontrado:
                print(f"\n-Actividades encontradas encontradas en '{ubicacion_buscada}":)
                encontrado = True
            print(
                f"- {evento['materia']} | {evento['dia']} "
                f"({evento['hora_inicio']}-{evento['hora_fin']}) | "
                f"Ubicación: {evento['ubicacion']}"
            )
    if not encontrado:
        print(f"No se encontraron actividades registradas en '{ubicacion_buscada}'.")

#Funcionalidad por dia
#Mostrar solo la informacion de un dia de la semana(el seleccionado)


def filtrar_dia_especifico(horario):
    print("\n---FILTRAR POR DIA---")
#Pedir dia() preegunta al usuario y lo guarda
    dia_buscado = pedir_dia()

#Si el día fue inválido o estuvo vacío, pedir_dia() devuelve None
    if dia_buscado is None:
        return
    encontrado = False

#recorre los eventos del horario
    for evento in horario:
        if normalizar_texto(evento["dia"]) == nomalizar_texto(dia_buscado):
            if not encontrado:
                print(f"\n-Actividades encontradas encontradas en '{dia_buscada}":)
                encontrado = True
            print(
                f"- {evento['materia']} | "
                f"({evento['hora_inicio']}-{evento['hora_fin']}) | "
                f"Ubicación: {evento['ubicacion']}"
            )
    if not encontrado:
        print(f"No se encontraron actividades registradas en el  '{dia_buscada}'.")

#Funcionalidada adicional
def filtrar_por_franja(horario):
    """Muestra todas las materias programadas en una franja horaria específica a lo largo de la semana."""
    print("\n--- FILTRAR POR FRANJA HORARIA ---")
    horas = pedir_horas()
    if horas is None:
        return

    hora_inicio, hora_fin = horas
    encontrado = False

    for evento in horario:
        if evento["hora_inicio"] == hora_inicio:
            if not encontrado:
                print(f"\nActividades programadas en la franja {hora_inicio}-{hora_fin}:")
                encontrado = True
            print(f"- {evento['dia']}: {evento['materia']} en {evento['ubicacion']}")

    if not encontrado:
        print(f"No tienes ninguna actividad programada en la franja {hora_inicio}-{hora_fin}.")

#Filttrar por materia 

def filtrar_por_materia(horario):
    """Busca todas las sesiones programadas para una materia o palabra clave."""
    print("\n--- FILTRAR POR MATERIA O PALABRA CLAVE ---")
    busqueda = input("Ingrese la materia o palabra clave a buscar: ").strip()

    if busqueda == "":
        print("El término de búsqueda no puede estar vacío.")
        return

    busqueda_normalizada = normalizar_texto(busqueda)
    encontrado = False

    for evento in horario:
        materia_normalizada = normalizar_texto(evento["materia"])
        if busqueda_normalizada in materia_normalizada:
            if not encontrado:
                print(f"\nSesiones encontradas para '{busqueda}':")
                encontrado = True
            print(
                f"- {evento['materia']} | {evento['dia']} "
                f"({evento['hora_inicio']}-{evento['hora_fin']}) | "
                f"Ubicación: {evento['ubicacion']}"
            )

    if not encontrado:
        print(f"No se encontraron actividades relacionadas con '{busqueda}'.")

#Funciones obtener horraio libre

def obtener_horarios_libres(horario):
    """Genera un listado de los bloques de tiempo en los que no hay actividades registradas."""
    print("\n--- HORARIOS LIBRES DE LA SEMANA ---")
    hay_libres = False

    for dia in DIAS:
        libres_del_dia = []
        for inicio, fin in FRANJAS.items():
            if not existe_choque(horario, dia, inicio):
                libres_del_dia.append(f"{inicio}-{fin}")

        if libres_del_dia:
            hay_libres = True
            print(f"\n{dia}:")
            for franja in libres_del_dia:
                print(f"  - Libre: {franja}")

    if not hay_libres:
        print("No tienes bloques libres registrados en la semana.")        


