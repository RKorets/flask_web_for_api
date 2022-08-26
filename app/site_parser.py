import requests
from bs4 import BeautifulSoup
from collections import defaultdict
from fake_headers import Headers
import asyncio
import aiohttp


class Rozetka:

    def __init__(self):
        self.parse_dict = {}

    @staticmethod
    def get_pages_in_categories(categories: str) -> dict:
        promo_category_element = defaultdict(list)
        header = Headers(
            browser="chrome",
            os="win",
            headers=True
        ).generate()

        response = requests.get(url=f'https://rozetka.com.ua/' + categories, headers=header)

        soup = BeautifulSoup(response.text, 'lxml')
        pagination_link = soup.find_all('a', class_='pagination__link ng-star-inserted')

        promo_category_element[categories].append(f'https://rozetka.com.ua/' + categories)

        for page in pagination_link:
            page_url = page.get('href')[1:]
            promo_category_element[categories].append(f'https://rozetka.com.ua/' + page_url)

        return promo_category_element

    async def get_page_data(self, session, category: str, link) -> str:

        async with session.get(link) as resp:
            print(f'get url: {link}')
            resp_text = await resp.text()
            soup = BeautifulSoup(resp_text, 'lxml')

            cards = soup.find_all('div', class_='goods-tile ng-star-inserted')

            for item in cards:
                try:

                    price = item.find('span', class_='goods-tile__price-value').text.replace(' ', '').strip()
                    goods_name = item.find('span', class_='goods-tile__title').text.strip()

                except AttributeError:
                    print('rozetka AttributeError')
                    continue
                self.parse_dict[goods_name] = {'name': goods_name, 'price': price, 'category': category}

        return resp_text


CATEGORIES_OPTION = {
    'notebook': 'notebooks/c80004/sell_status=available;seller=rozetka/',
    'phone': 'mobile-phones/c80003/sell_status=available;seller=rozetka/',
    'powerbank': 'universalnye-mobilnye-batarei/c387969/sell_status=available;seller=rozetka/',
}


async def load_site_data(categories_name: str):
    site_option = Rozetka()
    categories_option_url = CATEGORIES_OPTION.get(categories_name)
    dict_category_list = site_option.get_pages_in_categories(categories_option_url)

    header = Headers(browser="chrome", os="win", headers=True).generate()
    async with aiohttp.ClientSession(headers=header) as session:
        tasks = []
        for category_name, url_category_list in dict_category_list.items():
            for url in url_category_list:
                task = asyncio.create_task(site_option.get_page_data(session, categories_name, url))
                tasks.append(task)
        await asyncio.gather(*tasks)
        return site_option.parse_dict
