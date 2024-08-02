from abc import ABC, abstractmethod

from oraclai.core.crawl_context import CrawlContext
from oraclai.core.lifecycle.stage_repository import LifeCycleStage, StageRepository


class OnVisit(ABC):
    @abstractmethod
    def on_visit(self, crawl_context: CrawlContext, stages: dict[LifeCycleStage, StageRepository]) -> CrawlContext:
        pass
    
    
    def __call__(self, crawl_context: CrawlContext, stages: dict[LifeCycleStage, StageRepository]) -> CrawlContext:
        return self.on_visit(crawl_context, stages)
