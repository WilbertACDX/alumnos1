import json
import os
from typing import Dict, Any
from ContenedorDatos import ContenedorDatos 

class Alumno(ContenedorDatos):
    """
    Representa a un alumno con sus datos personales o un contenedor de alumnos.
    """
    def __init__(self, *args):
        if len(args) == 0:
            super().__init__()
        elif len(args) == 5:
            self.nombres, self.Apaterno, self.Amaterno, self.curp, self.matricula = args
        else:
            raise ValueError("Necesitas 0 o 5 parámetros")

    def __str__(self) -> str:
        """
        Retorna una representación en cadena del alumno o del contenedor.
        """
        if hasattr(self, 'nombres'):
            return f"Alumno: {self.nombres} {self.Apaterno} {self.Amaterno} - CURP: {self.curp} - Matricula: {self.matricula}"
        elif hasattr(self, 'datos'):
            return '\n'.join([str(dato) for dato in self.datos])
        else:
            return "Contenedor vacío."

    def to_dict(self) -> Dict[str, Any]:
        """
        Convierte el objeto Alumno o el contenedor a un diccionario.
        """
        if hasattr(self, 'nombres'):
            return {
                "nombres": self.nombres,
                "Apaterno": self.Apaterno,
                "Amaterno": self.Amaterno,
                "curp": self.curp,
                "matricula": self.matricula
            }
        elif hasattr(self, 'datos'):
            return [alumno.to_dict() for alumno in self.datos]


def guardar_en_json(data: Alumno, nombre_archivo: str, directorio: str = 'alumnos1') -> None:
    """
    Guarda los datos en un archivo JSON.    
    :param data: Puede ser un Alumno individual o un contenedor de Alumnos.
    :param nombre_archivo: Nombre del archivo JSON a crear.
    :param directorio: Directorio donde se guardará el archivo (por defecto 'alumnos1').
    """
    os.makedirs(directorio, exist_ok=True)
    ruta_archivo = os.path.join(directorio, nombre_archivo)    
    
    try:
        with open(ruta_archivo, 'w', encoding='utf-8') as file:
            json_data = data.to_dict()
            if not hasattr(data, 'datos'):
                json_data = []  # Envolver en lista si es un alumno individual
            json.dump(json_data, file, indent=4, ensure_ascii=False)
        print(f"Los datos han sido guardados en '{ruta_archivo}'.")
    except IOError as e:
        print(f"Error al escribir el archivo: {e}")

if __name__ == '__main__':
    # Crear algunos alumnos
    alumno0 = Alumno("Wilbert Omar", "Acosta", "Barrera", "AOBW9980318HCLCRL08", "221700211")
    alumno1 = Alumno("Juan Carlos", "Fernandez", "Lopez", "JCFL992018HCLCRL01", "22170022")
    alumno2 = Alumno("Maria Fernanda", "Gomez", "Martinez", "MGFM992018HCLCRL02", "221700233")
    alumno3 = Alumno("José Eliaz", "Galarza", "Pedroza", "DJFKSLDMS1547845KD", "221740024")

    # Crear un contenedor y agregar los alumnos
    contenedor = Alumno()  # Inicializa un contenedor vacío
    contenedor.agregar_dato(alumno0)
    contenedor.agregar_dato(alumno1)
    contenedor.agregar_dato(alumno2)
    contenedor.agregar_dato(alumno3)

    #print("Antes de editar y eliminar:")
    #print(contenedor)
    
    # Editar un alumno
    #contenedor.editar_dato(1, nombres="Juan Carlos Editado", Apaterno="Fernandez Editado")
    #print("\nDespués de editar un alumno:")
    #print(contenedor)
    
    # Eliminar un alumno
    #contenedor.eliminar_dato(0)
    #print("\nDespués de eliminar un alumno:")
    #print(contenedor)
    
    # Longitud del contenedor
    print(f"\nTotal de alumnos en el contenedor: {len(contenedor)}")
    
    # Acceder mediante índice
    print("\nAlumno en el índice 1:")
    print(contenedor[1])
    
    # Guardar un alumno individual en JSON
    #guardar_en_json(alumno0, 'alumno0.json')
    
    # Guardar todos los alumnos en JSON
    guardar_en_json(contenedor, 'alumnos.json')

    # Demostrar funcionalidad de alumno individual
    #print("\nInformación de alumno individual:")
    #print(alumno0)
    
    #print(contenedor)
