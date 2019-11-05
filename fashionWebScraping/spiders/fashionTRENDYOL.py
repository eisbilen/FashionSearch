import scrapy
from fashionWebScraping.items import FashionwebscrapingItem
from fashionWebScraping.items import ImgData

from scrapy.http import JSONRequest

import json

#to read from a csv file
import csv

class FashiontrendyolSpider(scrapy.Spider):
	name = 'fashionTRENDYOL'
	allowed_domains = ['trendyol.com']
	start_urls = ['http://trendyol.com/']

# This function helps us to scrape the whole content of the website 
	# by following the links in a csv file.
	def start_requests(self):

		# Read main category links from a csv file		
		with open("/Users/erdemisbilen/Angular/fashionWebScraping/csvFiles/SpiderMainCategoryLinksTRENDYOL.csv", "rU") as f:
			reader=csv.DictReader(f)
		
			for row in reader:

				url=row['url']
				# Change the offset value incrementally to navigate through the product list
				# You can play with the range value according to maximum product quantity
				link_urls = [url.format(i) for i in range(1,5)]

				
				for link_url in link_urls:
					
					print(link_url)
		


					#Pass the each link containing 100 products, to parse_product_pages function with the gender metadata
					request=JSONRequest(link_url, callback=self.parse_product_pages, meta={'gender': row['gender']})
		
					yield request

  
	# This function scrapes the page with the help of xpath provided
	def parse_product_pages(self,response):

		item=FashionwebscrapingItem()

		# Get the HTML block where all the products are listed
		# <ul> HTML element with the "products-listing small" class name
		jsonresponse = json.loads(response.text)

		
		#content=response.xpath('//div[@class="prdct-cntnr-wrppr"]')
		#print(content)
		# loop through the <li> elements with the "product-item" class name in the content
		for jsonItem in jsonresponse['result']['products']:

			print(jsonItem)
			
			image_urls = []

			# get the product details and populate the items
			item['productId']=jsonItem['id']
			item['productName']=jsonItem['name']

			
			item['priceOriginal']=str(jsonItem['price']['originalPrice'])+" TL"
			item['priceSale']=str(jsonItem['price']['discountedPrice'])+" TL"

			item['imageLink']="https://www.trendyol.com"+jsonItem['images'][0]		
			item['productLink']="https://www.trendyol.com"+jsonItem['url']
			
			image_urls.append(item['imageLink'])


			item['company']="TRENDYOL"
			item['gender']=response.meta['gender']


			yield (item)
			yield ImgData(image_urls=image_urls)

	def parse(self, response):
		pass