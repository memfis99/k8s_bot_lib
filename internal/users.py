import sqlite3

conn = sqlite3.connect(":memory:")
cur = conn.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS users(
   userid TEXT PRIMARY KEY);
""")
conn.commit()
cur.execute("""INSERT INTO users(userid)
   VALUES('234769242'),
         ('5647388991');""")

conn.commit()

cur.execute(f'SELECT userid FROM users')
user_id_g = cur.fetchall()

#cur.execute("SELECT * FROM users;")
#all_users = cur.fetchall()
#print(one_result)
#print(type(one_result))