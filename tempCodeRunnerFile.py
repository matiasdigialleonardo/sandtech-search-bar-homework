            self._cursor.execute(
                '''SELECT * FROM customers WHERE
                (id LIKE ? OR id IS NULL) AND
                (name LIKE ? OR name IS NULL) AND
                (surname LIKE ? OR surname IS NULL) AND
                (address LIKE ? OR address IS NULL)
                ''',
                (id, "%" + name + "%", "%" + surname + "%", "%" + address + "%")