from datetime import datetime

import bs4
import scrapy
from scrapy.crawler import CrawlerProcess

# from drugbank.items import ActionItem, DrugItem, ExternalIdentifierItem, TargetItem

SCRAPED_AT = datetime.utcnow()

URL_PAGINATE = 'https://go.drugbank.com/drugs?approved=0&c=name&ca=0&d=up&eu=0&experimental=0&illicit=0&investigational=0&nutraceutical=0&page={page}&us=0&withdrawn=0'
pages = [URL_PAGINATE.format(page=i) for i in range(1, 481)]


from scrapy.item import Field, Item


class BrandNamePrescriptionProducts(Item):
    name = Field()
    lebeller = Field()
    marketing_start = Field()
    marketing_end = Field()

class DrugItem(Item):
    generic_name = Field()
    access_number = Field()
    smiles = Field()
    brands = BrandNamePrescriptionProducts()




# process = CrawlerProcess(settings={
#     "FEEDS": {
#         "file.csv": {"format": "csv"},
#     },
# })

# class GetAllDrugsSpider(scrapy.Spider):
#     name='blah'
#     start_urls = pages

#     def parse(self, response):
#         rows = response.xpath('//*[@id="drugs-table"]/tbody/tr')
#         # print(table)
#         # rows = table.xpath('//tr')
#         for row in rows[1:]:
#             href = row.xpath('td[1]/strong/a/@href').get()
#             yield {'id': href.split('/')[-1]}




# process.crawl(GetAllDrugsSpider)
# process.start() 



# ------------------------------------------------

def ids():
    with open('file.csv') as f:
        yield from f.readlines()
    
print(len(list(ids())))

class DrugSpider(scrapy.Spider):
    name = "drug"
    allowed_domains = ["drugbank.ca"]
    # start_urls = [
    #     'https://go.drugbank.com/drugs/DB09095'
    # ]
    start_urls = [
        "https://www.drugbank.ca/drugs/{0}".format(id) for id in ids()
    ]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.counter = 0

    def parse(self, response):
        html = response.xpath('/html/body/main/div/div/div[2]/div[2]')[0]

        text = html.extract()
        text = bs4.BeautifulSoup(text).get_text()
        with open(f"{self.counter}.txt", 'w') as f:
            f.write(text)
        with open('index.txt', 'a') as f:
            f.write(f'{response.url}\n')
        self.counter += 1
        

process = CrawlerProcess(settings={
    # "FEEDS": {
    #     "res.txt": {"format": "txt"},
    # },
})

process.crawl(DrugSpider)
process.start()

    