from abc import ABC, abstractmethod

from oraclai.core.crawl_context import CrawlContext


class PostActionExecution(ABC):
    @abstractmethod
    def post_action_execution(self, crawl_context: CrawlContext) -> CrawlContext:
        pass
    
    
    def __call__(self, crawl_context: CrawlContext) -> CrawlContext:
        return self.post_action_execution(crawl_context)
