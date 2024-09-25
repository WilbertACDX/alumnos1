import json
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
    
    def agregar_grupo(self, grupo):
       self.agregar_dato(grupo)

    
    def __str__(self):
        if hasattr(self, 'grado'):
            alumnos_info = "\n".join(str(alumno) for alumno in self.alumnos.datos)
            return f"Grupo: {self.grado} {self.seccion}\nAlumnos:\n{alumnos_info}"
        else:
            return "Contenedor de grupos:\n" + "\n".join(str(grupo) for grupo in self)
        
    def to_dict(self):
        return {
            'grado': self.grado,
            'seccion': self.seccion,
            'alumnos': [alumno.to_dict() for alumno in self.alumnos.datos]
        }

def guardar_en_json(contenedor_grupos, nombre_archivo):
    with open(nombre_archivo, 'w') as file:
        grupos_data = [grupo.to_dict() for grupo in contenedor_grupos.datos]
        json.dump(grupos_data, file, indent=4)


if __name__ == '__main__':
    grupo1 = Grupo(6, "A")
    grupo2 = Grupo(6, "B")
    
    
    alumno0 = Alumno("Wilbert Omar", "Acosta", "Barrera", "AOBW9980318HCLCRL08", "22170021")
    alumno1 = Alumno("Juan Carlos", "Fernandez", "Lopez", "JCFL992018HCLCRL01", "22170022")
    alumno2 = Alumno("Maria Fernanda", "Gomez", "Martinez", "MGFM992018HCLCRL02", "22170023")
    
    alumno3 = Alumno ("José Eliaz", "Galarza", "Pedroza", "DJFKSLDMS1547845KD","221740024")
    alumno4 = Alumno ("Felix Gael", "Saldivar", "Martinez", "KDFGFDG541515_FG","221740025")
    alumno5 = Alumno ("Kevin Alexis", "Yescas", "Felix", "YFKA544541151sd","2217400268")

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
    print("\nLos datos han sido guardados en 'grupos.json'.")
