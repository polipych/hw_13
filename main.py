from hw_13.spiders.notik import NotikSpider
from hw_13.spiders.e2e4 import E2E4Spider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


def main():
    settings = get_project_settings()
    process = CrawlerProcess(settings)
    process.crawl(NotikSpider)
    process.crawl(E2E4Spider)
    process.start()

if __name__ == "__main__":
    main()