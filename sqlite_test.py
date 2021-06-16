import sqlite3

conn = sqlite3.connect('venv/include/config.db')

c = conn.cursor()

# c.execute("DROP TABLE misc")
# c.execute("CREATE TABLE IF NOT EXISTS testimonial (name text, test text)")
# c.execute("CREATE TABLE IF NOT EXISTS concern (id INTEGER PRIMARY KEY, conc text)")

# c.execute("INSERT INTO testimonial VALUES ('Gandalf', 'You shall not pass urine! Unsolicited! After seeing Katherine!')")
# c.execute("INSERT INTO testimonial VALUES ('golem', 'My problemses Katherine fixeded for us!')")

# c.execute("INSERT INTO firstconcern (care_name, care) VALUES ('first thing', 'this is how you do the first thing')")
# c.execute("INSERT INTO concern (conc) VALUES ('second concern')")

# id = (3, 4, 5, 6,)
# c.execute("DELETE FROM concern WHERE name = ?", id)
c.execute("SELECT item FROM misc WHERE id = 6")
rows = c.fetchall()
for row in rows:
    print(row[0])
# conn.commit()
# conn.close()
