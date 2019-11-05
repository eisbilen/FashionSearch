import scrapy
from fashionWebScraping.items import FashionwebscrapingItem
from fashionWebScraping.items import ImgData
from scrapy.http import Request
from scrapy.selector import Selector

#to read from a csv file
import csv

class FashionkotonSpider(scrapy.Spider):
	name = 'fashionKOTON'
	allowed_domains = ['www.koton.com']
	start_urls = ['http://www.koton.com/']

	def start_requests(self):

		with open("/Users/erdemisbilen/Angular/fashionWebScraping/csvFiles/SpiderMainCategoryLinksKOTON.csv", "rU") as f:
			reader=csv.DictReader(f)
		
			for row in reader:

				url=row['url'].split()
				print(url)
				request=Request(row['url'], callback=self.parse_product_pages, meta={'gender': row['gender']})
				
				yield request


	def parse_product_pages(self,response):
		max_page_numbers=response.xpath('//div[@class="paging"]//li/a/text()').extract()

		print(max_page_numbers)

		print(response.meta['gender'])

		pageList=[]

		for max_page_number in max_page_numbers:
			
			print(max_page_number)
			
			try:
				
				pageList.append(int(max_page_number))
				
			except ValueError:
				print("hata")
				pass      # or whatever		

		print(pageList)
		
		if pageList:
			max_page_number_one = max(pageList)
		else:
			max_page_number_one=0

		print(max_page_number_one)

		link_urls=[response.request.url+'?q=%3Arelevance&psize=192&page={}'.format(i) for i in range(0,max_page_number_one)]

		for link_url in link_urls:
			print(link_url)
			yield response.follow(link_url, callback=self.parse, meta={'gender': response.meta['gender']})



	def parse(self, response):

		item=FashionwebscrapingItem()
		
		sel = Selector(text=response.body)

		fullContent=sel.xpath('//div[@class="product-item plp-large-images"]')
			

		for content in fullContent:

			image_urls = []
			
			item['company']="KOTON"
			item['gender']=response.meta['gender']
			item['productName']=content.xpath('@data-name').extract_first()
			item['imageLink']=content.xpath('.//div[@class="swiper-slide"]/img/@data-src').extract_first()
			item['productLink']="https://www.koton.com"+content.xpath('.//a/@href').extract_first()
			
			image_urls.append(item['imageLink'])


			item['priceOriginal']=content.xpath('.//span[@class="firstPrice"]/text()').extract_first()
			item['priceSale']=content.xpath('.//span[@class="firstPrice"]/text()').extract_first()
			
			if item['priceOriginal']==None:
				item['priceOriginal']=content.xpath('.//span[@class="insteadPrice"]/s/text()').extract_first()
				item['priceSale']=content.xpath('.//span[@class="newPrice"]/text()').extract_first()
				
			item['productId']=content.xpath('.//div[@class="my-fav-icon"]/@data-product').extract_first()
			
			if item['productId']!= None:
				yield (item)
				yield ImgData(image_urls=image_urls)
