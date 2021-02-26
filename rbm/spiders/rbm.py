import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst
from datetime import datetime
from rbm.items import Article


class RbmSpider(scrapy.Spider):
    name = 'rbm'
    start_urls = ['https://www.rbm.ch/rbm']

    def parse(self, response):
        links = response.xpath('//a[@class="content-hub-tile-link"]/@href').getall()
        yield from response.follow_all(links, self.parse_article)


    def parse_article(self, response):
        if 'pdf' in response.url:
            return

        item = ItemLoader(Article())
        item.default_output_processor = TakeFirst()

        title = response.xpath('//h2[@class="font-weight-bold"]//text()').get() or \
                response.xpath('//h3[@class="font-weight-bold"]//text()').get()
        if title:
            title = title.strip()

        content = response.xpath('//div[@class="portlet-boundary portlet-boundary_com_liferay_journal_content_web_portlet_JournalContentPortlet_ portlet-static portlet-static-end portlet-margin-bottom-80 portlet-journal-content "]//text()').getall()
        content = [text for text in content if text.strip()]
        content = "\n".join(content).strip()

        item.add_value('title', title)
        item.add_value('link', response.url)
        item.add_value('content', content)

        return item.load_item()
