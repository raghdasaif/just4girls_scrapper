import re
import scrapy

from datetime import datetime

from just4girls_scraper.models.category import CategoryItem

class UnifiedSpiderSpider(scrapy.Spider):
    name = "unified_spider"
    allowed_domains = ["just4girls.pk"]
    start_urls = ["https://just4girls.pk"]

    def parse(self, response):
        category_links = response.xpath("//a[contains(@class, 'woodmart-nav-link')]/@href").getall()
        #self.logger.info(f"Found categories: {category_links}")

        for link in category_links:
            if not link or not link.strip() in ['#', 'javascript:void(0)']:
                link = link.strip()
                if link.startswith("/"):
                    full_link = response.urljoin(link)
                else:
                    full_link = link
                yield scrapy.Request(url=full_link, callback=self.parse_category)
            else:
                self.logger.warning("Empty or invalid link encountered, skipping.")

    def parse_category(self, response):
        item = CategoryItem()

        item['title'] = response.xpath("//h1[@class='entry-title title']/text()").get()
        item['description'] = response.xpath("//div[@class='term-description']/p/text()").get()
        item['breadcrumb_array'] = response.xpath("//div[@class='yoast-breadcrumb']//span//text()").getall()
        item['product_links'] = response.xpath("//a[contains(@class, 'product-image-link')]/@href").getall()
        item['url'] = response.url
        item['scraped_at'] = datetime.utcnow().isoformat()

        yield item

        for product_url in item['product_links']:
            yield response.follow(product_url, callback=self.parse_product)  
        
    def parse_product(self, response):
        breadcrumb_array = response.xpath("//div[@class='yoast-breadcrumb']//span//text()").getall()
        title = response.xpath("//h1[@class='product_title entry-title wd-entities-title']/text()").get()
        sku = response.xpath("//span[@class='sku_wrapper']/span[@class='sku']/text()").get().strip()
        if not sku:
            sku = response.url.rstrip('/').split('/')[-1] #if no sku found then treat slug as sku
        description = response.xpath('//div[@class="woocommerce-product-details__short-description"]/p/text()').get()
        old_price = response.xpath('//p[@class="price"]/del/span/bdi//text()').getall()
        current_price = response.xpath('//p[@class="price"]/ins/span/bdi//text()').getall()
        



