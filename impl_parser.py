import abc
import requests
from bs4 import BeautifulSoup

class Parser(abc.ABC):
    def __init__(self):
        self.session = requests.Session()

    @abc.abstractmethod
    def get_by_url(self, url: str):
        """

        :param url:
        :return:
        """

    @abc.abstractmethod
    def get_by_sku(self, sku: str):
        """

        :param sku:
        :return:
        """

    @abc.abstractmethod
    def get_by_keyword(self, keyword: str):
        """

        :param keyword:
        :return:
        """

    def set_session(self):
        self.session = requests.Session()

    def drop_session(self):
        self.session.close()

    # Создан для универсализации получения супа по ссылке
    def get_data(self, url):

        headers = {
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36 OPR/72.0.3815.400',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
            'Referer': url,
            'Upgrade-Insecure-Requests': '1',
            'TE': 'Trailers',
        }

        response = self.session.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')

        return soup, response

    # Создан для универслизации отправки данных
    def post_data(self, url, siteroot, data=None):

        headers = {
            'authority': siteroot[8:],
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-language': 'ru,en;q=0.9',
            'x-requested-with': 'XMLHttpRequest',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36 OPR/72.0.3815.400',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'origin': siteroot,
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': url,
            'Upgrade-Insecure-Requests': '1',
        }

        response = self.session.post(url, headers=headers, data=data)
        return response
