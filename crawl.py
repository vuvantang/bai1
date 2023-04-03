import requests
from bs4 import BeautifulSoup
from models import LaptopModel
from process import Process


class Crawl:

    @staticmethod
    def get_laptop_from_url(url):
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Tìm tới khung của sản phẩm
        divs = soup.select('div.product-row')

        # Lấy các item trong khung sản phẩm
        return [LaptopModel(Process.get_product_name(div.select_one('h2.product-row-name').get_text()),
                            Process.get_brand_name(div.select_one(
                                'h2.product-row-name').get_text()),
                            Process.convert_text_to_number(
                                div.select_one('del').get_text()),
                            Process.convert_text_to_number(
                                div.select_one('span.product-row-sale').get_text()),
                            Process.convert_percent(div.select_one(
                                'div.new-product-percent').get_text()),
                            1 if div.select_one('span.ico-km') else 0)
                for div in divs]
