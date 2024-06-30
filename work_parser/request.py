import requests

import settings

from fake_useragent import UserAgent


class RequestEngine:

    def get_response(self, url: str, params: dict | None = None) -> requests.Response:
        response = requests.get(url, params=params, headers={"User-Agent": self.get_user_agent()})
        response.raise_for_status()
        return response

    @staticmethod
    def get_user_agent():
        return UserAgent().random


