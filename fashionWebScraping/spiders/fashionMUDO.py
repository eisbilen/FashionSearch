import scrapy
from fashionWebScraping.items import FashionwebscrapingItem
from fashionWebScraping.items import ImgData
from scrapy.http import Request

#to read from a csv file
import csv


class FashionmudoSpider(scrapy.Spider):
	name = 'fashionMUDO'
	allowed_domains = ['mudo.com']
	start_urls = ['http://mudo.com/']

	# This function helps us to scrape the whole content of the website 
	# by following the links in a csv file.
	def start_requests(self):

		# Read main category links from a csv file		
		with open("/Users/erdemisbilen/Angular/fashionWebScraping/csvFiles/SpiderMainCategoryLinksMUDO.csv", "rU") as f:
			reader=csv.DictReader(f)
		
			for row in reader:

				url=row['url']
				# Change the offset value incrementally to navigate through the product list
				# You can play with the range value according to maximum product quantity
				link_urls = [url.format(i) for i in range(1,2)]

				
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
		content=response.xpath('//div[@class="list-content"]')

		
		# loop through the <li> elements with the "product-item" class name in the content
		for product_content in content.xpath('.//div[starts-with(@class,"product-item-wrapper")]'):
		

			image_urls = []

			
			# get the product details and populate the items
			item['productId']=product_content.xpath('.//div[@class="product__favourite-button js-toggle-favourite"]/@data-stockid').extract_first()
			item['productName']=product_content.xpath('.//p[@class="product-name"]/a/text()').extract_first()	

			
			item['priceOriginal']=product_content.xpath('.//span[@class="product-list-price"]/text()').extract_first()

			item['priceSale']=product_content.xpath('.//span[@class="product-sale-price"]/text()').extract_first()


			if item['priceOriginal']==None:
				item['priceOriginal']=item['priceSale']


			item['imageLink']=product_content.xpath('.//img[@class="product-item-image"]/@src').extract_first()			
			item['productLink']="https://www.mudo.com"+product_content.xpath('.//p[@class="product-name"]/a/@href').extract_first()
			
			image_urls.append(item['imageLink'])


			item['company']="MUDO"
			item['gender']=response.meta['gender']

			
			if item['productId']==None:
				break


			yield (item)
			yield ImgData(image_urls=image_urls)

	def parse(self, response):
		pass