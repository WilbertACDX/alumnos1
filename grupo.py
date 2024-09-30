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
    grupo1 = Grupo(6, "A")
    grupo2 = Grupo(6, "B")
    
    alumno0 = Alumno("Wilbert Omar", "Acosta", "Barrera", "AOBW9980318HCLCRL08", "22170021")
    alumno1 = Alumno("Juan Carlos", "Fernandez", "Lopez", "JCFL992018HCLCRL01", "22170022")
    alumno2 = Alumno("Maria Fernanda", "Gomez", "Martinez", "MGFM992018HCLCRL02", "22170023")
    
    alumno3 = Alumno("José Eliaz", "Galarza", "Pedroza", "DJFKSLDMS1547845KD", "221740024")
    alumno4 = Alumno("Felix Gael", "Saldivar", "Martinez", "KDFGFDG541515_FG", "221740025")
    alumno5 = Alumno("Kevin Alexis", "Yescas", "Felix", "YFKA544541151sd", "2217400266")

    grupo1.agregar_alumno(alumno0)
    grupo1.agregar_alumno(alumno1)
    grupo1.agregar_alumno(alumno2)
    
    grupo2.agregar_alumno(alumno3)
    grupo2.agregar_alumno(alumno4)
    grupo2.agregar_alumno(alumno5)

    contenerGrupo = Grupo()
    
    contenerGrupo.agregar_dato(grupo1)
    contenerGrupo.agregar_dato(grupo2)

    print("Estado inicial del grupo:")
    print(grupo1)

    print(f"Total de alumnos en el grupo: {len(grupo1.alumnos.datos)}")
       
    print("\nContenedor")
    print(contenerGrupo)
    
    guardar_en_json(contenerGrupo, 'grupos.json')

