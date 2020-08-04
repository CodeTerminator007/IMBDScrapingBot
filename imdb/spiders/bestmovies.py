# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import unicodedata

class BestmoviesSpider(CrawlSpider):
    name = 'bestmovies'
    allowed_domains = ['imdb.com']
    start_urls = ['https://www.imdb.com/search/title/?genres=drama&groups=top_250&sort=user_rating,desc']

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//h3[@class="lister-item-header"]/a'), callback='parse_item', follow=True),
        Rule(LinkExtractor(restrict_xpaths='(//a[@class="lister-page-next next-page"])[1]')),


        
    )

    def parse_item(self, response):
         title = response.xpath('//div[@class="title_wrapper"]/h1/text()').get()  #to remove the unicode  
         clean_text = unicodedata.normalize("NFKD",title)
         
         yield {
             'Title' : clean_text ,
             'Year' : response.xpath('//span[@id="titleYear"]/a/text()').get(),
             'Duration' : response.xpath('normalize-space((//time)[1]/text())').get(),
             'Ratting' : response.xpath('//div[@class="ratingValue"]/strong/span/text()').get(),
             'link' : response.url
           
           }