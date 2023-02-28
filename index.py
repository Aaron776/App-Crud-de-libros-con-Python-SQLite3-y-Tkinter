from tkinter import ttk
from tkinter import *
import sqlite3

class Libros:
    # Conexion a la base de datos
    db_name = 'database.db'
    
    
    def __init__(self,window):
        self.wind=window
        self.wind.title('Aplicacion de Libros')
        
    # Creando el contenedor Frame (un frame es un conetnedor para poder tener elementos) 
        frame = LabelFrame(self.wind, text = 'Registrar Nuevo Libro')
        frame.grid(row = 0, column = 0, columnspan = 3, pady = 20)
    
    
    # Input para ingresar Nombre
        Label(frame, text = 'Nombre del libro: ').grid(row = 1, column = 0)
        self.name = Entry(frame)
        self.name.focus()
        self.name.grid(row = 1, column = 1)
        
    # Input para ingresar Precio
        Label(frame, text = 'Precio del libro: ').grid(row = 2, column = 0)
        self.precio = Entry(frame)
        self.precio.focus()
        self.precio.grid(row = 2, column = 1)
        
    # Boton para agregar el libro al listado
        ttk.Button(frame, text='Registrar Libro', command=self.agregarLibros).grid(row = 3, columnspan = 2, sticky = W + E)
        
    # Mostrando Mensaje
        self.mensaje = Label(text = '', fg = 'red')
        self.mensaje.grid(row = 3, column = 0, columnspan = 2, sticky = W + E)
        
        
    # Tabla
        self.tree = ttk.Treeview(height = 10, columns = 2)
        self.tree.grid(row = 4, column = 0, columnspan = 2)
        self.tree.heading('#0', text = 'Libro', anchor = CENTER)
        self.tree.heading('#1', text = 'Precio', anchor = CENTER)
        
     
     # Botones para actualizar o eliminar un registro de la tabla
        ttk.Button(text = 'Borrar', command = self.eliminarRegistros).grid(row = 5, column = 0, sticky = W + E)
        ttk.Button(text = 'Editar', command = self.editarRegistros).grid(row = 5, column = 1, sticky = W + E)
     
     # Mostrando registros de la tabla de la base de datos
        self.obtenerRegistros() #ejecuto la funcion  que trae los registros
        
           
    # Funcion para conectarme a la base de datos
    def run_query(self, query, parameters = ()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
        return result
    
    # Funcion para traer los registros de la base de datos
    def obtenerRegistros(self):
        # Limpiar tabla
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
            
        # Obteniendo registros
        query = 'SELECT * FROM libros ORDER BY nombre DESC'
        db_rows = self.run_query(query)
        
        # filling data
        for row in db_rows:
            self.tree.insert('', 0, text = row[1], values = row[2])
            
    
    
    #Funcion para validar campos
    def validaciones(self):
        return len(self.name.get()) !=0 and len(self.precio.get())!=0 # aqui verifico si los valores ingresados en los campos name y precio son distinbtos de cero
        
    
    # Funcion para agregar nuevo libro
    def agregarLibros(self):
        if self.validaciones():
            print (self.name.get())
            print (self.precio.get())
            query='INSERT INTO libros VALUES(NULL,?,?)'
            parametros=(self.name.get(),self.precio.get())
            self.run_query(query, parametros) # ejecuto la consulta query
            self.mensaje['text'] = 'El libro {} agregado satisfactoriamente'.format(self.name.get()) # aqui muestro un mesaje una vez agreagdo el nuevo libro
            self.name.delete(0, END) # aqui estoy limpiando los inputs name y precio de la interfaz
            self.precio.delete(0, END)
        else:    
            self.mensaje['text']="El nombre y el precio son requeridos" 
            print("El nombre y el precio son requeridos")
        
        self.obtenerRegistros()
        
    
    #Eliminar registros
    def eliminarRegistros(self):
        self.mensaje['text'] = ''
        try:
           self.tree.item(self.tree.selection())['text'][0]
        except IndexError as e:
            self.mensaje['text'] = 'Por favor selecciona un registro'
            return
        self.mensaje['text'] = ''
        nombre=self.tree.item(self.tree.selection())['text'] # aqui estoy obteniendo el nombre del libro que quiero eliminar al dar click en el boton eliminar
        query="DELETE FROM libros WHERE nombre=?"
        self.run_query(query, (nombre, )) # aqui ejecuto la consulta SQL
        self.mensaje['text']="El registro {} ha sido eliminado con exito".format(nombre)
        self.obtenerRegistros()
    
    
    #Editar registros    
    def editarRegistros(self):   
        self.mensaje['text'] = ''
        try:
           self.tree.item(self.tree.selection())['text'][0]
        except IndexError as e:
            self.mensaje['text'] = 'Por favor selecciona un registro'
            return
        self.mensaje['text'] = ''
        nombre=self.tree.item(self.tree.selection())['text'] # aqui estoy obteniendo el nombre del libro que voy a editar (lo estoy capturando)
        precio_antiguo=self.tree.item(self.tree.selection())['values'][0] # aqui estoy obteniendo el precio del libro que voy a editar (lo estoy capturando)
        self.edit_wind = Toplevel()
        self.edit_wind.title = 'Editar Libro'
        
        # Mostrando el Nombre anterior del libro para editar en el input
        Label(self.edit_wind, text = 'Libro: ').grid(row = 0, column = 1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = nombre), state = 'readonly').grid(row = 0, column = 2)
        
        # Nuevo nombre del libro que vasmos a editar
        Label(self.edit_wind, text = 'Nuevo Nombre del libro: ').grid(row = 1, column = 1)
        new_nombre = Entry(self.edit_wind) # aqui obtnego el valor del nuevo nombre
        new_nombre.grid(row = 1, column = 2)
        
        # Mostrando el precio actual del libro seleccionado para editarlo y es mostrado en el input
        Label(self.edit_wind, text = 'Precio Actual: ').grid(row = 2, column = 1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = precio_antiguo), state = 'readonly').grid(row = 2, column = 2)
        
        # Nuevo precio que voy a ingresar
        Label(self.edit_wind, text = 'Nuevo Precio: ').grid(row = 3, column = 1)
        new_precio= Entry(self.edit_wind) # qui obtnego el valor del nuevo precio
        new_precio.grid(row = 3, column = 2)
        
        Button(self.edit_wind, text = 'Actualizar', command = lambda: self.editarLibro(new_nombre.get(), nombre, new_precio.get(),precio_antiguo)).grid(row = 4, column = 2, sticky = W)
        self.edit_wind.mainloop()

    def editarLibro(self, nuevo_nombre, nombre, nuevo_precio, precio_anterior):
        query = 'UPDATE libros SET nombre = ?, precio = ? WHERE nombre = ? AND precio = ?'
        parametros = (nuevo_nombre, nuevo_precio,nombre, precio_anterior)
        self.run_query(query, parametros)
        self.edit_wind.destroy()
        self.mensaje['text'] = 'Libro {} actualizado con exito'.format(nombre)
        self.obtenerRegistros()



if __name__ == '__main__':
    window=Tk()
    aplicacion=Libros(window)
    window.mainloop()

 #comando para ejecutar la aplicacion: python index.py 