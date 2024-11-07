from ContenedorDatos import ContenedorDatos
from grupo import Grupo
from alumno import Alumno
import json
import os

class Carrera(ContenedorDatos):
    def __init__(self, *args):
        if len(args) == 0:
            super().__init__()
        elif len(args) == 2:
            self.nombre, self.clave = args
            self.grupos = Grupo()  # Aquí se manejarán los grupos
        else:
            raise ValueError("Necesitas 0 o 2 parámetros")

    def agregar_grupo(self, grupo):
        self.grupos.agregar_dato(grupo)

    def __str__(self):
        if hasattr(self, 'clave'):
            grupo_info = "\n".join(str(grupo) for grupo in self.grupos.datos)
            return f"Carrera: {self.clave} {self.nombre} \nGrupos:\n{grupo_info}"
        else:
            # Para contenedores de varias carreras
            return "Contenedor de carreras:\n" + "\n".join(str(carrera) for carrera in self)

    def to_dict(self):
        if hasattr(self, 'clave'):
            # Convertir la carrera y sus grupos a diccionario
            return {
                'nombre': self.nombre,
                'clave': self.clave,
                'grupos': [grupo.to_dict() for grupo in self.grupos.datos]
            }
        elif hasattr(self, 'datos'):
            # Si es un contenedor de carreras
            return [carrera.to_dict() for carrera in self.datos]
        
    @classmethod
    def from_dict(cls, carrera_data: dict) -> 'Carrera':
        """
        Crea una instancia de Alumno a partir de un diccionario.
        :param alumno_data: Diccionario con los datos del alumno.
        :return: Un objeto Alumno.
        """
        return cls(
            carrera_data['nombre'],
            carrera_data['clave'],
        )
        
    @staticmethod
    def cargar_de_json(nombre_archivo: str, directorio: str = 'alumnos1') -> 'Carrera':
        """
        Carga los datos de un archivo JSON en un objeto Alumno.
        :param nombre_archivo: Nombre del archivo JSON a leer.
        :param directorio: Directorio donde se encuentra el archivo (por defecto 'alumnos1').
        :return: Un objeto Carrera con los datos cargados.
        """
        ruta_archivo = os.path.join(directorio, nombre_archivo)
        
        try:
            with open(ruta_archivo, 'r', encoding='utf-8') as file:
                json_data = json.load(file)
                contenedor = Carrera()  # Crear un contenedor vacío
                if isinstance(json_data, list):
                    for carrera_data in json_data:
                        carrera = Carrera.from_dict(carrera_data)
                        for grupo_data in carrera_data.get('grupos', []):
                                grupo = Grupo.from_dict(grupo_data)
                                for alumno_data in grupo_data.get('alumnos', []):
                                    alumno = Alumno.from_dict(alumno_data)
                                    grupo.agregar_alumno(alumno)
                                carrera.agregar_grupo(grupo)
                        contenedor.agregar_dato(carrera)
                else:
                    return Carrera(carrera_data['nombre'], carrera_data['clave'])
                
                return contenedor
        except (IOError, json.JSONDecodeError) as e:
            print(f"Error al leer el archivo: {e}")
            return Carrera()  # Retornar un contenedor vacío en caso de error
        
    def obtener_carrera_indice(self, index: int) -> 'Carrera':
        """
        Permite acceder a un alumno por su índice.
        :param index: Índice del alumno en el contenedor.
        :return: El Carrera en la posición especificada.
        """
        if hasattr(self, 'datos') and 0 <= index < len(self.datos):
            return self.datos[index]
        else:
            raise IndexError("Índice fuera de rango")
        
def guardar_en_json(data: Carrera, nombre_archivo: str, directorio: str = 'alumnos1') -> None:
    # Crear el directorio si no existe
    os.makedirs(directorio, exist_ok=True)

    # Definir la ruta completa del archivo
    ruta_archivo = os.path.join(directorio, nombre_archivo)
    
    # Validar que el objeto a guardar sea un contenedor de carreras
    if not (hasattr(data, 'datos') and isinstance(data.datos, list) and len(data.datos) > 0):
        print("Error: Solo se puede guardar un contenedor con varias carreras.")
        return
    
    try:
        # Convertir los datos a un diccionario
        json_data = data.to_dict()

        # Guardar los datos en formato JSON si es un contenedor válido
        with open(ruta_archivo, 'w', encoding='utf-8') as file:
            json.dump(json_data, file, indent=4, ensure_ascii=False)
        print(f"Los datos han sido guardados en '{ruta_archivo}'.")
    except IOError as e:
        print(f"Error al escribir el archivo: {e}")

    
if __name__ == "__main__":
   
    # Crear alumnos
   # alumno0 = Alumno("Wilbert Omar", "Acosta", "Barrera", "AOBW9980318HCLCRL08", "22170021")
    #alumno1 = Alumno("Juan Carlos", "Fernandez", "Lopez", "JCFL992018HCLCRL01", "22170022")
    #alumno2 = Alumno("Maria Fernanda", "Gomez", "Martinez", "MGFM992018HCLCRL02", "22170023")
    #alumno3 = Alumno ("José Eliaz", "Galarza", "Pedroza", "DJFKSLDMS1547845KD","221740024")
    #alumno4 = Alumno ("Felix Gael", "Saldivar", "Martinez", "KDFGFDG541515_FG","221740025")
    #alumno5 = Alumno ("Kevin Alexis", "Yescas", "Felix", "YFKA544541151sd","221740026")

    # Crear grupos
    #grupo_7a = Grupo("7", "A")
    #grupo_7b = Grupo("7", "B")
    #grupo_5a = Grupo("5", "A")
    #grupo_5b = Grupo("5", "B")    
    
    # Agregar alumnos a los grupos
    #grupo_7a.agregar_alumno(alumno0)
    #grupo_7a.agregar_alumno(alumno1)
    
    #grupo_7b.agregar_alumno(alumno2)
    #grupo_7b.agregar_alumno(alumno3)
    
    #grupo_5a.agregar_alumno(alumno4)
    #grupo_5b.agregar_alumno(alumno5)

    # Crear carreras y agregar los grupos
    #carrera1 = Carrera("Desarrollo de Software", 210)
    #carrera2 = Carrera("Administración", 211)   
    
    #carrera1.agregar_grupo(grupo_7a)
    #carrera1.agregar_grupo(grupo_7b)
    
    #carrera2.agregar_grupo(grupo_5a)
    #carrera2.agregar_grupo(grupo_5b)

    # Crear contenedor de carreras
    #contenedor = Carrera()
    #contenedor.agregar_dato(carrera1)
    #contenedor.agregar_dato(carrera2)
    
    # Mostrar el contenedor de carreras
    #print(contenedor)

    # Guardar en JSON
    #guardar_en_json(contenedor, 'carreras.json')
    
    
    carreras = Carrera.cargar_de_json('carreras.json')
    print("\nCarreras cargados desde el archivo JSON:")
    print(carreras.to_dict())

    
    try:
        indice = 1
        print(f"\nCarrera en el indice {indice}:")    
        print(carreras.obtener_carrera_indice(indice))
    except IndexError as e:
        print(e)

