import scrapy

from scrapy.loader import ItemLoader

from ..items import ElavonplItem
from itemloaders.processors import TakeFirst


class ElavonplSpider(scrapy.Spider):
	name = 'elavonpl'
	start_urls = ['https://www.elavon.pl/aktualnosci.html']

	def parse(self, response):
		post_links = response.xpath('//h5/a/@href')
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		title = response.xpath('//h1//text()').get()
		description = response.xpath(
			'//div[@class="news-article-content"]//div[@class="text aem-GridColumn aem-GridColumn--default--12"]//text()').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//time/text()').get()

		item = ItemLoader(item=ElavonplItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
