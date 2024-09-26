import json
import os
from ContenedorDatos import ContenedorDatos 

class Alumno(ContenedorDatos):
    def __init__(self, *args):
        if len(args) == 0:
            super().__init__()
        elif len(args) == 5:
            self.nombres, self.Apaterno, self.Amaterno, self.curp, self.matricula = args
        else:
            raise ValueError("Necesitas 5 parámetros")

    def obtener_info(self):
        if hasattr(self, 'nombres'):
            return f"Alumno: {self.nombres}, Apellido Paterno: {self.Apaterno}, Apellido Materno: {self.Amaterno}, Curp: {self.curp}, Matricula: {self.matricula}"
        else:
            return "Este es un contenedor de datos."

    def __str__(self):
        if hasattr(self, 'nombres'):
            return f"Alumno: {self.nombres} {self.Apaterno} {self.Amaterno} - CURP: {self.curp} - Matricula: {self.matricula}"
        elif hasattr(self, 'datos'):
            return '\n'.join([str(dato) for dato in self.datos])
        else:
            return "Contenedor vacío."

    def to_dict(self):
        if hasattr(self, 'nombres'):
            # Es un solo alumno
            return {
                "nombres": self.nombres,
                "Apaterno": self.Apaterno,
                "Amaterno": self.Amaterno,
                "curp": self.curp,
                "matricula": self.matricula
            }
        elif hasattr(self, 'datos'):
            # Es un contenedor de alumnos
            return [alumno.to_dict() for alumno in self.datos if isinstance(alumno, Alumno)]
        else:
            raise ValueError("El objeto no tiene atributos válidos para convertir a diccionario.")

def guardar_en_json(data, nombre_archivo):
    ruta_archivo = os.path.join('alumnos1', nombre_archivo)    
    with open(ruta_archivo, 'w') as file:
        if isinstance(data, Alumno):
            # Si es un solo objeto Alumno
            alumnos_data = [data.to_dict()]
        elif isinstance(data, ContenedorDatos):
            # Si es un contenedor de datos
            alumnos_data = data.to_dict()  # Cambia aquí para usar el to_dict del contenedor
        else:
            raise ValueError("El argumento 'data' debe ser un objeto Alumno o una instancia de ContenedorDatos.")
        
        json.dump(alumnos_data, file, indent=4)

if __name__ == '__main__':
    alumno0 = Alumno("Wilbert Omar", "Acosta", "Barrera", "AOBW9980318HCLCRL08", "22170021")
    alumno1 = Alumno("Juan Carlos", "Fernandez", "Lopez", "JCFL992018HCLCRL01", "22170022")
    alumno2 = Alumno("Maria Fernanda", "Gomez", "Martinez", "MGFM992018HCLCRL02", "22170023")

    arreglo = Alumno()  # Esto inicializa un contenedor de datos

    arreglo.agregar_dato(alumno0)
    arreglo.agregar_dato(alumno1)
    arreglo.agregar_dato(alumno2)

    print("Antes de editar y eliminar:")
    print(arreglo)
    
    # Editar un alumno
    arreglo.editar_dato(1, nombres="Juan Carlos Editado", Apaterno="Fernandez Editado")
    print("\nDespués de editar un alumno:")
    print(arreglo)
    
    # Eliminar un alumno
   # arreglo.eliminar_dato(0)
   # print("\nDespués de eliminar un alumno:")
   # print(arreglo)
    
    # Longitud del arreglo
    print(f"Total de datos en el contenedor: {len(arreglo)}")
    
    # Ingresar mediante índice
    print(arreglo[1])
    
    guardar_en_json(alumno0, 'alumno0.json')
    print("\nLos datos han sido guardados en 'alumno0.json'.")
    
    guardar_en_json(arreglo, 'alumnos.json')
    print("\nLos datos han sido guardados en 'alumnos.json'.")
