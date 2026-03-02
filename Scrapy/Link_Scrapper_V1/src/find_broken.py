import os
import sys
from datetime import datetime
from urllib.parse import urlparse

import scrapy
from scraper_helper import headers, run_spider

# Default start page if no argument is provided
START_PAGE = sys.argv[1] if len(sys.argv) > 1 else "https://www.bethel.k12.or.us"


def is_valid_url(url):
    """Check if a given URL is valid."""
    try:
        result = urlparse(url.strip())
        return all([result.scheme, result.netloc])
    except:
        return False


def follow_this_domain(link):
    """Determine if the given link belongs to the same domain as START_PAGE."""
    return urlparse(link.strip()).netloc == urlparse(START_PAGE).netloc


class FindBrokenSpider(scrapy.Spider):
    """Scrapy spider to find broken links on a website."""

    # Parse the START_PAGE URL
    parsed_url = urlparse(START_PAGE)
    site_name = parsed_url.netloc.replace("www.", "").replace(".", "_")

    # Define output folder and ensure it exists
    output_folder = "broken_links_reports"
    os.makedirs(output_folder, exist_ok=True)

    # Generate a timestamped output filename
    time_stamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_filename = os.path.join(
        output_folder, f"{site_name}_broken_links_{time_stamp}.csv"
    )

    # Scrapy custom settings
    custom_settings = {
        "DEFAULT_REQUEST_HEADERS": headers(),
        "ROBOTSTXT_OBEY": False,
        "RETRY_TIMES": 3,
        "FEEDS": {
            output_filename: {
                "format": "csv",
                "encoding": "utf8",
                "fields": [
                    "Source_Page",
                    "Link_Text",
                    "Broken_Page_Link",
                    "HTTP_Code",
                    "External",
                ],
            }
        },
    }

    name = "find_broken"
    handle_httpstatus_list = [x for x in range(400, 600) if x not in (401, 403)]
    total_links_checked = 0

    def start_requests(self):
        """Initiate crawling from the START_PAGE."""
        yield scrapy.Request(
            START_PAGE,
            cb_kwargs={"source": "NA", "text": "NA"},
            errback=self.handle_error,
        )

    def parse(self, response, source, text):
        """Parse page contents and check links."""
        self.total_links_checked += 1

        # Log broken links
        if response.status in self.handle_httpstatus_list:
            yield self.create_item(source, text, response.url, response.status)
            return

        # Skip non-HTML content
        content_type = response.headers.get("content-type", b"").decode("utf-8").lower()
        if "text" not in content_type:
            self.logger.info(f"{response.url} is NOT HTML")
            return

        # Extract and process links from the page
        for a in response.xpath("//a"):
            text = a.xpath("./text()").get()
            link = response.urljoin(a.xpath("./@href").get())
            if not is_valid_url(link):
                continue

            self.total_links_checked += 1
            callback_func = (
                self.parse if follow_this_domain(link) else self.parse_external
            )
            yield scrapy.Request(
                link,
                cb_kwargs={"source": response.url, "text": text},
                callback=callback_func,
                errback=self.handle_error,
            )

    def handle_error(self, failure):
        """Handle request failures and log errors."""
        request = failure.request
        self.logger.error(f"Error on {request.url}: {repr(failure)}")
        yield self.create_item(
            "Unknown", None, request.url, "DNSLookupError or other unhandled"
        )

    def parse_external(self, response, source, text):
        """Check external links and log if broken."""
        self.total_links_checked += 1
        if response.status != 200:
            yield self.create_item(source, text, response.url, response.status)

    def create_item(self, source, text, link, status):
        """Create an item to store broken link data."""
        return {
            "Source_Page": source,
            "Link_Text": text,
            "Broken_Page_Link": link,
            "HTTP_Code": status,
            "External": not follow_this_domain(link),
        }

    def closed(self, reason):
        """Log summary when the spider closes."""
        output_file = list(self.custom_settings["FEEDS"].keys())[0]
        message = (
            f"Spider closed ({reason}). Total links checked: {self.total_links_checked}"
        )
        print(message)


if __name__ == "__main__":
    run_spider(FindBrokenSpider)
