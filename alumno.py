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
    @classmethod
    def from_dict(cls, alumno_data: dict) -> 'Alumno':
        """
        Crea una instancia de Alumno a partir de un diccionario.
        :param alumno_data: Diccionario con los datos del alumno.
        :return: Un objeto Alumno.
        """
        return cls(
            alumno_data['nombres'],
            alumno_data['Apaterno'],
            alumno_data['Amaterno'],
            alumno_data['curp'],
            alumno_data['matricula']
        )
        
    @staticmethod
    def cargar_de_json(nombre_archivo: str, directorio: str = 'alumnos1') -> 'Alumno':
        """
        Carga los datos de un archivo JSON en un objeto Alumno.
        :param nombre_archivo: Nombre del archivo JSON a leer.
        :param directorio: Directorio donde se encuentra el archivo (por defecto 'alumnos1').
        :return: Un objeto Alumno con los datos cargados.
        """
        ruta_archivo = os.path.join(directorio, nombre_archivo)
        
        try:
            with open(ruta_archivo, 'r', encoding='utf-8') as file:
                json_data = json.load(file)
                contenedor = Alumno()  # Crear un contenedor vacío
                if isinstance(json_data, list):
                    for alumno_data in json_data:
                        alumno = Alumno.from_dict(alumno_data)
                        contenedor.agregar_dato(alumno)
                else:
                    return Alumno(json_data['nombres'], json_data['Apaterno'], 
                                json_data['Amaterno'], json_data['curp'], 
                                json_data['matricula'])  # Retornar un alumno individual
                return contenedor
        except (IOError, json.JSONDecodeError) as e:
            print(f"Error al leer el archivo: {e}")
            return Alumno()  # Retornar un contenedor vacío en caso de error
        
    def obtener_alumno_indice(self, index: int) -> 'Alumno':
        """
        Permite acceder a un alumno por su índice.
        :param index: Índice del alumno en el contenedor.
        :return: El alumno en la posición especificada.
        """
        if hasattr(self, 'datos') and 0 <= index < len(self.datos):
            return self.datos[index]
        else:
            raise IndexError("Índice fuera de rango")



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
    #print(f"\nTotal de alumnos en el contenedor: {len(contenedor)}")
    
    # Acceder mediante índice
    #print("\nAlumno en el índice 1:")
    #print(contenedor[1])
    
    # Guardar un alumno individual en JSON
    #guardar_en_json(alumno0, 'alumno0.json')
    
    # Guardar todos los alumnos en JSON
    #guardar_en_json(contenedor, 'alumnos.json')

    # Demostrar funcionalidad de alumno individual
    #print("\nInformación de alumno individual:")
    #print(alumno0)
    
    #print(contenedor)
    
    # Cargar los alumnos desde el JSON
    nuevo_contenedor = Alumno.cargar_de_json('alumnos.json')
    print("\nAlumnos cargados desde el archivo JSON:")
    print(nuevo_contenedor.to_dict())
    
    try:
        indice = 1
        print(f"\nAlumno en el indice {indice}:")    
        print(nuevo_contenedor.obtener_alumno_indice(indice))
    except IndexError as e:
        print(e)
    
