import scrapy
from fashionWebScraping.items import FashionwebscrapingItem
from fashionWebScraping.items import ImgData
from scrapy.http import Request

#to read from a csv file
import csv


class FashionmatmazelSpider(scrapy.Spider):
	name = 'fashionMATMAZEL'
	allowed_domains = ['matmazel.com']
	start_urls = ['http://matmazel.com/']

# This function helps us to scrape the whole content of the website 
	# by following the links in a csv file.
	def start_requests(self):

		# Read main category links from a csv file		
		with open("/Users/erdemisbilen/Angular/fashionWebScraping/csvFiles/SpiderMainCategoryLinksMATMAZEL.csv", "rU") as f:
			reader=csv.DictReader(f)
		
			for row in reader:

				url=row['url']
				# Change the offset value incrementally to navigate through the product list
				# You can play with the range value according to maximum product quantity
				link_urls = [url.format(i) for i in range(0,5)]

				
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
		content=response.xpath('//div[@class="col col-4 col-sm-6 col-xs-12 productItem ease"]')
		print(content)
		# loop through the <li> elements with the "product-item" class name in the content
		for product_content in content:

			
			image_urls = []

			# get the product details and populate the items
			item['productId']=product_content.xpath('.//div[@class="variantOverlay"]/@data-id').extract_first()
			item['productName']=product_content.xpath('.//a[@class="col col-12 productDescription detailLink"]/@title').extract_first()

			
			item['priceOriginal']=product_content.xpath('.//div[@class="discountedPrice"]/text()').extract_first()

			item['priceSale']=product_content.xpath('.//div[@class="currentPrice"]/text()').extract_first()

			

			if item['priceOriginal']==None:
				item['priceOriginal']=item['priceSale']



			item['imageLink']=product_content.xpath('.//span[@itemprop="image"]/@content').extract_first()			
			item['productLink']="https://www.matmazel.com"+product_content.xpath('.//a/@href').extract_first()
			
			image_urls.append(item['imageLink'])


			item['company']="MATMAZEL"
			item['gender']=response.meta['gender']

			
			if item['productId']==None:
				break

			yield (item)
			yield ImgData(image_urls=image_urls)

	def parse(self, response):
		pass