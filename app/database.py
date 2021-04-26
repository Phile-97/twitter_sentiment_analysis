import sqlite3
from sqlite3 import Error

## Database
class Database:
    def __init__(self, path):
        self.path = path
        self.connect()

    # create connection 
    def connect(self):
        try:
            self.conn = sqlite3.connect(self.path, check_same_thread=False)
            print("\nDatabase Connected.\n")
            self.cur = self.conn.cursor()
        except Error as e:
            print("\nDatabase Connection Failed!!!\n")
            print(e)
    
    # close connection 
    def close(self):
        try:
            self.conn.close()
            print("\nDatabase connection closed.\n")
        except Error as e:
            print(e)

    # live keyword search 
    def search(self, col, val):
        try:
            self.cur.execute(f"SELECT DISTINCT {col} FROM tweets WHERE {col} LIKE ? LIMIT 10", ('%'+val+'%',))
            return [row[0] for row in self.cur.fetchall()]
        except Error as e:
            print(e)        


    # get data and count from the columns
    def get_data(self, hashtags, location, date_start, date_end):
        data = {'tweets': [], 'counts': {'neg': 0, 'pos': 0, 'neu': 0}}
        try:
            if len(hashtags) == 1:
                self.cur.execute(f"SELECT DISTINCT * FROM tweets WHERE hashtags=? AND location=? AND date(date) BETWEEN ? AND ? ORDER BY random() LIMIT 50", (hashtags[0], location, date_start, date_end))
                data['tweets'] = self.cur.fetchall()
                self.cur.execute("SELECT COUNT(*) FROM tweets WHERE sentiment='negative' AND hashtags=? AND location=? AND date(date) BETWEEN ? AND ?", (hashtags[0], location, date_start, date_end))
                data['counts']['neg'] = self.cur.fetchone()[0]
                self.cur.execute("SELECT COUNT(*) FROM tweets WHERE sentiment='positive' AND hashtags=? AND location=? AND date(date) BETWEEN ? AND ?", (hashtags[0], location, date_start, date_end))
                data['counts']['pos'] = self.cur.fetchone()[0]
                self.cur.execute("SELECT COUNT(*) FROM tweets WHERE sentiment='neutral' AND hashtags=? AND location=? AND date(date) BETWEEN ? AND ?", (hashtags[0], location, date_start, date_end))
                data['counts']['neu'] = self.cur.fetchone()[0]

            if len(hashtags) > 1:
                self.cur.execute(f"SELECT DISTINCT * FROM tweets WHERE hashtags IN {tuple(hashtags)} AND location=? AND date(date) BETWEEN ? AND ? ORDER BY random() LIMIT 50", (location, date_start, date_end))
                data['tweets'] = self.cur.fetchall()
                self.cur.execute(f"SELECT COUNT(*) FROM tweets WHERE sentiment='negative' AND hashtags IN {tuple(hashtags)} AND location=? AND date(date) BETWEEN ? AND ?", (location, date_start, date_end))
                data['counts']['neg'] = self.cur.fetchone()[0]
                self.cur.execute(f"SELECT COUNT(*) FROM tweets WHERE sentiment='positive' AND hashtags IN {tuple(hashtags)} AND location=? AND date(date) BETWEEN ? AND ?", (location, date_start, date_end))
                data['counts']['pos'] = self.cur.fetchone()[0]
                self.cur.execute(f"SELECT COUNT(*) FROM tweets WHERE sentiment='neutral' AND hashtags IN {tuple(hashtags)} AND location=? AND date(date) BETWEEN ? AND ?", (location, date_start, date_end))
                data['counts']['neu'] = self.cur.fetchone()[0]

            data['counts']['total'] = data['counts']['pos'] + data['counts']['neg'] + data['counts']['neu']
            return data

        except Error as e:
            print(e)





