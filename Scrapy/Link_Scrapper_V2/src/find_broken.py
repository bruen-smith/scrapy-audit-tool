import multiprocessing

import requests
import scrapy
from scrapy.crawler import CrawlerProcess


class LinkSpider(scrapy.Spider):
    name = "link_spider"
    start_urls = ["http://example.com"]  # Replace with the target URL
    all_links = []  # This will store all the links

    def parse(self, response):
        # Extract links from the page
        links = response.css("a::attr(href)").getall()
        self.all_links.extend(links)  # Add found links to the list

        for link in links:
            yield response.follow(link, self.parse)  # Recursively follow links


def run_scrapy_spider():
    process = CrawlerProcess()
    process.crawl(LinkSpider)
    process.start()


def check_link_status_mp(url):
    try:
        response = requests.get(url, timeout=10)
        return (url, response.status_code)
    except requests.exceptions.RequestException as e:
        return (url, str(e))


def check_links_in_parallel(links):
    with multiprocessing.Pool(processes=4) as pool:
        results = pool.map(check_link_status_mp, links)
    return results


# Start Scrapy spider
run_scrapy_spider()

# After Scrapy finishes, check the status of all the links
results = check_links_in_parallel(LinkSpider.all_links)

# Print results
for result in results:
    print(f"URL: {result[0]}, Status Code: {result[1]}")
