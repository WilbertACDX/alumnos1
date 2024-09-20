from ContenedorDatos import ContenedorDatos
from grupo import Grupo
from alumno import Alumno

class Carrera(ContenedorDatos):
    def __init__(self, *args):
        if len(args) == 0:
            super().__init__()
        elif len(args) == 2:
            self.nombre, self.clave = args
            self.grupos = Grupo()
            self.alumnos = Alumno()
        else:
            raise ValueError("Necesitas 2 parámetros")

    def agregar_alumno(self, alumno):
        self.alumnos.agregar_dato(alumno)
    
    def agregar_grupo(self, grupo):
        self.grupos.agregar_dato(grupo)
        
    def agregar_carrera (self, carrera):
        self.agregar_dato(carrera)


    def __str__(self):
        if hasattr(self, 'clave'):
            grupo_info = "\n".join(str(grupo) for grupo in self.grupos.datos)
            return f"Carrera: {self.clave} {self.nombre} \n{grupo_info}"
        else:
            # Aquí puedes personalizar cómo se representa un contenedor sin grupos
            return "Contenedor de carreras:\n" + "\n".join(str(carrera) for carrera in self)
    
if __name__ == "__main__":
   
    alumno0 = Alumno("Wilbert Omar", "Acosta", "Barrera", "AOBW9980318HCLCRL08", "22170021")
    alumno1 = Alumno("Juan Carlos", "Fernandez", "Lopez", "JCFL992018HCLCRL01", "22170022")
    alumno2 = Alumno("Maria Fernanda", "Gomez", "Martinez", "MGFM992018HCLCRL02", "22170023")
    
    alumno3 = Alumno ("José Eliaz", "Galarza", "Pedroza", "DJFKSLDMS1547845KD","221740024")
    alumno4 = Alumno ("Felix Gael", "Saldivar", "Martinez", "KDFGFDG541515_FG","221740025")
    alumno5 = Alumno ("Kevin Alexis", "Yescas", "Felix", "YFKA544541151sd","221740026")


    
    # Crear los grupos
    grupo_7a = Grupo("7", "A")
    grupo_7b = Grupo("7", "B")
    
    grupo_5a = Grupo("5", "A")
    grupo_5b = Grupo("5", "A")    
    
    grupo_7a.agregar_alumno(alumno0)
    grupo_7a.agregar_alumno(alumno1)
    
    grupo_7b.agregar_alumno(alumno2)    
    grupo_7b.agregar_alumno(alumno3)
    
    grupo_5a.agregar_alumno(alumno4)
    
    grupo_5b.agregar_alumno(alumno5)


    # Crear la carrera y agregar los grupos
    carrera1 = Carrera("Desarrollo de Software", 210)
    carrera2 = Carrera("Administración", 211)   
    
    carrera1.agregar_grupo(grupo_7a)
    carrera1.agregar_grupo(grupo_7b)
    carrera2.agregar_grupo(grupo_5a)
    carrera2.agregar_grupo(grupo_5b)
    contenedor = Carrera()
    
    contenedor.agregar_dato(carrera1)
    contenedor.agregar_dato(carrera2)
    
    print(contenedor)

    
        





