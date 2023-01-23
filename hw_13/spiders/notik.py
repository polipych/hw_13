import scrapy
from datetime import datetime
from scrapy.spiders import CrawlSpider
import re
from hw_13.items import CompsItem


class NotikSpider(CrawlSpider):
    name = 'notik'
    allowed_domains = ['notik.ru']
    start_urls = ["https://www.notik.ru/index/notebooks.htm?srch=true&full=&page=1"]

    default_headers = {}

    def scrap_notik(self, response):
        comps_item = CompsItem()
        for card in response.xpath("//tr[@class='goods-list-table']"):
            price_selector = card.xpath(".//td[@class='glt-cell gltc-cart']")
            price = re.findall(r'\d+', price_selector.xpath(".//b").css("::text").get())
            comps_item['price'] = int("".join(price))

            ecname = price_selector.xpath(".//a").attrib.get("ecname")
            comps_item['title'] = re.search(r'^.*?(?=\s\d{1,2}Gb(\s|\+))', ecname).group()
           
            freq = card.xpath(".//td[@class='glt-cell w4']//text()[normalize-space()]").getall()
            for i in range(len(freq)):
                freq_i = re.search(r'МГц', freq[i])
                if freq_i != None:
                    comps_item['freq_i'] = float((re.match(r'\d+', freq[i]).group()))/1000
                    break
                else:
                    i+=1
            
            comps_item['link'] = 'https://www.notik.ru' + card.xpath(".//td[@class='glt-cell gltc-title show-mob hide-desktop']//a").attrib.get("href")
            
            comps_item['ram'] = int(re.search(r'\b\d{1,2}(?=Gb (S|\dT|eM))', ecname).group())

            rom_gb = re.search(r'(?<=SSD\s|MMC\s)\d{1,3}|\d{1,2}(?=Tb\s)', ecname).group()
            if len(rom_gb) == 1:
                comps_item['rom'] = int(rom_gb) * 1024
            else:
                comps_item['rom'] = int(rom_gb)
            
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
        paginator = response.xpath("//div[@class='paginator align-left']//a").css("::text").getall()
        for i in range(1,int(paginator[-1])+1):
            next_page = f'https://www.notik.ru/index/notebooks.htm?srch=true&full=&page={i}'
            yield response.follow(next_page, callback=self.scrap_notik)