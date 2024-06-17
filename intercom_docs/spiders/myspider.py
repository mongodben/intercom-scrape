import scrapy
import html2text
from bs4 import BeautifulSoup


class MySpider(scrapy.Spider):
    name = 'myspider'
    allowed_domains = ["intercom-help.mongodb.com"]
    start_urls = ["https://intercom-help.mongodb.com/en/"]

    def parse(self, response):
        # Extract and follow all links on the page
        for link in response.css('a::attr(href)').getall():
            url = response.urljoin(link)
            yield scrapy.Request(url, callback=self.parse)
        # Extract the main content of the page
        main_content = response.css('body').get()

        # Convert the HTML to Markdown
        if main_content:
            soup = BeautifulSoup(main_content, 'html.parser')
            converter = html2text.HTML2Text()
            converter.ignore_links = False
            markdown_content = converter.handle(str(soup))

            # Create a full Markdown document
            title = response.css('title::text').get()
            html_doc = str(main_content)

            yield {
                'url': response.url,
                'markdown': f"# {title}\n\n{markdown_content}",
                'html': html_doc,
            }
