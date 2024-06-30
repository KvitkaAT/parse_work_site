import json
import csv
import _sqlite3

import settings


class ExportEngine:

    def __init__(self, db: bool, json_mode: bool, csv_mode: bool, result: list):
        self.db = db
        self.json_mode = json_mode
        self.csv_mode = csv_mode
        self.result = result


    def export(self):
        if self.db:
            ...
        if self.csv_mode:
            ...
        if self.json_mode:
            ...

    @staticmethod
    def create_db():
        conn = _sqlite3.connect(settings.DB_PATH)
        cursor = conn.cursor()

        cursor.execute("CREATE TABLE vacancy (id integer, title text, link text)")
        conn.close()