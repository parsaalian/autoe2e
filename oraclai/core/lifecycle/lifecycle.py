from oraclai.core.lifecycle.abstracts import (
    OnStartup,
    OnVisit,
    OnStateDiscovery,
)
from oraclai.core.lifecycle.defaults import (
    DefaultOnStartup,
    DefaultOnVisit,
    DefaultOnStateDiscovery,
)
from oraclai.core.lifecycle.stage_repository import LifeCycleStage, StageRepository
from oraclai.core.crawl_context import CrawlContext


class LifeCycle(
    OnStartup,
    OnVisit,
):
    '''
    Executes different plugins at different stages of the lifecycle.
    '''
    def __init__(self):
        super().__init__()
        
        on_startup: StageRepository[OnStartup] = StageRepository()
        on_visit: StageRepository[OnVisit] = StageRepository()
        on_state_discovery: StageRepository[OnStateDiscovery] = StageRepository()
        
        self.stages: dict[LifeCycleStage, StageRepository] = {
            LifeCycleStage.ON_STARTUP: on_startup,
            LifeCycleStage.ON_VISIT: on_visit,
            LifeCycleStage.ON_STATE_DISCOVERY: on_state_discovery,
        }
    
        self.stages[LifeCycleStage.ON_STARTUP].add_plugin(DefaultOnStartup())
        self.stages[LifeCycleStage.ON_VISIT].add_plugin(DefaultOnVisit())
        self.stages[LifeCycleStage.ON_STATE_DISCOVERY].add_plugin(DefaultOnStateDiscovery())
    
    
    def on_startup(self, crawl_context: CrawlContext, _=None) -> CrawlContext:
        return self.stages[LifeCycleStage.ON_STARTUP].execute_stage(crawl_context, self.stages)


    def on_visit(self, crawl_context: CrawlContext, _=None) -> CrawlContext:
        return self.stages[LifeCycleStage.ON_VISIT].execute_stage(
            crawl_context,
            self.get_stage_subset([
                LifeCycleStage.ON_STATE_DISCOVERY
            ])
        )

    
    def get_stage_subset(self, stages: list[LifeCycleStage]) -> dict[LifeCycleStage, StageRepository]:
        '''
        Returns a subset of the stages dictionary based on the given list of stages.
        '''
        return {stage: self.stages[stage] for stage in stages}


    def add_plugin(self, plugin, stage: LifeCycleStage):
        '''
        Adds a plugin to the lifecycle stage to be executed during runtime.
        '''
        self.stages[stage].add_plugin(plugin)
    
    
    def __call__(self):
        raise NotImplementedError(
            'LifeCycle cannot be called directly. Use the on_startup, on_visit, on_action_extraction, and post_action_execution methods instead.'
        )
