import time

from worker.app_worker import app


from billiard import Process
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


class RunCrawlerScript:

    def __init__(self):
        self.crawler = CrawlerProcess(get_project_settings())

    def _crawl(self, **kwargs):
        self.crawler.crawl('ukg_spider', **kwargs)
        self.crawler.start()
        self.crawler.stop()

    def crawl(self, client_id: int):
        p = Process(target=self._crawl, kwargs={'client_id': client_id})
        p.start()
        p.join()


crawler = RunCrawlerScript()


@app.task(name="run_crawler")
def crawler_task(client_id: int):
    crawler.crawl(client_id)
    return True
