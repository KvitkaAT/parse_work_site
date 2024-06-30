import argparse
import os.path
import shutil
import time
from bs4 import BeautifulSoup

import settings
from work_parser import Vacancy, RequestEngine, Parser, ExportEngine


def create_data_directory():
    path = os.path.join(settings.PARENT_DIR, "data")

    try:
        shutil.rmtree(path)
    except FileNotFoundError:
        pass

    os.makedirs(path)


def main(db: bool, json_mode: bool, csv_mode: bool):
    create_data_directory()
    page = settings.START_PAGE

    while True:
        vacancy = Vacancy()
        page_number = f"PAGE: {page}"
        print(page_number)

        request_engine = RequestEngine()
        response = request_engine.get_response(settings.HOST + settings.ROOT_PATH, {"ss": settings.SS, "page": page})
        html = response.text

        time.sleep(1)

        parser = Parser(BeautifulSoup(html, "html.parser"))
        cards = parser.find_cards(
            class_="card card-hover card-search card-visited wordwrap job-link js-job-link-blank js-hot-block"
        )

        if not cards:
            break

        result = []
        for card in cards:
            vacancy = Vacancy()
            href, id_vac = parser.get_vacancy_id_and_href(card)
            card_link = settings.HOST + href
            print(card_link)

            response = request_engine.get_response(card_link)
            parser.soup = BeautifulSoup(response.text, "html.parser")
            title = parser.get_title()
            print(title)

            vacancy.title = title
            vacancy.vacancy_id = id_vac
            vacancy.href = card_link
            result.append(vacancy)
        export_engine = ExportEngine(db, json_mode, csv_mode, result)
        export_engine.export()


        break
        page += 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parser of work ua site")
    parser.add_argument("-db", default=False, action="store_true", help="DB store opportunity")
    parser.add_argument("-json", default=False, action="store_true", help="JSON store opportunity")
    parser.add_argument("-csv", default=False, action="store_true", help="CSV store opportunity")
    args = parser.parse_args()
    # main(args.db, args.json, args.csv)
    main(db=True, json_mode=True, csv_mode=True)

