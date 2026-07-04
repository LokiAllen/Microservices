import sqlite3
class Repository:
  """Initialize the repository with a table name and create the database."""
  def __init__(self, table):
    self.table = table 
    self.database = self.table + ".db" 
    self.make()


  """Create the table if it does not exist."""
  def make(self):
    connection = sqlite3.connect(self.database)
    try:
      cursor = connection.cursor()
      cursor.execute(
        f"CREATE TABLE IF NOT EXISTS {self.table} " +
        "(name TEXT, artist TEXT, song TEXT, PRIMARY KEY (name, artist))"
      )
      connection.commit()
    finally:
      connection.close()


  """Clear all records from the table."""
  def clear(self):
    connection = sqlite3.connect(self.database)
    try:
      cursor = connection.cursor()
      cursor.execute(
        f"DELETE FROM {self.table}" 
      )
      connection.commit()
    finally:
      connection.close()


  """Insert a new record into the table."""
  def insert(self, js):
    connection = sqlite3.connect(self.database)
    try:
      cursor = connection.cursor()
      cursor.execute(
        f"INSERT INTO {self.table} (name, artist, song) VALUES (?,?,?)",
        (js["name"], js["artist"], js["song"])
      )
      connection.commit()
      return cursor.rowcount
    finally:
      connection.close()
  

  """Delete a record from the table by name and artist."""
  def delete(self, name, artist):
    connection = sqlite3.connect(self.database)
    try:
      cursor = connection.cursor()
      cursor.execute(
        f"DELETE FROM {self.table} WHERE name = ? AND artist = ?",
        (name, artist)
      )
      connection.commit()
      return cursor.rowcount
    finally:
      connection.close()


  """Update the song of a record identified by name and artist."""
  def update(self, js):
    connection = sqlite3.connect(self.database)
    try:
      cursor = connection.cursor()
      cursor.execute(
        f"UPDATE {self.table} SET song = ? WHERE name = ? AND artist = ?",
        (js["song"], js["name"], js["artist"])
      )
      connection.commit()
      return cursor.rowcount
    finally:
      connection.close()


  """Look up a record by name and artist."""
  def lookup(self, name, artist):
    connection = sqlite3.connect(self.database)
    try:
      cursor = connection.cursor()
      cursor.execute(
        f"SELECT name, artist, song FROM {self.table} WHERE name = ? AND artist = ?",
        (name, artist)
      )
      row = cursor.fetchone()
      if row:
        return {"name": row[0], "artist": row[1], "song": row[2]}
      else:
        return None
    finally:
      connection.close()


  """Return all records in the table."""
  def return_all(self):
    connection = sqlite3.connect(self.database)
    try:
      cursor = connection.cursor()
      cursor.execute(
        f"SELECT name, artist, song FROM {self.table}"
      )
      rows = cursor.fetchall()
      return [{"name": row[0], "artist": row[1], "song": row[2]} for row in rows]
    finally:
      connection.close()
