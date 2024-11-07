from alumno import Alumno  # Importa la clase Alumno
from alumno import guardar_en_json  # Importa la función para guardar en JSON
from mongoDBConnection import MongoDBConnection


class GestionarAlumnos:
    def __init__(self, contenedor=None, db_uri=None, db_name="UTT"):
        self.archivo_cargado = None  # Atributo para almacenar el nombre del archivo
        self.isSave=False
        self.mongo_conn = MongoDBConnection(db_uri, db_name) if db_uri else None  # Conexión a MongoDB
        if contenedor is None:
            self.contenedor = Alumno()  # Crear un contenedor vacío
            print("Se ha creado un contenedor vacío.")
        elif isinstance(contenedor, str):
            try:
                self.contenedor = Alumno.cargar_de_json(contenedor)
                self.archivo_cargado = contenedor  # Guardar el nombre del archivo
                print(f"Alumnos cargados desde {contenedor}")
                self.isSave=True
            except FileNotFoundError:
                print(f"No se encontró el archivo {contenedor}. Se utilizará un contenedor vacío.")
                self.contenedor = Alumno()  # Inicializar un contenedor vacío
        elif isinstance(contenedor, Alumno):
            self.contenedor = contenedor
            print("Contenedor de Alumnos proporcionado directamente.")
        else:
            print("Tipo de contenedor no válido. Se utilizará un contenedor vacío.")
            self.contenedor = Alumno()





    def mostrar_menu(self):
        """
        Muestra el menú principal y maneja la selección del usuario.
        """
        while True:
            print("\n--- Menú Principal---")
            print("1. Ver todos los alumnos")
            print("2. Agregar un alumno")
            print("3. Editar un alumno")
            print("4. Eliminar un alumno")
            print("5. Salir")
            
            opcion = input("Selecciona una opción: ")
            
            if opcion == "1":
                self.mostrar_alumnos()
            elif opcion == "2":
                self.agregar_alumno()
            elif opcion == "3":
                self.editar_alumno()
            elif opcion == "4":
                self.eliminar_alumno()
            elif opcion == "5":

                print("Saliendo...")
                break
            else:
                print("Opción no válida. Intenta de nuevo.")

    def mostrar_alumnos(self):
        """
        Muestra todos los alumnos en el contenedor.
        """
        print("\n--- Lista de Alumnos ---")
        if hasattr(self.contenedor, 'datos') and len(self.contenedor.datos) > 0:
            for i, alumno in enumerate(self.contenedor.datos, start=1):
                print(f"{i}. {alumno}")
        else:
            print("No hay alumnos en el contenedor.")
    
        input("Presiona Enter para continuar...")

    def agregar_alumno(self):
        """
        Agrega un nuevo alumno al contenedor.
        """
        print("\n--- Agregar Alumno ---")
        nombres = input("Nombres: ")
        Apaterno = input("Apellido Paterno: ")
        Amaterno = input("Apellido Materno: ")
        curp = input("CURP: ")
        matricula = input("Matrícula: ")
        
        nuevo_alumno = Alumno(nombres, Apaterno, Amaterno, curp, matricula)
        self.contenedor.agregar_dato(nuevo_alumno)
        print(f"Alumno {nombres} agregado correctamente.")
        if self.isSave:
            self.guardar_en_json()
        
        if self.isSave and self.mongo_conn:
            alumno_dict = nuevo_alumno.to_dict()  # Convertir a diccionario
            self.mongo_conn.insert_documents("Alumnos", [alumno_dict])
    
    def editar_alumno(self):
        """
        Edita los datos de un alumno existente.
        """
        if len(self.contenedor) == 0:
            print("No hay alumnos para editar.")
            input("Presiona Enter para continuar...")
            return
        
        self.mostrar_alumnos()

        indice = self.solicitar_indice()

        if indice is not None:
            alumno = self.contenedor.obtener_alumno_indice(indice)
            print(f"Editando a {alumno.nombres} {alumno.Apaterno}")
            
            matricula_original = alumno.matricula
            
            nuevos_nombres = input(f"Nombres [{alumno.nombres}]: ") or alumno.nombres
            nuevo_Apaterno = input(f"Apellido Paterno [{alumno.Apaterno}]: ") or alumno.Apaterno
            nuevo_Amaterno = input(f"Apellido Materno [{alumno.Amaterno}]: ") or alumno.Amaterno
            nuevo_curp = input(f"CURP [{alumno.curp}]: ") or alumno.curp
            nueva_matricula = input(f"Matrícula [{alumno.matricula}]: ") or alumno.matricula
            
            self.contenedor.editar_dato(indice, nombres=nuevos_nombres, Apaterno=nuevo_Apaterno, 
                                        Amaterno=nuevo_Amaterno, curp=nuevo_curp, matricula=nueva_matricula)
            print("Alumno editado correctamente.")
        input("Presiona Enter para continuar...")
        if self.isSave:
            self.guardar_en_json()

            if self.mongo_conn:
                alumno_dict = alumno.to_dict()  # Diccionario actualizado del alumno
                filter_criteria = {"matricula": matricula_original}  # Filtra por matrícula o algún identificador único
                self.mongo_conn.update_document("Alumnos", filter_criteria, alumno_dict)
                
                print("Datos del alumno actualizados en MongoDB Atlas.")

        
    def eliminar_alumno(self):
        """
        Elimina un alumno del contenedor.
        """
        if len(self.contenedor) == 0:
            print("No hay alumnos para editar.")
            input("Presiona Enter para continuar...")
            return
        
        self.mostrar_alumnos()

        indice = self.solicitar_indice()

        if indice is not None:
            alumno = self.contenedor.datos[indice]  # Acceder al alumno usando el índice
            self.contenedor.eliminar_dato(indice)
            alumno_original = alumno.matricula
            print("Alumno eliminado correctamente.")
            
        if self.isSave:
            self.guardar_en_json()
        
        # Guardar cambios en MongoDB si es necesario
            if self.mongo_conn:
                alumno_dict = alumno.to_dict()  # Convertir el alumno eliminado a diccionario
                filter_criteria = {"matricula": alumno_original}  # Usar la matrícula como filtro
                self.mongo_conn.delete_document("Alumnos", filter_criteria)  # Eliminar en MongoDB
                print("Datos del alumno eliminados de MongoDB Atlas.")
                    

        
    def guardar_en_json(self):
        if self.archivo_cargado:
            nombre_archivo = self.archivo_cargado
            guardar_en_json(self.contenedor, nombre_archivo)
            print(f"Datos guardados en {nombre_archivo}.")
            

        else:
            print("Saliendo...")
            
    


    def solicitar_indice(self):
        """
        Solicita al usuario que ingrese un índice válido (entero positivo).
        """
        try:
            indice = int(input("\nSelecciona el número del alumno: ")) - 1
            if indice < 0 or indice >= len(self.contenedor):
                print("Índice fuera de rango.")
                return None
            return indice
        except ValueError:
            print("Por favor, ingresa un número entero válido.")
            return None


if __name__ == '__main__':
    contenedor = "alumnos.json"
    uri = "mongodb+srv://ZkOHDR5Y8tQq2C52:ZkOHDR5Y8tQq2C52@cluster0.sztvu.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    interfaz = GestionarAlumnos(contenedor, db_uri=uri)
    interfaz.mostrar_menu()
