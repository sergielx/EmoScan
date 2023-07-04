from EmoScan import db

from flask_login import UserMixin


# Crea un cursor para ejecutar comandos en la base de datos
cursor = db.cursor()

# Crea la tabla "users" en la base de datos
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INT(11) NOT NULL AUTO_INCREMENT,
        name VARCHAR(50) NOT NULL,
        last VARCHAR(50) NOT NULL,
        username VARCHAR(50) NOT NULL,
        email VARCHAR(100) NOT NULL,
        password VARCHAR(255) NOT NULL,
        PRIMARY KEY (id),
        UNIQUE KEY email (email),
        UNIQUE KEY username (username)
    ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
""")

# Confirma la transacción
db.commit()

class User(UserMixin):
    def __init__(self, id, name, last, username, email, password):
        self.id = id
        self.name = name
        self.last = last
        self.username = username
        self.email = email
        self.password = password
    
    @staticmethod
    def getId(id):
        try:
            sql = "SELECT * FROM users WHERE id = {}".format(id)
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                return User(row[0], row[1], row[2], row[3], row[4], row[5])
            else:
                return None
        except Exception as ex:
            raise Exception(ex)   
        
    @staticmethod
    def updateUserData(user_id, field, new_value):
        try:
            # Verifica el campo que se desea actualizar y construye la sentencia SQL correspondiente
            if field == 'name':
                sql = "UPDATE users SET name = %s WHERE id = %s"
            elif field == 'last':
                sql = "UPDATE users SET last = %s WHERE id = %s"
            elif field == 'username':
                sql = "UPDATE users SET username = %s WHERE id = %s"
            elif field == 'email':
                sql = "UPDATE users SET email = %s WHERE id = %s"
            elif field == 'password':
                sql = "UPDATE users SET password = %s WHERE id = %s"
            else:
                raise ValueError("Campo inválido")

            cursor.execute(sql, (new_value, user_id))
            db.commit()
        except Exception as ex:
            raise Exception(ex)