import requests
import bs4
import lxml
import collections
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('wb')

ParseResult = collections.namedtuple(
    'ParseResult',
    (
        'product_name',
        'price',
        'currency',
        'img',
        'url'
    )
)


class AlmauShop:

    def __init__(self):
        self.session = requests.Session()
        self.session.headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Mobile Safari/537.36',
            'Accept-Language': 'ru',
        }
        self.result = []

    def load_page(self):
        url = 'https://almaushop.kz'
        res = self.session.get(url)
        return res.text

    def parse_page(self, text: str):
        soup = bs4.BeautifulSoup(text, 'lxml')
        container = soup.select('div.t754__col.t-col.t-col_3.t-align_center.t-item.t754__col_mobile-grid.js-product')
        for block in container:
            self.parse_block(block=block)

    def parse_block(self, block):
        # logging.info(block)
        # logger.info('=' * 100)

        name_block = block.select_one('div.t754__title.t-name.t-name_xs.js-product-name')
        if not name_block:
            # logger.error('no name_block')
            print('error')

        price_block = block.select_one('div.t754__price-value.js-product-price')
        if not price_block:
            # logger.error('no price_block')
            print('error')

        currency_block = block.select_one('div.t754__price-currency')
        if not currency_block:
            # logger.error('no currency_block')
            print('error')
        currency_block = currency_block.text[:-1]

        img_block = block.select_one('div.t754__imgwrapper.t754__imgwrapper_mobile-nopadding')
        if not img_block:
            # logger.error('no img_block')
            print('error')
        img = img_block.select_one('img').get('data-original')

        url2 = name_block.get('field')
        url2 = url2.split('__')[1]

        url = f'https://almaushop.kz/#!/tproduct/221510661-{url2}'

        self.result.append(ParseResult(
            product_name=name_block.text,
            price=price_block.text,
            currency=currency_block,
            img=img,
            url=url
        ))

        logger.info(f'{name_block.text}, {price_block.text}, {currency_block}, {img}, {url}')

    def run(self):
        text = self.load_page()
        self.parse_page(text=text)
        # logger.info(f'Получено {len(self.result)} товаров')
        # for i in self.result:
        #     logger.info(i)
        #     logger.info(i.product_name)


def main():
    shop = AlmauShop()
    shop.run()


if __name__ == '__main__':
    main()
