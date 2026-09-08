"""Punto de entrada del Generador de Horarios para Estudiantes."""

import json

import funciones


def cargar_horario():
    """Lee los eventos guardados. Si no existe el archivo, devuelve una lista vacía."""
    try:
        with open("horario.json", "r", encoding="utf-8") as archivo:
            horario = json.load(archivo)
            if isinstance(horario, list):
                return horario

            print("horario.json debe contener una lista de actividades. Se iniciará vacío.")
            return []
    except FileNotFoundError:
        print("No existe horario.json. Se iniciará un horario vacío.")
        return []
    except json.JSONDecodeError:
        print("horario.json no tiene un formato válido. Se iniciará un horario vacío.")
        return []


def mostrar_menu():
    print("\n================================================")
    print("       GENERADOR DE HORARIOS PARA ESTUDIANTES")
    print("================================================")
    print("Organiza tus materias y actividades de lunes a viernes.")
    print("\n¿Qué deseas hacer?")
    print("  1. Registrar una materia o actividad")
    print("  2. Ver mi horario semanal")
    print("  3. Modificar una actividad")
    print("  4. Eliminar una actividad")
    print("  5. Generar reporte semanal")
    print("  6. Salir")
    print("------------------------------------------------")


def main():
    horario = cargar_horario()
    continuar = True

    while continuar:
        try:
            mostrar_menu()
            opcion = input("Escribe el número de una opción (1 a 6): ").strip()

            if opcion == "1":
                funciones.registrar_evento(horario)
            elif opcion == "2":
                funciones.ver_horario_semanal(horario)
            elif opcion == "3":
                funciones.modificar_evento(horario)
            elif opcion == "4":
                funciones.eliminar_evento(horario)
            elif opcion == "5":
                funciones.generar_reporte(horario)
            elif opcion == "6":
                respuesta = input("¿Está seguro de que desea salir? (Y/N): ").strip().lower()
                if respuesta == "y":
                    continuar = False
                    print("Gracias por usar el generador de horarios. ¡Hasta luego!")
                elif respuesta == "n" or respuesta == "":
                    print("Regresando al menú.")
                else:
                    print("Respuesta no válida. Regresando al menú.")
            else:
                print("Opción no válida. Solo puede escribir un número del 1 al 6.")
        except KeyboardInterrupt:
            respuesta = input("\n¿Está seguro de que desea salir? (Y/N): ").strip().lower()
            if respuesta == "y":
                continuar = False
                print("Gracias por usar el generador de horarios. ¡Hasta luego!")
            elif respuesta == "n" or respuesta == "":
                print("Regresando al menú.")
            else:
                print("Respuesta no válida. Regresando al menú.")


if __name__ == "__main__":
    main()
