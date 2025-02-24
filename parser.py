import requests
import re
import json
from bs4 import BeautifulSoup
from exceptions import LogoutException
    
class ItemParser:
    def __init__(self, url, params, cookies, headers):
        self.url = url
        self.params = params
        self.cookies = cookies
        self.headers = headers

    def get_items(self):
        response = requests.get(self.url, params=self.params, cookies=self.cookies, headers=self.headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        if 'Вы новый пользователь или забыли свой пароль в системе?' in soup.text:
            raise LogoutException
        script = soup.find(id='4me-js2')
        pattern = r'props\s*=\s*({.*?});'
        match = re.search(pattern, script.text, re.DOTALL)

        if match:
            props = json.loads(match.group(1))
            items = props.get('items', [])
            return items
        return []

    def get_unread_items(self):
        """Возвращает только новые непрочитанные элементы."""
        all_items = self.get_items()
        unread_items = [item for item in all_items if item.get('unread') is not None]
        return unread_items
