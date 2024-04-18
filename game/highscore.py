import sqlite3


class HighScore : 
    def __init__(self) : 
        conn = sqlite3.connect('high_scores.db')
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS high_scores
                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                       username TEXT,
                       score INTEGER)''')
        conn.commit()
        conn.close()

    def save_high_score(self,username,score) : 
        conn = sqlite3.connect('high_scores.db')
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO high_scores (username, score)
                      VALUES (?, ?)''', (username, score))
        conn.commit()
        conn.close()
    
    def load_high_score(self) :
        conn = sqlite3.connect('high_scores.db')
        cursor = conn.cursor()
        cursor.execute('''SELECT * FROM high_scores
                      ORDER BY score DESC''')
        high_scores = cursor.fetchall()
        conn.close()
        return high_scores
    
    