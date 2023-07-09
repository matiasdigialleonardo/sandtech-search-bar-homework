# Clase POJO que representa al cliente:
class Customer:
    def __init__(self, id, name, surname, address):
        self._id = id
        self._name = name
        self._surname = surname
        self._address = address
        
    # PROPERTIES para clase Customers
    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def surname(self):
        return self._surname

    @surname.setter
    def surname(self, value):
        self._surname = value

    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, value):
        self._address = value