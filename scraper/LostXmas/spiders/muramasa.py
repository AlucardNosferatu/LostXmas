# -*- coding: utf-8 -*-
import scrapy
from LostXmas.items import LostxmasItem
import datetime
import pickle
import time
import csv


class MuramasaSpider(scrapy.Spider):
    name = 'muramasa'
    allowed_domains = ['www.bijianshang.com']
#    start_urls = ['http://www.bijianshang.com/news/class/?100.html']
    start_urls = ['http://www.bijianshang.com/news/html/?3076.html']
    
    def parse(self, response):
#        filename = "teacher.html"
#        open(filename, 'w').write(response.body)#把response.body写入html文件
#        for con in response.xpath("//div[@class='title']/a"):
##      ../../news/html/?2896.html
#            if con.xpath('@href').extract_first():
#                url = "http://www.bijianshang.com/"+str(con.xpath('@href').extract_first()).strip("../../")
#                yield scrapy.Request(url, callback=self.parse_page)
#                
#    def parse_page(self,response):
        now_time = datetime.datetime.now()
        now_str = datetime.datetime.strftime(now_time,'%Y-%m-%d-%H-%M-%S')
        items = []
            
        for each in response.xpath("//font/b/span/font"):
            item = LostxmasItem()
            name = each.xpath("text()").extract()
            item['name']=name[0]
            items.append(item)
            
        i=0
        for each in response.xpath("//font/span[1]/font"):
            title = each.xpath("text()").extract()
            items[i]['title']=title[0]
            i+=1
#        i=0
#        for each in response.xpath(""):
##            info = each.xpath("text()").extract()
##            items[i]['info']=info[0]
##            i+=1            
#        with open(now_str + '.pkl', 'wb') as f:
#            pickle.dump(items, f, pickle.HIGHEST_PROTOCOL)
            
#        with open(now_str + '.csv','wb') as myFile:      
#            myWriter=csv.writer(myFile)
#            for each in items:
#                myWriter.writerow([each['name'].decode('unicode-escape'),each['title'].decode('unicode-escape')])
#            myFile.close()
        
            
            
        return items
#        time.sleep(5)
#        with open(now_str+".csv", "wb") as csvFile:
#            csvWriter = csv.writer(csvFile)
#            for k,v in items.iteritems():
#                csvWriter.writerow([k,v])
#            csvFile.close()
#        
        
    