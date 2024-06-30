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
            self.create_db()
            conn = _sqlite3.connect(settings.DB_PATH)
            cursor = conn.cursor()
            cursor.executemany("INSERT INTO vacancy VALUES (?, ?, ?)", [vacancy.to_list() for vacancy in self.result])
            conn.commit()
            conn.close()

        if self.json_mode:
            with open(settings.JSON_PATH, "a") as file:
                json.dump([vacancy.to_dict() for vacancy in self.result], file, indent=2, ensure_ascii=False)


        if self.csv_mode:
            vacancies = [vacancy.to_dict() for vacancy in self.result]
            keys = vacancies[0].keys()
            with open(settings.CSV_PATCH, "a") as file:
                writer = csv.DictWriter(file, keys)
                writer.writeheader()
                writer.writerows(vacancies)

    @staticmethod
    def create_db():
        conn = _sqlite3.connect(settings.DB_PATH)
        cursor = conn.cursor()

        cursor.execute("CREATE TABLE vacancy (id integer, title text, link text)")
        conn.close()
        print("DB created")