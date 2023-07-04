from EmoScan import db
from flask_login import UserMixin

# Crea un cursor para ejecutar comandos en la base de datos
cursor = db.cursor()

# Crea la tabla "tweets" en la base de datos
cursor.execute("""
    CREATE TABLE IF NOT EXISTS tweets (
        id INT(11) NOT NULL AUTO_INCREMENT,
        user_id INT(11) NOT NULL,
        query_id INT(11) NOT NULL,
        date VARCHAR(50) NOT NULL,
        content VARCHAR(255) NOT NULL,
        tweet_user VARCHAR(50) NOT NULL,
        polarity FLOAT,
        sentiment VARCHAR(50),
        PRIMARY KEY (id),
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
        FOREIGN KEY (query_id) REFERENCES queries(id) ON DELETE CASCADE
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
""")

# Confirma la transacción
db.commit()

#Clase Tweet
class Tweet(UserMixin):
    def __init__(self, id, user_id, query_id, date, content, tweet_user, polarity=None, sentiment=None):
        self.id = id
        self.user_id = user_id
        self.query_id = query_id
        self.date = date
        self.content = content
        self.tweet_user = tweet_user
        self.polarity = polarity
        self.sentiment = sentiment

    def saveTweets(self):
        try:
            sql = "INSERT INTO tweets (id, user_id, query_id,  date, content, tweet_user) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (self.id, self.user_id,self.query_id, self.date, self.content, self.tweet_user))
            db.commit()
        except Exception as ex:
            db.rollback()
            raise Exception(ex)

    @staticmethod
    def getId(id):
        try:
            sql = "SELECT id FROM tweets WHERE id = %s"
            cursor.execute(sql, (id,))
            row = cursor.fetchone()
            if row is not None:
                return row
            else:
                return None
        except Exception as ex:
            raise Exception(ex)

    @staticmethod
    def getTweetsByUser(user_id):
        try:
            sql = "SELECT id, date, content, tweet_user FROM tweets WHERE user_id = %s"
            cursor.execute(sql, (user_id,))
            rows = cursor.fetchall()
            tweets = []
            for row in rows:
                tweets.append(row)
            return tweets
        except Exception as ex:
            raise Exception(ex)
        
    @staticmethod
    def getTweetsByQuery(user_id, query_id):
        try:
            sql = "SELECT id, date, content, tweet_user, sentiment FROM tweets WHERE user_id = %s AND query_id = %s"
            cursor.execute(sql, (user_id,query_id,))
            rows = cursor.fetchall()
            tweets = []
            for row in rows:
                tweets.append(row)
            return tweets
        except Exception as ex:
            raise Exception(ex)

    @staticmethod    
    def addPolAndSent(polarity, sentiment, id):
        try:
            sql = "UPDATE tweets SET polarity=%s, sentiment=%s WHERE id=%s"
            cursor.execute(sql, (polarity,sentiment,id, ))
            db.commit()
        except Exception as ex:
            db.rollback()
            raise Exception(ex)

    @staticmethod
    def getTweetsBySent(user_id, query_id):
        try:
            sql = "SELECT * FROM tweets WHERE user_id = %s AND query_id = %s"
            cursor.execute(sql, (user_id,query_id,))
            rows = cursor.fetchall()
            tweets = []
            for row in rows:
                tweets.append(row)
            return tweets
        except Exception as ex:
            raise Exception(ex)
        
    @staticmethod
    def deleteTweetsByQueryId(query_id):
        try:
            sql = "DELETE FROM tweets WHERE query_id = %s"
            cursor.execute(sql, (query_id,))
            db.commit()
        except Exception as ex:
            db.rollback()
            raise Exception(ex)
        
