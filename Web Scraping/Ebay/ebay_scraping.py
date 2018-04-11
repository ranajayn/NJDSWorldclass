import sys
from lxml import html
import requests
from unicodecsv import csv
import pandas as pd
import time
arguments = len(sys.argv) - 1
position = 1

while arguments >= position:
    print(sys.argv[position])
    brand = sys.argv[position]
    for i in range(5):
        try:
            url = 'http://www.ebay.com/sch/i.html?_nkw={0}&_sacat=0'.format(brand)
            headers = {
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}
            #print("Retrieving %s" % url)
            response = requests.get(url, headers=headers, verify=False)
            #print("Parsing page")
            parser = html.fromstring(response.text)
            product_listings = parser.xpath('//li[contains(@class,"lvresult")]')
            raw_result_count = parser.xpath("//span[@class='rcnt']//text()")
            result_count = ''.join(raw_result_count).strip()
            #print("Found {0} results for {1}".format(result_count, brand))
            scraped_products = []

            for product in product_listings:
                raw_url = product.xpath('.//a[@class="vip"]/@href')
                raw_title = product.xpath('.//a[@class="vip"]/text()')
                raw_price = product.xpath(".//li[contains(@class,'lvprice')]//span[@class='bold']//text()")
                price = ' '.join(' '.join(raw_price).split())
                title = ' '.join(' '.join(raw_title).split())
                data = {
                    'url': raw_url[0],
                    'title': title,
                    'price': price
                }
                scraped_products.append(data)
            scraped_data = pd.DataFrame(scraped_products)
            scraped_data.to_csv('%s-ebay-scraped-data.csv' %(brand),sep=",")
            #print(scraped_data)
        except Exception as e:
            print(e)
    time.sleep(5)
    position = position + 1
