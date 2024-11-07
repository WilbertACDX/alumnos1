from carrera import Carrera, guardar_en_json
from gestionarGrupos import GestionarGrupos
from mongoDBConnection import MongoDBConnection

class GestionarCarreras:
    def __init__(self, contenedor = None, db_uri=None, db_name="UTT"):
        self.archivo_cargado = None  # Atributo para almacenar el nombre del archivo
        self.isSave=True
        self.mongo_conn = MongoDBConnection(db_uri, db_name) if db_uri else None  # Conexión a MongoDB
        if contenedor is None:
            self.contenedor = Carrera()  # Crear un contenedor vacío
            print("Se ha creado un contenedor vacío.")
        elif isinstance(contenedor, str):
            try:
                self.contenedor = Carrera.cargar_de_json(contenedor)
                self.archivo_cargado = contenedor  # Guardar el nombre del archivo
                print(f"Alumnos cargados desde {contenedor}")
            except FileNotFoundError:
                print(f"No se encontró el archivo {contenedor}. Se utilizará un contenedor vacío.")
                self.contenedor = Carrera()  # Inicializar un contenedor vacío
        elif isinstance(contenedor, Carrera):
            self.contenedor = contenedor
            print("Contenedor de Alumnos proporcionado directamente.")
        else:
            print("Tipo de contenedor no válido. Se utilizará un contenedor vacío.")
            self.contenedor = Carrera()

    def mostrar_menu(self):
        while True:
            print("\n--- Menú de Carrera ---")
            print("1. Crear un Carrera")
            print("2. Ver Carreras")
            print("3. Eliminar Carrera")
            print("4. Editar Carrera")
            print("5. Agregar grupo a una carrera")
            print("6. Salir")
            
            opcion = input("Selecciona una opción: ")
            
            if opcion == "1":
                self.crear_carrera()
            elif opcion == "2":
                self.ver_carreras()
            elif opcion == "3":
                self.eliminar_carrera()
            elif opcion == "4":
                self.editar_carrera()
            elif opcion == "5":
                self.agregar_grupo_a_carrera()
            elif opcion == "6":
                print("Saliendo...")
                break
            else:
                print("Opción no válida. Intenta de nuevo.")

    def crear_carrera(self):
        nombre = input("Nombre: ")
        clave = input("SClave: ")
        
        nueva_carrera = Carrera(nombre, clave)
        self.contenedor.agregar_dato(nueva_carrera)  # Agrega el nuevo grupo al contenedor principal
        
        print(f"Carrera '{nombre} {clave}' creado correctamente.")
        if self.isSave:
            self.guardar_en_json()
            
            if self.mongo_conn:
                carrera_dict = nueva_carrera.to_dict()  # Convertir a diccionario si no está en este formato
                self.mongo_conn.insert_documents("Carreras", [carrera_dict])
                self.mongo_conn.remove_duplicates("Carreras", ["nombre", "clave"])
                print("Carrera guardada en MongoDB Atlas.")
                
        input("Presiona Enter para continuar...")


    def ver_carreras(self):
        if not self.contenedor.datos:
            print("No hay carreras disponibles.")
        else:
            for i, carrera in enumerate(self.contenedor.datos, start=1):
                print(f"{i}. {carrera}")
        input("Presiona Enter para continuar...")
                
    def eliminar_carrera(self):
        """
        Elimina un Carrera del contenedor.
        """
        if len(self.contenedor) == 0:
            print("No hay carreras para editar.")
            input("Presiona Enter para continuar...")
            return
        
        self.ver_carreras()

        indice = self.solicitar_indice()

        if indice is not None:
            carrera = self.contenedor.datos[indice]
            self.contenedor.eliminar_dato(indice)
            carrera_original= carrera.clave
            print("Carrera eliminado correctamente.")
        if self.isSave:
            self.guardar_en_json()
            if self.mongo_conn:
                    filter_criteria = {"clave": carrera_original}
                    self.mongo_conn.delete_document("Grupos", filter_criteria)  # Eliminar en MongoDB
                    
                    print("Datos del grupo eliminados de MongoDB Atlas.")
        input("Presiona Enter para continuar...")
        
    def editar_carrera(self):
        if len(self.contenedor) == 0:
            print("No hay carreras para editar.")
            input("Presiona Enter para continuar...")
            return
        
        self.ver_carreras()
        indice = self.solicitar_indice()

        if indice is not None:
            carrera = self.contenedor.obtener_carrera_indice(indice)
            clave_original = carrera.clave
            print(f"Editando a {carrera.nombre} {carrera.clave}")
            
            nuevo_nombre = input(f"Nombre [{carrera.nombre}]: ") or carrera.nombre
            nueva_clave = input(f"Clave [{carrera.clave}]: ") or carrera.clave
            
            # Actualiza en el contenedor
            self.contenedor.editar_dato(indice, nombre=nuevo_nombre, clave=nueva_clave)
            print("Carrera editada correctamente.")
        
        if self.isSave:
            self.guardar_en_json()
        
        # Actualizar en MongoDB
            if self.mongo_conn:
                filter_criteria = {"clave": clave_original}  # Filtrar por clave única
                new_values = {"nombre": nuevo_nombre, "clave": nueva_clave}
                self.mongo_conn.update_document("Carreras", filter_criteria, new_values)
                print("Carrera actualizada en MongoDB Atlas.")
    
    input("Presiona Enter para continuar...")


    def agregar_grupo_a_carrera(self):
        if not self.contenedor.datos:
            print("No hay carreras disponibles. Crea una carrera primero.")
            return

        self.ver_carreras()
        indice_carrera = int(input("Selecciona el número de la carrera: ")) - 1

        if 0 <= indice_carrera < len(self.contenedor.datos):
            carrera = self.contenedor.datos[indice_carrera]
            # Pasar la conexión MongoDB al crear la instancia de GestionarGrupos
            gestionar_grupos = GestionarGrupos(
                contenedor=carrera.grupos,
                db_uri=self.mongo_conn.uri if self.mongo_conn else None,
                db_name=self.mongo_conn.database_name if self.mongo_conn else "UTT"
            )
            gestionar_grupos.mostrar_menu()
            
            print(f"Grupo(s) agregados a la carrera '{carrera.nombre} {carrera.clave}' correctamente.")
            
            if self.isSave:
                self.guardar_en_json()
                
                if self.mongo_conn:
                    filter_criteria = {"nombre": carrera.nombre, "clave": carrera.clave}
                    carrera_actual = self.mongo_conn.find_documents("Carreras", filter_criteria)
                    
                    if carrera_actual:
                        grupos_dict = [grupo.to_dict() for grupo in carrera.grupos]
                        self.mongo_conn.update_document(
                            "Carreras", 
                            filter_criteria,
                            {"grupos": grupos_dict}
                        )
                    else:
                        carrera_dict = carrera.to_dict()
                        self.mongo_conn.insert_documents("Carreras", [carrera_dict])
        else:
            print("Índice de carrera no válido.")
            
    def solicitar_indice(self):
        """
        Solicita al usuario que ingrese un índice válido (entero positivo).
        """
        try:
            indice = int(input("\nSelecciona el número de la carrera: ")) - 1
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
    contenedor = 'carreras.json'
    uri = "mongodb+srv://ZkOHDR5Y8tQq2C52:ZkOHDR5Y8tQq2C52@cluster0.sztvu.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    interfaz_carrera = GestionarCarreras(contenedor, db_uri=uri)
    interfaz_carrera.mostrar_menu()