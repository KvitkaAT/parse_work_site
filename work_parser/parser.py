from bs4 import BeautifulSoup, Tag


class Parser:

    def __init__(self, soup: BeautifulSoup):
        self.soup = soup

    @staticmethod
    def get_vacancy_id_and_href(card: Tag) -> tuple[str, str]:
        tag_a = card.find("h2").find("a")
        href = tag_a["href"]
        id_vac = "".join(x for x in href if x.isdigit())
        return href, id_vac

    def find_cards(self, class_: str) -> list[Tag]:
        cards = self.soup.find_all("div", class_=class_)
        extend_class = class_ + " mt-lg"
        first_card = self.soup.find_all("div", class_=extend_class)
        cards = first_card + cards
        return cards

    def get_title(self) -> str:
        class_title = "my-0"
        title = self.soup.find("h1", class_=class_title)
        title = "".join(letter for letter in title if letter != "'")
        return title
