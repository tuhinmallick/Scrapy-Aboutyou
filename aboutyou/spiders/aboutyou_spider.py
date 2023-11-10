import scrapy
import os
from urllib.parse import urlencode
from scrapy.crawler import CrawlerProcess


class AboutyouSpider(scrapy.Spider):
    name = 'aboutyou'
    download_delay = 10
    custom_settings = {'FEEDS': {'results.csv': {'format': 'csv'}}}
    allowed_domains = ['aboutyou.ro']
    start_urls = ['https://www.aboutyou.ro/barbati/haine/geci']
    headers = {
        'cache-control': 'no-cache',
        'referer': 'https://www.aboutyou.ro/barbati/haine/geci',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0'
    }

    params = {
        'page': 1,
        'sort': 'topseller'
    }

    try:
        os.remove('results.csv')
    except OSError:
        pass

    def __init__(self):
        self.page = 1
        self.base_url = 'https://www.aboutyou.ro/barbati/haine/geci?'

    def parse(self, response):

        listing = response.xpath('//*[contains(@class, "sc-1qheze-0 gsZQBd")]')

        for jackets in listing:
            title = jackets.xpath('.//*[contains(@class, "sc-1gv4rhx-2 dHHtsu")]/text()').get()
            price1 = jackets.xpath('.//*[contains(@class, "sc-1kqkfaq-0 x3voc9-0 hAXkjt")]/text()').get()
            price2 = jackets.xpath('.//*[contains(@class, "sc-1kqkfaq-0 x3voc9-0 eBbsYV")]/text()').get()

            try:
                global size
                size = jackets.xpath('.//span[@class="sc-1gv4rhx-6 dIpfJe"]/text()')[3].get()
            except:
                pass

            jacket_img = jackets.xpath('//div[@class="sc-1kws8ub-0 dsjkVe"]/img/@src').get()

            yield dict(
                title=title,
                price1=price1,
                price2=price2,
                size=size,
                jacket_img=jacket_img,
            )
        # next page if exits
        self.params['page'] += self.page
        self.params['sort'] = str(self.params['page'])

        next_url = self.base_url + urlencode(self.params)

        if response.xpath('//li[@class="pageNumbers"]/a/text()').get() == 2 or 3:
            yield response.follow(next_url, headers=self.headers, callback=self.parse)


if __name__ == "__main__":
    process = CrawlerProcess()
    process.crawl(AboutyouSpider)
    process.start()
