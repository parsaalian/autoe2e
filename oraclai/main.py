from oraclai.core import CrawlController


def run(config: str):
    crawler: CrawlController = CrawlController()
    crawler.run(config)
