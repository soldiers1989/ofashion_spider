import sys
sys.path.append('../')
import of_spider
import of_utils

class SandroParis(of_spider.Spider):
    def parse_entry(self, driver):
        products = []
        elements = of_utils.find_elements_by_css_selector(driver, 'div.product-image > div.table-cell > a')
        for element in elements:
            products.append(element.get_attribute('href').strip())
        pages = of_utils.find_elements_by_css_selector(driver, 'div.pagination > ul.clearfix > li > a')
        for page in pages:
            page.click()
            elements = of_utils.find_elements_by_css_selector(driver, 'div.product-image > div.table-cell > a')
            for element in elements:
                products.append(element.get_attribute('href').strip())
        return products

    def parse_product(self, driver):
        product = of_spider.empty_product.copy()
        # title
        element = of_utils.find_element_by_css_selector(driver, 'h1#title')
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found')
        # code N/A
        # price_cny
        element = of_utils.find_element_by_css_selector(driver, 'div.product-price > span')
        if element:
            price_text = element.text.strip()[1:].strip().replace(',', '') # 去掉开头的¥
            product['price_cny'] = int(float(price_text))
        # images
        elements = of_utils.find_elements_by_css_selector(driver, 'ul.productSlide > li > a > div.zoomPad > img')
        images = [element.get_attribute('src').strip() for element in elements]
        product['images'] = ';'.join(images)
        # detail
        element = of_utils.find_element_by_css_selector(driver, 'h2.detaildesc')
        product['detail'] = element.text.strip()
        return product