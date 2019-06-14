# -*- coding: utf-8 -*-
import scrapy
from weather.items import WeatherItem

class SztianqiSpider(scrapy.Spider):
    name = 'SZtianqi'
    allowed_domains = ['tianqi.com']
    start_urls = []
    citys = ['nanjing','suzhou','shanghai']
    for city in citys:
        start_urls.append('https://'+city+'.tianqi.com')

    def parse(self, response):
        items = []
        dayseven = response.xpath('//div[@class="day7"]')
        item = WeatherItem()
        for i in range(1,8):
            date = dayseven.xpath('./ul[1]/li['+str(i)+']/b/text()').extract()[0]
            week = dayseven.xpath('./ul[1]/li['+str(i)+']/span/text()').extract()[0]
            #temperature = dayseven.xpath('./ul[3]/li['+str(i)+']/span/text()').extract()[0]
            weather = dayseven.xpath('./ul[2]/li['+str(i)+']/text()').extract()[0]
            wind = dayseven.xpath('./ul[3]/li['+str(i)+']/text()').extract()[0]
            item['date'] = date
            item['week'] = week
            #item['temperature'] = temperature
            item['weather'] = weather
            item['wind'] = wind
            
            items.append(item)
        return items