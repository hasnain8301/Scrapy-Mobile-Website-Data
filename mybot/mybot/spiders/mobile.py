import scrapy
import requests



class QuotesSpider(scrapy.Spider):

    # these 2 variables will name same everytime in every spider class
    name = "mobile"
    start_urls = [
        'http://www.mobile-phone.pk/samsung_galaxy_a32_5g-1/'
    ]

    def parse(self, response):
        
        # a_link = response.css('div#specs-list table').extract()

        device_name = response.css("h1#head1::text")[0].extract()
        pak_price = response.css("div.h2_class p.bold::text")[0].extract().strip()

        img_url = response.css("div.mobile_rate img").xpath("@src")[0].extract()

        img_response = requests.get(img_url)
        img_name = device_name.replace(' ', '_')
        if img_response.status_code:
            fp = open(f'images/{img_name}.jpg', 'wb')
            fp.write(img_response.content)
            fp.close()

        specs_list = response.css("div#specs-list div.specs_table")
        
        specifications = {}
        
        for rows in specs_list:
            val_name = ""
            sub_specs = {}
            if rows.css("div.h2_class::text").extract() != [] and val_name=="":
                val_name = str(rows.css("div.h2_class::text")[0].extract())
                
            sub_row = rows.css("div.specs_table_row")
            for row in sub_row:
                    if row.css("div.specs_cell1::text").extract() != [] and row.css("div.specs_cell2::text").extract() != []:
                        sub_specs[str(row.css("div.specs_cell1::text")[0].extract())] = str(row.css("div.specs_cell2::text")[0].extract())
                        specifications[val_name] = sub_specs
        


        yield { 'device': {
            "device_name": device_name,
            "pak_price": pak_price,
            "img_url": img_url,
            "img_name": img_name,
            "specifications": specifications
        }} 
        


        for x in range(2,1000):
            # time.sleep(0.5)
            next_page_url = f"http://www.mobile-phone.pk/samsung_galaxy_a32_5g-{x}/"
            yield response.follow(next_page_url, callback=self.parse)
