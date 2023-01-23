import scrapy
from datetime import datetime
from scrapy.spiders import CrawlSpider
import re
from hw_13.items import CompsItem


class E2E4Spider(CrawlSpider):
    name = 'e2e4'
    allowed_domains = ['moscow.e2e4online.ru']
    start_urls = ["https://moscow.e2e4online.ru/catalog/noutbuki-42/?page=1"]

    default_headers = {}

    def scrap_e2e4(self, response):
        comps_item = CompsItem()
        for card in response.xpath("//div[@class='block-offer-item subcategory-new-offers__item-block']"):
            price_selector = card.xpath(".//div[@class='price-block__price _WAIT']")
            if price_selector != []:
                price = re.findall(r'\d+', price_selector.xpath(".//span").css("::text").get())
            else:
                price_selector = card.xpath(".//div[@class='price-block__price _OK']")
                price = re.findall(r'\d+', price_selector.xpath(".//span").css("::text").get())
            comps_item['price'] = int("".join(price))

            comps_item['title'] = card.xpath(".//div[@class='block-offer-item__head-info']").css("::text").get()
            
            comps_item['link'] = 'https://moscow.e2e4online.ru' + card.xpath(".//div[@class='block-offer-item__head-info']//a").attrib.get("href")
            
            ecname = card.xpath(".//div[@class='block-offer-item__description lg-and-up']").css("::text").get()

            freq = re.search(r'((\d\.\d)|(\d))(?=GHz)', ecname)
            if freq != None:
                comps_item['freq_i'] = float(freq.group(0))
            else:
                comps_item['freq_i'] = 0

            ram_gb = re.search(r'\d+(?=Gb\sR)', ecname)
            comps_item['ram'] = int(ram_gb.group(0))

            rom_gb = re.search(r'\d+(?=(G|T)b\s(S|e|H))', ecname)
            if len(rom_gb.group()) == 1:
                comps_item['rom'] = int(rom_gb.group()) * 1024
            else:
                comps_item['rom'] = int(rom_gb.group())

            comps_item['timestamp'] = datetime.utcnow()
            
            if comps_item['ram'] >= 4 and comps_item['ram'] < 8:
                rank_ram = comps_item['ram'] * 4.6
            elif comps_item['ram'] >= 8 and comps_item['ram'] < 12:
                rank_ram = comps_item['ram'] * 5.2
            elif comps_item['ram'] >= 12 and comps_item['ram'] < 16:
                rank_ram = comps_item['ram'] * 5.8
            elif comps_item['ram'] >= 16 and comps_item['ram'] < 32:
                rank_ram = comps_item['ram'] * 6.2
            else:
                rank_ram = comps_item['ram'] * 6.6

            if comps_item['rom'] >= 128 and comps_item['rom'] < 256:
                rank_rom = comps_item['rom'] * 0.0046
            elif comps_item['rom'] >= 256 and comps_item['rom'] < 512:
                rank_rom = comps_item['rom'] * 0.0056
            elif comps_item['rom'] >= 512 and comps_item['rom'] < 1024:
                rank_rom = comps_item['rom'] * 0.0066
            elif comps_item['rom'] >= 1024 and comps_item['rom'] < 2048:
                rank_rom = comps_item['rom'] * 0.0076
            else:
                rank_rom = comps_item['rom'] * 0.0086

            comps_item['rank'] = round(rank_ram + rank_rom - comps_item['price'] * 0.0001, 2)

            yield comps_item

    def parse_start_url(self, response, **kwargs):
        for i in range(1,9):
            next_page = f'https://moscow.e2e4online.ru/catalog/noutbuki-42/?page={i}'
            yield response.follow(next_page, callback=self.scrap_e2e4)