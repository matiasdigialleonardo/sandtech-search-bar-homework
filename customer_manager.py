import sqlite3
from customer import Customer


# Clase CustomerManager para mapear datos de la clase Customer a la base de datos.
class CustomerManager:
    def __init__(self):
        self._connection = sqlite3.connect("customers.db")
        self._cursor = self._connection.cursor()
        self._create_table()    
    
    def _create_table(self):
        # Solo va a crear la tabla customers si no existe. 
        # Es mejor no permitir valores nulos
        self._cursor.execute("""          
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL, 
                surname TEXT NOT NULL,
                address TEXT NOT NULL
            );
        """)
        # Solo va a insertar el valor 99 de id atoincremental
        # para empezar cn código en valor igual a 100 si no 
        # existe la columna name con el valor 'customers',
        # esto significa que solo se insertará la primera
        # vez que se crea la tabla customers.
        self._cursor.execute("""
            INSERT INTO sqlite_sequence (name, seq)
            SELECT 'customers', 99
            WHERE NOT EXISTS (SELECT 1 FROM sqlite_sequence WHERE name = 'customers')
        """)   
        self._connection.commit()
        
    def insert_customer(self, customer):
        self._cursor.execute("""
            INSERT INTO customers (name, surname, address)
            VALUES (?, ?, ?)
        """, (customer.name, customer.surname, customer.address))
        self._connection.commit()
        print("Cliente agregado correctamente.")

    def delete_customer(self, id):
        self._cursor.execute("DELETE FROM customers WHERE id=?", (id,))
        self._connection.commit()
        print("Cliente eliminado correctamente.")

    def update_customer(self, customer):
        self._cursor.execute("""
            UPDATE customers
            SET name=?, surname=?, address=?
            WHERE id=?
        """, (customer.name, customer.surname, customer.address, customer.id))
        self._connection.commit()
        print("Cliente actualizado correctamente.")

    def get_customer(self, id):
        self._cursor.execute("SELECT * FROM customers WHERE id=?", (id,))
        customer_data = self._cursor.fetchone()
        if customer_data:
            id, name, surname, address = customer_data
            return Customer(id, name, surname, address)
        else:
            print("Cliente no encontrado.")
            return None

    def get_all_customers(self):
        self._cursor.execute("SELECT * FROM customers")
        customers_data = self._cursor.fetchall()
        customers = []
        for customer_data in customers_data:
            id, name, surname, address = customer_data
            customer = Customer(id, name, surname, address)
            customers.append(customer)
        return customers

    def find_matching_customers(self, customer_data):

        name, surname = customer_data

        # Query to search for customers based on name and surname
        if customer_data:
            self._cursor.execute(
                '''SELECT * FROM customers WHERE
                name LIKE ? AND
                surname LIKE ?
                ''',
                ("%" + name + "%", "%" + surname + "%")
        )
            
        # For each result, create a Customer object, append it to a list and return it. Returns None if no matches were found
        customers = []
        matching_customers = self._cursor.fetchall()
        if matching_customers:
            for customer_data in matching_customers:
                id, name, surname, address = customer_data
                customer = Customer(id, name, surname, address)
                customers.append(customer)
            return customers
        else:
            return None

    def close_connection(self):
        self._cursor.close()
        self._connection.close()