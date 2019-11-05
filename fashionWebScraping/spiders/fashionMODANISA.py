import scrapy
from fashionWebScraping.items import FashionwebscrapingItem
from fashionWebScraping.items import ImgData
from scrapy.http import Request

#to read from a csv file
import csv

class FashionmodanisaSpider(scrapy.Spider):
	name = 'fashionMODANISA'
	allowed_domains = ['modanisa.com']
	start_urls = ['http://modanisa.com/']

# This function helps us to scrape the whole content of the website 
	# by following the links in a csv file.
	def start_requests(self):

		# Read main category links from a csv file		
		with open("/Users/erdemisbilen/Angular/fashionWebScraping/csvFiles/SpiderMainCategoryLinksMODANISA.csv", "rU") as f:
			reader=csv.DictReader(f)
		
			for row in reader:

				url=row['url']
				# Change the offset value incrementally to navigate through the product list
				# You can play with the range value according to maximum product quantity
				link_urls = [url.format(i) for i in range(1,3)]

				
				for link_url in link_urls:
					
					print(link_url)



					#Pass the each link containing 100 products, to parse_product_pages function with the gender metadata
					request=Request(link_url, callback=self.parse_product_pages, meta={'gender': row['gender'],'dont_redirect': False})
		
					yield request

  
	# This function scrapes the page with the help of xpath provided
	def parse_product_pages(self,response):

		item=FashionwebscrapingItem()

		

		# Get the HTML block where all the products are listed
		# <ul> HTML element with the "products-listing small" class name
		content=response.xpath('//ul[@id="productsList"]')

		# loop through the <li> elements with the "product-item" class name in the content
		for product_content in content.xpath('.//li'):
		
			image_urls = []

			# get the product details and populate the items
			item['productId']=product_content.xpath('.//a/@data-product-id').extract_first()
			item['productName']=product_content.xpath('.//a/@data-product-name').extract_first()

			item['priceSale']=product_content.xpath('.//a/@data-product-price').extract_first()

			item['priceOriginal']=product_content.xpath('.//p[@class="price"]/del/text()').extract_first()


			if item['priceOriginal']==None:
				item['priceOriginal']=item['priceSale']



			item['imageLink']=product_content.xpath('.//img/@data-original').extract_first()		
			if item['imageLink']==None:
				item['imageLink']=product_content.xpath('.//img/@src').extract_first()

			item['productLink']=product_content.xpath('.//a[@class="productClickClass"]/@href').extract_first()
			
			image_urls.append(item['imageLink'])


			item['company']="MODANISA"
			item['gender']=response.meta['gender']

			
			if item['productId']==None:
				break


			yield (item)
			yield ImgData(image_urls=image_urls)

	def make_requests_from_url(self, url):
		return Request(url, dont_filter=True, meta = {'dont_redirect': True,'handle_httpstatus_list': [301,302]})


	def parse(self, response):
		pass
