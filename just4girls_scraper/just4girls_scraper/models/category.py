from scrapy import Item, Field

class CategoryItem(Item):
    title = Field()
    description = Field()
    breadcrumb_path = Field()
    breadcrumb_array = Field()
    product_links = Field()
    url = Field()
    scraped_at = Field()
    category_id = Field()
    parent_category = Field()
    product_count = Field()
