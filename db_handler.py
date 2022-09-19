import os, sqlite3

db_file = os.getcwd() + "\player_database.db"

class PlayerDBHandler():
    def __init__(self):
        self.conn = sqlite3.connect(db_file)
        self.cursor = conn.cursor()
        if not os.path.exists(db_file):
            self.create_tables()

    def create_tables(self):
        query_str = """ CREATE TABLE IF NOT EXISTS players (
                        player_id INT NOT NULL PRIMARY KEY,
                        balance INT
                        ); """
        self.cursor.execute(query_str)
    
    def create_player_entry(self, player_id):
        query_str = "INSERT INTO players (player_id, balance) VALUES (" + player_id + ", 1000);"
        self.cursor.execute(query_str)