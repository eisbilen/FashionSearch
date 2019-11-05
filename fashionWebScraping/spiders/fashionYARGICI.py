import scrapy
from fashionWebScraping.items import FashionwebscrapingItem
from fashionWebScraping.items import ImgData
from scrapy.http import Request

#to read from a csv file
import csv

class FashionyargiciSpider(scrapy.Spider):
	name = 'fashionYARGICI'
	allowed_domains = ['yargici.com']
	start_urls = ['http://yargici.com/']

	# This function helps us to scrape the whole content of the website 
	# by following the links in a csv file.
	def start_requests(self):

		# Read main category links from a csv file		
		with open("/Users/erdemisbilen/Angular/fashionWebScraping/csvFiles/SpiderMainCategoryLinksYARGICI.csv", "rU") as f:
			reader=csv.DictReader(f)
		
			for row in reader:

				url=row['url']
				# Change the offset value incrementally to navigate through the product list
				# You can play with the range value according to maximum product quantity
				link_urls = [url.format(i) for i in range(1,4)]

				
				for link_url in link_urls:
					
					print(link_url)

					#Pass the each link containing 100 products, to parse_product_pages function with the gender metadata
					request=Request(link_url, callback=self.parse_product_pages, meta={'gender': row['gender']})
		
					yield request

  
	# This function scrapes the page with the help of xpath provided
	def parse_product_pages(self,response):

		item=FashionwebscrapingItem()

		# Get the HTML block where all the products are listed
		# <ul> HTML element with the "products-listing small" class name
		content=response.xpath('//div[@class="row"]')
		
		# loop through the <li> elements with the "product-item" class name in the content
		for product_content in content.xpath('.//div[@class="col-6 col-xs-6 col-sm-6 col-md-4 col-lg-4 col-xl-4 product-grid-item-container p-0"]'):
		

			image_urls = []

			# get the product details and populate the items
			item['productId']=product_content.xpath('.//a/@data-fav-check').extract_first()
			item['productName']=product_content.xpath('.//img/@alt').extract_first()

			
			item['priceOriginal']=product_content.xpath('.//li[@class="list-inline-item mr-0"]/s/text()').extract_first()

			item['priceSale']=product_content.xpath('.//li[@class="list-inline-item"]/span/text()').extract_first()


			if item['priceOriginal']==None:
				item['priceOriginal']=item['priceSale']


			item['imageLink']=product_content.xpath('.//img/@data-original').extract_first()			
			item['productLink']="https://www.yargici.com"+product_content.xpath('.//a/@href').extract_first()
			
			image_urls.append(item['imageLink'])


			item['company']="YARGICI"
			item['gender']=response.meta['gender']

			
			if item['productId']==None:
				break


			yield (item)
			yield ImgData(image_urls=image_urls)

	def parse(self, response):
		pass

