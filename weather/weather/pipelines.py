# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


import json
import pymysql

class WeatherPipeline(object):
    def __init__(self):
        self.file = open('weather.txt','a',encoding='utf-8')
    def process_item(self, item, spider):
        self.file.write(item['date']+'\n')
        self.file.write(item['week']+'\n')
        self.file.write(item['weather']+'\n')
        self.file.write(item['wind']+'\n')
        return item
    def close_spider(self,spider):
        self.file.close()
class Weatherjson(object):
    def __init__(self):
        self.file = open('weather.json','a',encoding='utf-8')
    def process_item(self, item, spider):
        line = json.dumps(dict(item),ensure_ascii=False)+'\n'
        self.file.write(line)
        return item
    def close_spider(self,spider):
        self.file.close()

class Weathermysql(object):
    def process_item(self,item,spider):
        date = item['date']
        week = item['week']
        #temperature = item['temperature']
        weather = item['weather']
        wind = item['wind']
        #img = item['img']
        connection = pymysql.connect(
            host='localhost',
            user='root',
            passwd='root',
            db='scrapyDB',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor)

        try:
            with connection.cursor() as cursor:
                sql = """INSERT INTO WEATHER(date,week,weather,wind)
                values (%s,%s,%s,%s)"""
                cursor.execute(
                    sql,(date,week,weather,wind))
            connection.commit()
        finally:
            connection.close()
        return item