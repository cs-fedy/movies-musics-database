import sqlite3
from os import path
from abc import ABC, abstractmethod
from typing import Dict, List

class DB(ABC):
  def __init__(self) -> None:
    super().__init__()
    self.connection: sqlite3.Connection = None

  def connect(self):
    try:
      BASE_DIR = path.dirname(path.abspath(__file__)) 
      db_path = path.join(BASE_DIR, "sqlite.db")
      self.connection = sqlite3.connect(db_path)
    except sqlite3.Error as error:
      print("Failed to read data from sqlite table", error)
      exit(1)
    return self

  def __enter__(self):
    return self.connect()

  def __exit__(self, exc_type, exc_value, exc_tb):
    self.connection.close()

  @abstractmethod
  def _create_table(self):
    print('table created')


class Title(DB):
  def _create_table(self):
    self.connect()
    CREATE_TABLE_SQL_QUERY = """
      CREATE TABLE title(
        name TEXT PRIMARY KEY,
        title_link TEXT NOT NULL,
        title_cover TEXT NOT NULL,
        genres TEXT NOT NULL,
        description TEXT NOT NULL,
        title_type TEXT CHECK(title_type IN ('tv_show', 'movie')) NOT NULL
      )
    """

    cursor = self.connection.cursor()
    cursor.execute(CREATE_TABLE_SQL_QUERY)
  
  def save_new_title(self, title_data) -> None:
    cursor = self.connection.cursor()
    SAVE_NEW_TITLE_SQL_QUERY = f"""
      INSERT INTO title VALUES (
        {title_data['title']},
        {title_data['title_link']},
        {title_data['title_cover']},
        {title_data['genres']},
        {title_data['description']},
        {title_data['title_type']}
      )
    """
    cursor.execute(SAVE_NEW_TITLE_SQL_QUERY)


  def get_titles_names(self) -> List:
    cursor = self.connection.cursor()
    GET_TITLE_NAMES_SQL_QUERY = """
      SELECT name, title_type FROM title
    """
    return cursor.execute(GET_TITLE_NAMES_SQL_QUERY).fetchall()


class Song(DB):
  def _create_table(self):
    self.connect()
    CREATE_TABLE_SQL_QUERY = """
      CREATE TABLE song(
        title_name TEXT PRIMARY KEY,
        song_name TEXT PRIMARY KEY,
        artist TEXT NOT NULL,
        description TEXT NOT NULL,
        PRIMARY KEY(title_name, song_name),
        FOREIGN KEY (title_name) REFERENCES title(title_name)
      )
    """

    cursor = self.connection.cursor()
    cursor.execute(CREATE_TABLE_SQL_QUERY)

  def save_new_songs(self, title_name: str, songs: Dict):
    cursor = self.connection.cursor()
    SAVE_SONGS_SQL_QUERY = """
      INSERT INTO song VALUES(?,?,?,?)
    """

    songs = [
      (title_name, song['song_title'], song['artist'], song['description']) 
      for song in songs
    ]
    cursor.executemany(SAVE_SONGS_SQL_QUERY, songs)
    self.connection.commit()