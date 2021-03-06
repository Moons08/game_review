import scrapy
import numpy as np
from crawler.items import CrawlerItem

class MakeError(Exception):

    def __str__(self):
        return "self check"

class C_Spider(scrapy.Spider):
    name = "critic"
    allow_domain = ["metacritic.com"]

    def start_requests(self):
        for i in range(0, 15+1):
            url = "http://www.metacritic.com/browse/games/release-date/available/ps4/date" + "?page={}".format(i)
            yield scrapy.Request(url, self.parse)

    def parse(self, response):
        games = response.xpath('//*[@id="main"]/div[1]/div[2]/div[3]/div/ol/li')

        for game in games:
            link = 'http://www.metacritic.com'+game.xpath('./div/div[@class="basic_stat product_title"]/a/@href').extract()[0] + '/critic-reviews'

            yield scrapy.Request(link, callback=self.parse_page_contents)

    def parse_page_contents(self, response):
        item = CrawlerItem()
        title = response.xpath('//*[@id="main"]/div[1]/div[2]/a/h1/text()')[0].extract()
        reviews = response.xpath('//*[@id="main"]/div[5]/div/ol/li')

        for review in reviews:

            item["title"] = title
            try:
                item["id"] = review.xpath('./div/div/div/div/div/div[1]/div[1]/div[1]/div[1]/a/text()')[0].extract()

            except:
                item["id"] = review.xpath('./div/div/div/div/div/div[1]/div[1]/div[1]/div[1]/a/text()').extract()

                if not item["id"]:
                    try:
                        item["id"] = review.xpath('./div/div/div/div/div/div[1]/div[1]/div[1]/div[1]/text()')[0].extract()
                    except:
                        item["id"] = review.xpath('./div/div/div/div/div/div[1]/div[1]/div[1]/div[1]/text()').extract()

            try:
                item["score"] = review.xpath('./div/div/div/div/ div/div[1]/div[1]/div[2]/div/text()')[0].extract()

            except:
                item["score"] = review.xpath('./div/div/div/div/ div/div[1]/div[1]/div[2]/div/text()').extract()

            try:
                item["review"] = review.xpath('./div/div/div/div/div/div[1]/div[2]/text()')[0].extract()
            except:
                item["review"] = review.xpath('./div/div/div/div/div/div[1]/div[2]/text()').extract()

            yield item

class Spider(scrapy.Spider):
    name = "user"
    allow_domain = ["metacritic.com"]

    def start_requests(self):
        for i in range(0, 15+1):
            url = "http://www.metacritic.com/browse/games/release-date/available/ps4/date" + "?page={}".format(i)
            yield scrapy.Request(url, self.parse)

    def parse(self, response):
        games = response.xpath('//*[@id="main"]/div[1]/div[2]/div[3]/div/ol/li')

        for game in games:
            link = 'http://www.metacritic.com'+game.xpath('./div/div[@class="basic_stat product_title"]/a/@href').extract()[0] + '/user-reviews?sort-by=most-helpful&num_items=100'

            yield scrapy.Request(link, callback=self.parse_page_contents)

    def parse_page_contents(self, response):
        item = CrawlerItem()
        title = response.xpath('//*[@id="main"]/div[1]/div[2]/a/h1/text()')[0].extract()
        reviews = response.xpath('//*[@id="main"]/div[5]/div[2]/div/ol/li')

        for review in reviews:

            item["title"] = title

            try:
                item["id"] = review.xpath('./div/div/div/div/div/div[1]/div[1]/div[1]/div[1]/a/text()')[0].extract()
                if not item["id"]:
                    raise MakeError()
            except:
                item["id"] = review.xpath('./div/div/div/div/div/div[1]/div[1]/div[1]/div[1]/text()')[0].extract()

            item["score"] = review.xpath('./div/div/div/div/ div/div[1]/div[1]/div[2]/div/text()')[0].extract()

            try:
                tmp = review.xpath('./div/div/div/div/div/div[1]/div[2]/span/span[1]/text()').extract()
                item["review"] = ''.join(tmp) #for muliple lines

                if not tmp: #for spoliers lines
                    tmp = review.xpath('./div/div/div/div/div/div[1]/div[2]/span/span[2]/text()').extract()
                    item["review"] = ''.join(tmp)

                    if not tmp:
                        raise MakeError()
            except:
                tmp = review.xpath('./div/div/div/div/div/div[1]/div[2]/span/text()').extract()
                item["review"] = ''.join(tmp)

            yield item

class U_Spider(scrapy.Spider):
    name = "user_detail"
    allow_domain = ["metacritic.com"]

    def start_requests(self):
        userid = np.load('/home/mk/documents/dev/game_review/data/user_id.npy')
        for id in userid:
            url = "http://www.metacritic.com/user/" + id + "?myscore-filter=Game"
            yield scrapy.Request(url, self.parse)

    def parse(self, response):
        try:
            last_page = response.xpath('//*[@id="main"]/div[3]/div/div[2]/div/div/div[2]/ul/li[last()]/a/text()')[0].extract()
            for i in range(0, int(last_page)):
                url = response.url + "&page=" + "{}".format(i)
                yield scrapy.Request(url, self.parse_page_contents)

        except:
            url = response.url
            yield scrapy.Request(url, self.parse_page_contents, dont_filter=True)

    def parse_page_contents(self, response):
        item = CrawlerItem()
        id_ = response.xpath('//*[@id="main"]/div[1]/div/div[2]/h2/text()')[0].extract()

        reviews = response.xpath('//*[@id="main"]/div[3]/div/div[2]/ol/li')

        for review in reviews:

            item["title"] = review.xpath('./div/div/div/div/div/div[1]/div[1]/div[1]/div[1]/a/text()')[0].extract()

            item["id"] = id_

            item["score"] = review.xpath('./div/div/div/div/div/div[1]/div[1]/div[2]/div/text()')[0].extract()

            try:
                tmp = review.xpath('./div/div/div/div/div/div[1]/div[3]/span/span[2]/text()').extract()
                item["review"] = ''.join(tmp)
                if not tmp:
                    raise MakeError()
            except:
                tmp = review.xpath('./div/div/div/div/div/div[1]/div[3]/span/text()').extract()
                item["review"] = ''.join(tmp)

            yield item
