import sqlite3
import os
import pathlib
from typing import Literal

path = pathlib.Path(os.getcwd())

class User():
    def __init__(self, id: int, username: str, password: str) -> None:
        self.id = id
        self.username = username
        self.password = password

class DataModelService():
    def __init__(self, db_name="database.db") -> None:
        self.cnxn = sqlite3.connect(db_name)
        self.c = self.cnxn.cursor()
        self.create_tables()
        self.populate_database()
    
    def populate_database(self):
        if not len(self.fetch_all("users")):
            with open(path.joinpath("sql", "populate.sql")) as f:
                self.c.executescript(f.read())

    def create_tables(self):
        with open(path.joinpath("sql", "tables.sql")) as f:
            self.c.executescript(f.read())
    
    def fetch(self, query, n: Literal["all", "one"] ="all"):
        qs = self.c.execute(query)
        cols = [i[0] for i in qs.description]
        if n == "all":
            return [dict(zip(cols, i)) for i in qs.fetchall()]
        one = qs.fetchone()
        if one:
            return dict(zip(cols, one))
        return None
    
    def fetch_by_id(self, table: str, pk: int):
        return self.fetch(f'SELECT * FROM {table} WHERE id={pk};', "one")
    
    def fetch_all(self, table: str) -> list[dict]:
        return self.fetch(f'SELECT * FROM {table}', "all")
    
    def login(self, username, password):
        return self.fetch(f'SELECT * FROM users WHERE username="{username}" AND password="{password}";', "one")
    

