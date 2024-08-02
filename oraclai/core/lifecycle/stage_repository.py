from enum import Enum
from typing import Generic, TypeVar, Self

from oraclai.core.crawl_context import CrawlContext


T = TypeVar('T')


class LifeCycleStage(Enum):
    '''
    Enum for the different stages of the lifecycle.
    '''
    ON_STARTUP = 'on_startup'
    ON_VISIT = 'on_visit'
    ON_STATE_DISCOVERY = 'on_state_discovery'


class StageRepository(Generic[T]):
    def __init__(self):
        self.plugin_list: list[T] = []
    
    
    def execute_stage(self, crawl_context: CrawlContext, stages: dict[LifeCycleStage, Self] | None) -> CrawlContext:
        for plugin in self.plugin_list:
            crawl_context = plugin(crawl_context, stages)
        return crawl_context
    
    
    def add_plugin(self, plugin: T):
        '''
        Adds a plugin to the lifecycle stage to be executed during runtime.
        '''
        self.plugin_list.append(plugin)
