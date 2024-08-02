import time
import importlib

from oraclai.utils import logger
from oraclai.core.lifecycle import LifeCycle, LifeCycleStage
from oraclai.core.crawl_context import CrawlContext
from oraclai.core.crawler import Crawler


class CrawlController:
    def __init__(self):
        self.lifecycle: LifeCycle = LifeCycle()
        # should contain: queue, state graph, current state id, driver
        self.crawl_context: CrawlContext = CrawlContext()
    
    
    def add_stage_plugins(self, stage: LifeCycleStage) -> None:
        logger.info(f"Adding {stage} plugins to the runtime plugins")
        
        modules = list(map(
            lambda x: getattr(importlib.import_module(x[0]), x[1]),
            getattr(self.crawl_context.config, stage.value)
        ))
        for module in modules:
            self.lifecycle.add_plugin(module(), stage)
    
    
    def initialize_runtime_plugins(self):
        self.add_stage_plugins(LifeCycleStage.ON_STATE_DISCOVERY)
        self.add_stage_plugins(LifeCycleStage.ON_VISIT)
    
    
    def run(self, config_path: str) -> None:
        logger.info("Starting crawl controller")
        
        logger.info(f"Loading config from {config_path}")
        self.crawl_context = self.crawl_context.set_temp_var('config_path', config_path)
        self.crawl_context = self.lifecycle.on_startup(self.crawl_context).clear_temp_vars()

        logger.info("Initializing runtime plugins")
        self.initialize_runtime_plugins()
        
        logger.info("Starting the crawler")
        crawler = Crawler()
        
        logger.info("Running the crawler")
        crawler.run(self.lifecycle, self.crawl_context)
        logger.info("Crawler finished")
        
        time.sleep(1)
