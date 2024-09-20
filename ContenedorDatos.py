class ContenedorDatos:
    def __init__(self):
        self.datos = []

    def agregar_dato(self, dato):
        if isinstance(dato, self.__class__.__bases__[0]): 
            self.datos.append(dato)
        else:
            raise TypeError(f"Solo se pueden agregar objetos de la clase {self.__class__.__bases__[0].__name__}")

    def editar_dato(self, index, **kwargs):
        if 0 <= index < len(self.datos):
            dato = self.datos[index]
            for key, value in kwargs.items():
                if hasattr(dato, key):
                    setattr(dato, key, value)
        else:
            raise IndexError("Índice fuera de rango")

    def eliminar_dato(self, index):
        if 0 <= index < len(self.datos):
            del self.datos[index]
        else:
            raise IndexError("Índice fuera de rango")

    def __getitem__(self, index):
        if hasattr(self, 'datos'):
            return self.datos[index]
        else:
            raise IndexError("El objeto no es un contenedor de datos")

    def __len__(self):
        if hasattr(self, 'datos'):
            return len(self.datos)
        else:
            raise TypeError("El objeto no es un contenedor de datos")

    def __iter__(self):
        if hasattr(self, 'datos'):
            return iter(self.datos)
        else:
            raise TypeError("El objeto no es un contenedor de datos")
