import scrapy

class QuotesSpider(scrapy.Spider):

    # these 2 variables will name same everytime in every spider class
    name = "quotes"
    start_urls = [
        'https://www.gsmarena.com/samsung_galaxy_a32-6.php'
    ]

    def parse(self, response):
        
        # a_link = response.css('div#specs-list table').extract()


        device_name = response.css("h1.specs-phone-name-title::text").extract() 
        imgage_url = response.css("div.specs-photo-main a img").xpath("@src").extract()

        specs_list = response.css("div#specs-list table")

        device_specification = {}
        for table in specs_list:
            rows_in_table = table.css("tr")
            sub_specs = {}
            val_name = ''
            for rows in rows_in_table:
                td_in_rows = rows.css("td")
                
                for td in td_in_rows:
                    if td.css("td.ttl a::text").extract() != [] and val_name=="":
                        val_name = str(td.css("td.ttl a::text")[0].extract())
                        sub_specs[val_name] = []
                    elif td.css("td.nfo a::text").extract() != [] and val_name != "":
                        sub_specs[val_name] += td.css("td.nfo a::text").extract()
                    elif td.css("td.nfo::text").extract() != [] and val_name != "":
                        sub_specs[val_name] += td.css("td.nfo::text").extract()
                        
            
            device_specification[str(table.css("th::text")[0].extract())] = sub_specs

                


        

        
        yield { f'device_{device_name}':{
        "device_name" : device_name,
        "imgage_url": imgage_url,
        "device_specification" : device_specification,
        }
        }


        for x in range(7,25):
            next_page_url = f"https://www.gsmarena.com/s-{x}.php"
            yield response.follow(next_page_url, callback=self.parse)
