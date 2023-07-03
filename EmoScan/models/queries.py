from EmoScan import db
from flask_login import UserMixin

# Crea un cursor para ejecutar comandos en la base de datos
cursor = db.cursor()

# Crea la tabla "queries" en la base de datos
cursor.execute("""
    CREATE TABLE IF NOT EXISTS queries (
        id INT(11) NOT NULL AUTO_INCREMENT,
        user_id INT(11) NOT NULL,
        query VARCHAR(50) NOT NULL,
        query_datetime DATETIME NOT NULL,
        query_type VARCHAR(20) NOT NULL,
        show_replies BOOLEAN,
        language VARCHAR(20),
        from_date DATE,
        to_date DATE,
        tweet_count INT(11),
        PRIMARY KEY (id),
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
""")
# Confirma la transacción
db.commit()

class Query(UserMixin):
    def __init__(self, id, user_id, query, query_datetime, query_type, show_replies=None, language=None, from_date=None, to_date=None, tweet_count=None):
        self.id = id
        self.user_id = user_id
        self.query = query
        self.query_datetime = query_datetime
        self.query_type = query_type
        self.show_replies = show_replies
        self.language = language
        self.from_date = from_date
        self.to_date = to_date
        self.tweet_count = tweet_count

    def savequery(self):
        try:
            sql = "INSERT INTO queries (id, user_id, query, query_datetime, query_type, show_replies, language, from_date, to_date, tweet_count) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (self.id, self.user_id, self.query, self.query_datetime, self.query_type, self.show_replies, self.language, self.from_date, self.to_date, self.tweet_count))
            db.commit()
            return cursor.lastrowid
        except Exception as ex:
            db.rollback()
            raise Exception(ex)

    @staticmethod
    def getQueryById(id):
        try:
            sql = "SELECT * FROM queries WHERE id = %s"
            cursor.execute(sql, (id,))
            row = cursor.fetchone()
            if row is not None:
                return Query(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9])
            else:
                return None
        except Exception as ex:
            raise Exception(ex)

    @staticmethod
    def getQueriesByUser(user_id):
        try:
            sql = "SELECT * FROM queries WHERE user_id = %s"
            cursor.execute(sql, (user_id,))
            rows = cursor.fetchall()
            queries = []
            for row in rows:
                queries.append([row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9]])
            return queries
        except Exception as ex:
            raise Exception(ex)

    @staticmethod
    def deleteQueryById(id):
        try:
            sql = "DELETE FROM queries WHERE id = %s"
            cursor.execute(sql, (id,))
            db.commit()
        except Exception as ex:
            db.rollback()
            raise Exception(ex)
        

    @staticmethod
    def getQueriesWithSentimentByUser(user_id):
        try:
            sql = """
                SELECT q.id, q.user_id, q.query, q.query_datetime, q.query_type, q.show_replies, q.language, q.from_date, q.to_date, q.tweet_count
                FROM queries q
                INNER JOIN tweets t ON q.id = t.query_id
                WHERE q.user_id = %s AND t.sentiment IS NOT NULL
                GROUP BY q.id
            """
            cursor.execute(sql, (user_id,))
            rows = cursor.fetchall()
            queries = []
            for row in rows:
                queries.append(Query(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9]))
            return queries
        except Exception as ex:
            raise Exception(ex)
        
