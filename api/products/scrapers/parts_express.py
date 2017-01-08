import re

from products.scrapers.scraper import DealerScraper, Scraper


class CategoryListScraper(Scraper):

    PATH = "/cat/hi-fi-woofers-subwoofers-midranges-tweeters/13"
    TARGETS = {
        "DRIVER_CATEGORY": '//a[@id="lbCategoryName"]/@href'
    }

    def run(self):
        try:
            categories = self.get_html(
                self.build_url(self.PATH)).xpath(self.TARGETS["DRIVER_CATEGORY"])

            for c in categories:
                if re.search(r'replace|recone', c):
                    self.add_skip(c)
                else:
                    self.add_pass(c)

            return self.result
        except Exception as e:
            print("{0}".format(e))
            self.add_error(repr(e))


# @todo return DealerScraperResult
class PartsExpressScraper(DealerScraper):

    LABEL = "Parts Express"

    def run(self):
        base_url = self.get_url()
        print("{0}".format(base_url))
        result = CategoryListScraper(base_url=base_url).run()
        print("{0}".format(result))


# if __name__ == "__main__":
#     PartsExpressScraper().run()
