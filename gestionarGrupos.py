from grupo import Grupo, guardar_en_json
from gestionarAlumnos import GestionarAlumnos
from mongoDBConnection import MongoDBConnection

class GestionarGrupos:
    def __init__(self, contenedor = None, db_uri=None, db_name="UTT"):
        self.archivo_cargado = None  # Atributo para almacenar el nombre del archivo
        self.isSave=True
        self.mongo_conn = MongoDBConnection(db_uri, db_name) if db_uri else None  # Conexión a MongoDB
        if contenedor is None:
            self.contenedor = Grupo()  # Crear un contenedor vacío
            print("Se ha creado un contenedor vacío.")
        elif isinstance(contenedor, str):
            try:
                self.contenedor = Grupo.cargar_de_json(contenedor)
                self.archivo_cargado = contenedor  # Guardar el nombre del archivo
                print(f"Alumnos cargados desde {contenedor}")
            except FileNotFoundError:
                print(f"No se encontró el archivo {contenedor}. Se utilizará un contenedor vacío.")
                self.contenedor = Grupo()  # Inicializar un contenedor vacío
        elif isinstance(contenedor, Grupo):
            self.contenedor = contenedor
            print("Contenedor de Alumnos proporcionado directamente.")
        else:
            print("Tipo de contenedor no válido. Se utilizará un contenedor vacío.")
            self.contenedor = Grupo()

    def mostrar_menu(self):
        while True:
            print("\n--- Menú de Grupos ---")
            print("1. Crear un grupo")
            print("2. Ver grupos")
            print("3. Eliminar Grupo")
            print("4. Editar Grupo")
            print("5. Agregar alumno a un grupo")
            print("6. Salir")
            
            opcion = input("Selecciona una opción: ")
            
            if opcion == "1":
                self.crear_grupo()
            elif opcion == "2":
                self.ver_grupos()
            elif opcion == "3":
                self.eliminar_grupo()
            elif opcion == "4":
                self.editar_grupo()
            elif opcion == "5":
                self.agregar_alumno_a_grupo()
            elif opcion == "6":
                print("Saliendo...")
                break
            else:
                print("Opción no válida. Intenta de nuevo.")

    def crear_grupo(self):
        grado = input("Grado del grupo: ")
        seccion = input("Sección del grupo: ")
        
        nuevo_grupo = Grupo(grado, seccion)
        self.contenedor.agregar_dato(nuevo_grupo)  # Agrega el nuevo grupo al contenedor principal
        
        print(f"Grupo '{grado} {seccion}' creado correctamente.")
        
            
        if self.isSave or self.mongo_conn:
            grupo_dict = nuevo_grupo.to_dict()  # Convertir a diccionario
            self.mongo_conn.insert_documents("Grupos", [grupo_dict])
            
        if self.isSave:
            self.guardar_en_json()
            
        input("Presiona Enter para continuar...")


    def ver_grupos(self):
        if not self.contenedor.datos:
            print("No hay grupos disponibles.")
        else:
            for i, grupo in enumerate(self.contenedor.datos, start=1):
                print(f"{i}. {grupo}")
        input("Presiona Enter para continuar...")
                
    def eliminar_grupo(self):
        """
        Elimina un grupo del contenedor.
        """
        if len(self.contenedor) == 0:
            print("No hay grupos para editar.")
            input("Presiona Enter para continuar...")
            return
    
        self.ver_grupos()

        indice = self.solicitar_indice()

        if indice is not None:
            grupo = self.contenedor.datos[indice]
            self.contenedor.eliminar_dato(indice)
            grupo_original = grupo.grado
            
            print("Grupo eliminado correctamente.")
            
            if self.isSave:
                self.guardar_en_json()
        
        # Guardar cambios en MongoDB si es necesario
                if self.mongo_conn:
                    filter_criteria = {"grado": grupo_original}
                    self.mongo_conn.delete_document("Grupos", filter_criteria)  # Eliminar en MongoDB
                    
                    print("Datos del grupo eliminados de MongoDB Atlas.")

                    

        
        
    def editar_grupo(self):
        """
        Edita los datos de un alumno existente.
        """
        if len(self.contenedor) == 0:
            print("No hay Grupos para editar.")
            input("Presiona Enter para continuar...")
            return
        
        self.ver_grupos()

        indice = self.solicitar_indice()

        if indice is not None:
            grupo = self.contenedor.obtener_grupo_indice(indice)
            print(f"Editando a {grupo.grado} {grupo.seccion}")
            

            
            nuevo_grado = input(f"Grado [{grupo.grado}]: ") or grupo.grado
            nueva_seccion = input(f"Seccion [{grupo.seccion}]: ") or grupo.seccion
            
            self.contenedor.editar_dato(indice, grado=nuevo_grado, seccion=nueva_seccion)
            print("Grupo editado correctamente.")
        input("Presiona Enter para continuar...")
        if self.isSave:
            self.guardar_en_json()

            if self.mongo_conn:
                grupo_dict = grupo.to_dict()  # Diccionario actualizado del alumno
                filter_criteria = {"grado": grupo.grado}
                self.mongo_conn.update_document("Grupos", filter_criteria, grupo_dict)

                print("Datos del alumno actualizados en MongoDB Atlas.")


    def agregar_alumno_a_grupo(self):
        if not self.contenedor.datos:
            print("No hay grupos disponibles. Crea un grupo primero.")
            return

        self.ver_grupos()
        indice_grupo = int(input("Selecciona el número del grupo: ")) - 1

        if 0 <= indice_grupo < len(self.contenedor.datos):
            grupo = self.contenedor.datos[indice_grupo]
            gestionar_alumnos = GestionarAlumnos(grupo.alumnos)
            gestionar_alumnos.mostrar_menu()
            
            print(f"Alumnos agregados al grupo '{grupo.grado} {grupo.seccion}' correctamente.")
            
            if self.isSave:
                self.guardar_en_json()
                
                if self.mongo_conn:
                    filter_criteria = {"grado": grupo.grado, "seccion": grupo.seccion}
                    grupo_actual = self.mongo_conn.find_documents("Grupos", filter_criteria)
                    
                    if grupo_actual:
                        alumnos_dict = [alumno.to_dict() for alumno in grupo.alumnos]
                        self.mongo_conn.update_document(
                            "Grupos", 
                            filter_criteria,
                            {"alumnos": alumnos_dict}
                        )
                    else:
                        grupo_dict = grupo.to_dict()
                        self.mongo_conn.insert_documents("Grupos", [grupo_dict])
                        
        else:
            print("Índice de grupo no válido.")


            
    def solicitar_indice(self):
        """
        Solicita al usuario que ingrese un índice válido (entero positivo).
        """
        try:
            indice = int(input("\nSelecciona el número del Grupo: ")) - 1
            if indice < 0 or indice >= len(self.contenedor):
                print("Índice fuera de rango.")
                return None
            return indice
        except ValueError:
            print("Por favor, ingresa un número entero válido.")
            return None
        
    def guardar_en_json(self):
        if self.archivo_cargado:
            nombre_archivo = self.archivo_cargado
            guardar_en_json(self.contenedor, nombre_archivo)
            print(f"Datos guardados en {nombre_archivo}.")
            
            
        else:
            print("Saliendo...")


if __name__ == '__main__':
    contenedor = "grupos.json"
    uri = "mongodb+srv://ZkOHDR5Y8tQq2C52:ZkOHDR5Y8tQq2C52@cluster0.sztvu.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    interfaz_grupos = GestionarGrupos(contenedor, db_uri=uri)
    interfaz_grupos.mostrar_menu()