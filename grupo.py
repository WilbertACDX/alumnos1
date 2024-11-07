import json
import os
from typing import Dict, Any
from ContenedorDatos import ContenedorDatos
from alumno import Alumno

class Grupo(ContenedorDatos):
    def __init__(self, *args):
        if len(args) == 0:
            super().__init__()
        elif len(args) == 2:
            self.grado, self.seccion = args
            self.alumnos = Alumno()
        else:
            raise ValueError("Necesitas 2 parámetros")

    def agregar_alumno(self, alumno):
        self.alumnos.agregar_dato(alumno)   
    
    def __str__(self):
        if hasattr(self, 'grado'):
            alumnos_info = "\n".join(str(alumno) for alumno in self.alumnos.datos)
            return f"Grupo: {self.grado} {self.seccion}\nAlumnos:\n{alumnos_info}"
        else:
            return "Contenedor de grupos:\n" + "\n".join(str(grupo) for grupo in self)
        
    def to_dict(self) -> Dict[str, Any]:
        if hasattr(self, 'grado'):
            return {
                'grado': self.grado,
                'seccion': self.seccion,
                'alumnos': [alumno.to_dict() for alumno in self.alumnos.datos]
            }
        elif hasattr(self, 'datos'):
            return [grupo.to_dict() for grupo in self.datos]
        else:
            return {}
        
    @classmethod
    def from_dict(cls, grupo_data: dict) -> 'Grupo':
        """
        Crea una instancia de Alumno a partir de un diccionario.
        :param alumno_data: Diccionario con los datos del alumno.
        :return: Un objeto Alumno.
        """
        return cls(
            grupo_data['grado'],
            grupo_data['seccion'],
        )
        
    @staticmethod
    def cargar_de_json(nombre_archivo: str, directorio: str = 'alumnos1') -> 'Grupo':
        """
        Carga los datos de un archivo JSON en un objeto Alumno.
        :param nombre_archivo: Nombre del archivo JSON a leer.
        :param directorio: Directorio donde se encuentra el archivo (por defecto 'alumnos1').
        :return: Un objeto Grupo con los datos cargados.
        """
        ruta_archivo = os.path.join(directorio, nombre_archivo)
        
        try:
            with open(ruta_archivo, 'r', encoding='utf-8') as file:
                json_data = json.load(file)
                contenedor = Grupo()  # Crear un contenedor vacío
                if isinstance(json_data, list):
                    for grupo_data in json_data:
                        grupo = Grupo.from_dict(grupo_data)
                        for alumno_data in grupo_data.get('alumnos', []):
                                alumno = Alumno.from_dict(alumno_data)
                                grupo.agregar_alumno(alumno)
                        contenedor.agregar_dato(grupo)
                else:
                    return Grupo(grupo_data['grado'], grupo_data['seccion'])
                
                return contenedor
        except (IOError, json.JSONDecodeError) as e:
            print(f"Error al leer el archivo: {e}")
            return Grupo()  # Retornar un contenedor vacío en caso de error
        
    def obtener_grupo_indice(self, index: int) -> 'Grupo':
        """
        Permite acceder a un alumno por su índice.
        :param index: Índice del alumno en el contenedor.
        :return: El Grupo en la posición especificada.
        """
        if hasattr(self, 'datos') and 0 <= index < len(self.datos):
            return self.datos[index]
        else:
            raise IndexError("Índice fuera de rango")

def guardar_en_json(data: Grupo, nombre_archivo: str, directorio: str = 'alumnos1') -> None:
    # Crear el directorio si no existe
    os.makedirs(directorio, exist_ok=True)

    # Definir la ruta completa del archivo
    ruta_archivo = os.path.join(directorio, nombre_archivo)
    
    # Validar que el objeto a guardar sea un arreglo (contenedor de grupos)
    if not (hasattr(data, 'datos') and isinstance(data.datos, list) and len(data.datos) > 0):
        print("Error: Solo se puede guardar un contenedor con varios grupos.")
        return 
    
    try:
        # Convertir los datos a un diccionario
        json_data = data.to_dict()
        
        # Guardar los datos en formato JSON si es un arreglo válido
        with open(ruta_archivo, 'w', encoding='utf-8') as file:
            json.dump(json_data, file, indent=4, ensure_ascii=False)
        print(f"Los datos han sido guardados en '{ruta_archivo}'.")
    except IOError as e:
        print(f"Error al escribir el archivo: {e}")
     


if __name__ == '__main__':
    
    #grupo1 = Grupo(6, "A")
   # grupo2 = Grupo(6, "B")
    
    #alumno0 = Alumno("Wilbert Omar", "Acosta", "Barrera", "AOBW9980318HCLCRL08", "22170021")
    #alumno1 = Alumno("Juan Carlos", "Fernandez", "Lopez", "JCFL992018HCLCRL01", "22170022")
    #alumno2 = Alumno("Maria Fernanda", "Gomez", "Martinez", "MGFM992018HCLCRL02", "22170023")
    
    #alumno3 = Alumno("José Eliaz", "Galarza", "Pedroza", "DJFKSLDMS1547845KD", "221740024")
    #alumno4 = Alumno("Felix Gael", "Saldivar", "Martinez", "KDFGFDG541515_FG", "2217400255")
    #alumno5 = Alumno("Kevin Alexis", "Yescas", "Felix", "YFKA544541151sd", "2217400266")

    #grupo1.agregar_alumno(alumno0)
    #grupo1.agregar_alumno(alumno1)
    #grupo1.agregar_alumno(alumno2)
    
    #grupo2.agregar_alumno(alumno3)
    #grupo2.agregar_alumno(alumno4)
    #grupo2.agregar_alumno(alumno5)

    #contenerGrupo = Grupo()
    
    #contenerGrupo.agregar_dato(grupo1)
    #contenerGrupo.agregar_dato(grupo2)

    #print("Estado inicial del grupo:")
    #print(grupo1)

    #print(f"\nTotal de alumnos en el grupo: {len(grupo1.alumnos.datos)}\n")
       
    #print("\nContenedor")
    #print(contenerGrupo)
    
    #guardar_en_json(contenerGrupo, 'grupos.json')
    
    #Cargar grupos desde json
    grupos = Grupo.cargar_de_json('grupos.json')
    print("\nGrupos cargados desde el archivo JSON:")
    print(grupos.to_dict())

    #cargar un solo grupo
    
    try:
        indice = 1
        print(f"\nAlumno en el indice {indice}:")    
        print(grupos.obtener_grupo_indice(indice))
    except IndexError as e:
        print(e)