from abc import ABC, abstractmethod

from oraclai.core.crawl_context import CrawlContext


class OnStateDiscovery(ABC):
    @abstractmethod
    def on_state_discovery(self, crawl_context: CrawlContext) -> CrawlContext:
        pass
    
    
    def __call__(self, crawl_context: CrawlContext, _) -> CrawlContext:
        return self.on_state_discovery(crawl_context)
