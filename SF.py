import requests
import urllib.parse
from bs4 import BeautifulSoup
from impl_parser import Parser


class SFParser(Parser):
	def __init__(self):
		self.cookies = {}
		self.siteroot = 'https://www.saintalfred.com'

		super().__init__()

	def __set_cookies(self, response: requests.Response) -> None:
		self.cookies.update(response.cookies.get_dict())

	def get_by_url(self, url: str, size: int):

		import json
		soup, response = self.get_data(url)
		self.__set_cookies(response)
	
		product_id_in_system = soup.find_all('select', attrs={'class': 'single-option-selector'})[0].attrs['data-option-select']
		find_goods_json_data = soup.find_all('script', attrs={'type': 'application/json', f'data-product-json-{product_id_in_system}': True})
		get_goods_json_data = json.loads(str(find_goods_json_data[0])[67:-9])

		# В дальнейшем отсюда можно получить всю информацию по каждому размеру товара
		goods_variants = get_goods_json_data['variants']

		for good in goods_variants:
			# Здесь можно получить SKU через good['sku']
			size_variant = process_size(good["title"])
			if size_variant == str(size):

				print(f' # id: {good["id"]} | size: {size_variant}')
				return good["id"]

		return None


	def get_by_sku(self, sku: str): pass
		#SKU получен через массив JSON данных в get_by_url()

	def get_by_keyword(self, keyword: str):

		url = f'{self.siteroot}/search?q={keyword}'
		soup, response = self.get_data(url)
		print('rer', response.url)
		self.__set_cookies(response)

		# Находим все товары по запросу и создаем из них массив для дальнейшего использования в поисковике приложения
		products_soup = soup.find_all("h3", attrs={"class": "product-list-item-title"})
		products = [{'name': product.text, 'link': f'{self.siteroot}/{product.findNext().attrs["href"]}'} for product in products_soup]

		return products


	def add_to_cart(self, variant_id):

		data = {
			'id': variant_id
		}

		post_response = self.post_data(f'{self.siteroot}/cart/add.js', self.siteroot, data=data)
		post_response.cookies.update(self.cookies)

	def get_login_page(self):

		url = f'{self.siteroot}/checkout'
		soup, response = self.get_data(url)
		self.__set_cookies(response)

		return response.url

	def login(self, checkout_url, email, password):

		data = {
			'form_type': 'customer_login',
			'utf8': '\u2713',
			'customer[email]': email,
			'customer[password]': password,
			'checkout_url': checkout_url
		}

		post_response = self.post_data(f'{self.siteroot}/account/login', self.siteroot, data=data)
		post_response.cookies.update(self.cookies)

		print(post_response.headers)

# Функция для получения размера товара из строки
def process_size(size):
	import re

	if re.fullmatch(r'.+ / .+', size): size = size.split()[0]
	if size.isdigit(): return size
	result = re.findall(r'\d{1,2}.\d{1,2}' or r'\d{1,2}', size)[0]
	return result

def get_checkout_url(login_page):
    return login_page[55:].replace('%2F', '/').replace('%3A', '/')


def start_SF(search_key):
	process = SFParser()

	# Ссылка на первый товар по ключу
	product_link = process.get_by_keyword(search_key)[0]['link']

	# Вариант id для добавления в корзину, полченный по размеру товара
	variant_id = process.get_by_url(product_link, 5)
	add = process.add_to_cart(variant_id)

	# Получение уникальной страницы авторизации
	login_page = process.get_login_page()

	# Авторизация
	checkout_url = get_checkout_url(login_page)
	process.login(checkout_url, 'test@gmail.com', 'q123w456')
	
	# После авторизации ведет на страницу капчи
	# Нужно пройти капчу и продолжить


if __name__ == '__main__':
	start_SF('AIR MAX')