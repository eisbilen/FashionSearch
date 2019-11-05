
import scrapy
from scrapy.item import Item, Field

class FashionwebscrapingItem(scrapy.Item):
 
    #product related items
    gender=Field()
    productId=Field()
    productName=Field()
    priceOriginal=Field()
    priceSale=Field()

    #items to store links 
    imageLink = Field()
    productLink=Field()

    #item for company name
    company = Field()

    #items for image pipeline
    #image_urls = scrapy.Field()
    #images = scrapy.Field()


    pass

class ImgData(Item):
    image_urls=scrapy.Field()
    images=scrapy.Field()
