# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk, messagebox

from customer import Customer
from customer_manager import CustomerManager

# Clase Application para implementar la vista con Tkinter, observar la herencia:
class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gestión de Clientes")
        self.geometry("1024x768")

        self.customer_manager = CustomerManager()

        self.create_menu()
        self.create_table_view()

        # Cuando inicia la aplicación refresca la tabla clientes
        self.refresh_table()
        
    # Método que crea el menú:
    def create_menu(self):
        self.menu_bar = tk.Menu(self)

        # Opciones del menú
        customers_menu = tk.Menu(self.menu_bar, tearoff=0)
        customers_menu.add_command(
            label="Dar de alta", command=self.add_customer)
        customers_menu.add_command(
            label="Modificar", command=self.update_customer)
        customers_menu.add_command(
            label="Eliminar", command=self.delete_customer)
        customers_menu.add_command(
            label="Listar todos", command=self.list_all_customers)
        customers_menu.add_command(
            label="Buscar", command=self.search_customer
        )
        

        self.menu_bar.add_cascade(label="Clientes", menu=customers_menu)
        self.config(menu=self.menu_bar)

    # Método que crea la vista en tabla para listar todos los clientes.
    def create_table_view(self):
        self.table_frame = tk.Frame(self)
        self.table_frame.pack(padx=10, pady=10)

        self.table = ttk.Treeview(self.table_frame, columns=(
            "id", "name", "surname", "address"))
        self.table.heading("id", text="Código")
        self.table.heading("name", text="Nombre")
        self.table.heading("surname", text="Apellido")
        self.table.heading("address", text="Dirección")
        self.table.pack()

    # Método que refresca la tabla para mostrar los datos de los clientes guardados
    def refresh_table(self):
        self.table.delete(*self.table.get_children())
        customers = self.customer_manager.get_all_customers()
        if customers:
            for customer in customers:
                self.table.insert("", "end", values=(
                    customer.id, customer.name, customer.surname, customer.address))
        else:
            self.table.insert("", "end", values=(
                "No hay clientes cargados.", "", "", ""))
            
    # Método de vista para mostrar el formulario de inserción de un cliente
    def add_customer(self):
        add_window = tk.Toplevel(self)
        add_window.title("Agregar un cliente")
        add_window.geometry("300x200")

        tk.Label(add_window, text="Nombre:").pack()
        name_entry = tk.Entry(add_window)
        name_entry.pack()

        tk.Label(add_window, text="Apellido:").pack()
        surname_entry = tk.Entry(add_window)
        surname_entry.pack()

        tk.Label(add_window, text="Dirección:").pack()
        address_entry = tk.Entry(add_window)
        address_entry.pack()

        def save_customer():
            name = name_entry.get()
            surname = surname_entry.get()
            address = address_entry.get()

            customer = Customer(id, name, surname, address)
            self.customer_manager.insert_customer(customer)
            add_window.destroy()
            self.refresh_table()

        tk.Button(add_window, text="Guardar", command=save_customer).pack()

    # Método de vista para mostrar el formulario de borrado de un cliente
    def delete_customer(self):
        delete_window = tk.Toplevel(self)
        delete_window.title("Eliminar un cliente")
        delete_window.geometry("200x100")

        tk.Label(delete_window, text="Código:").pack()
        id_entry = tk.Entry(delete_window)
        id_entry.pack()

        def delete():
            id = int(id_entry.get())
            self.customer_manager.delete_customer(id)
            delete_window.destroy()
            self.refresh_table()

        tk.Button(delete_window, text="Eliminar", command=delete).pack()

    # Método de vista para mostrar el formulario de modificación de un cliente
    def update_customer(self):
        update_window = tk.Toplevel(self)
        update_window.title("Modificar un cliente")
        update_window.geometry("300x200")

        tk.Label(update_window, text="Código:").pack()
        id_entry = tk.Entry(update_window)
        id_entry.pack()

        tk.Label(update_window, text="Nombre:").pack()
        name_entry = tk.Entry(update_window)
        name_entry.pack()

        tk.Label(update_window, text="Apellido:").pack()
        surname_entry = tk.Entry(update_window)
        surname_entry.pack()

        tk.Label(update_window, text="Dirección:").pack()
        address_entry = tk.Entry(update_window)
        address_entry.pack()

        def update():
            id = int(id_entry.get())
            customer = self.customer_manager.get_customer(id)
            if customer:
                customer.name = name_entry.get()
                customer.surname = surname_entry.get()
                customer.address = address_entry.get()
                self.customer_manager.update_customer(customer)
                update_window.destroy()
                self.refresh_table()

        tk.Button(update_window, text="Modificar", command=update).pack()

    # Método de vista para mostrar los clientes en la tabla y por consola
    def list_all_customers(self):
        # Refrescar el listado de clientes en la tabla de Tkinter
        self.refresh_table()
        
        # Listar los clientes por consola para ver salida de la transacción
        customers = self.customer_manager.get_all_customers()
        if customers:
            for customer in customers:
                print(f"Código: {customer.id}")
                print(f"Nombre: {customer.name}")
                print(f"Apellido: {customer.surname}")
                print(f"Dirección: {customer.address}")
                print("-------------------")
        else:
            print("No se encontraron clientes.")
            
    def search_customer(self):
        
        # Clears the table and insert the customers returned from the search into it.
        def search():
            search_table.delete(*search_table.get_children())
            search_string = (name_entry.get(), surname_entry.get())
            
            customers = self.customer_manager.find_matching_customers(search_string)
            
            if customers:
                for customer in customers:
                    search_table.insert("", tk.END, values=(customer.id, customer.name, customer.surname, customer.address))

        search_window = tk.Toplevel(self)
        search_window.title("Buscar clientes")

        tk.Label(search_window, text="Nombre:").pack()
        name_entry = tk.Entry(search_window)
        name_entry.pack()

        tk.Label(search_window, text="Apellido:").pack()
        surname_entry = tk.Entry(search_window)
        surname_entry.pack()
        
        tk.Button(search_window, text="Buscar", command=search).pack()
        
        # Create a table widget
        search_table = ttk.Treeview(search_window, columns=("id", "name", "surname", "address"), show="headings")

        # Define column headings
        search_table.heading("id", text="ID")
        search_table.heading("name", text="Name")
        search_table.heading("surname", text="Surname")
        search_table.heading("address", text="Address")

        # Set column widths, anchor=tk.CENTER is used to center the content of the columns.
        search_table.column("id", width=50, anchor=tk.CENTER)
        search_table.column("name", width=100, anchor=tk.CENTER)
        search_table.column("surname", width=100, anchor=tk.CENTER)
        search_table.column("address", width=200, anchor=tk.CENTER)
        
        search_table.pack()

        
    def quit(self):
        self.customer_manager.close_connection()
        self.destroy()

##Iniciar la aplicación:
if __name__ == "__main__":
    app = Application()
    app.mainloop()
