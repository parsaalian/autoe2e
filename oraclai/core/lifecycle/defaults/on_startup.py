import json

from selenium.webdriver.remote.webdriver import WebDriver

from oraclai.utils import logger
from oraclai.core.lifecycle.abstracts import OnStartup
from oraclai.core.lifecycle.stage_repository import LifeCycleStage, StageRepository
from oraclai.core.config import Config
from oraclai.core.browser import get_driver_container
from oraclai.core.crawl_context import CrawlContext
from oraclai.core.state import State


class DefaultOnStartup(OnStartup):
    def read_config(self, config_path: str | None) -> dict:
        if config_path is None:
            logger.warn('No config path provided')
            return {}
        
        logger.info(f'Reading config from {config_path}')
        
        with open(config_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    
    
    def initialize_driver(self, config: Config) -> WebDriver:
        logger.info('Initializing driver')
        return get_driver_container(config).get_driver()
    
    
    def initialize_variables(self, crawl_context: CrawlContext, stages: dict[LifeCycleStage, StageRepository]) -> CrawlContext:
        logger.info('Initializing classes with initial state')
        
        crawl_context.driver.get(crawl_context.config.base_url)
        # TODO: dynamic state discovery is not executed here. Fix.
        stages[LifeCycleStage.ON_STATE_DISCOVERY].execute_stage(crawl_context, None)
        
        # TODO: Change the structure of temp vars since it seems to be a bit unclean
        initial_state: State = crawl_context.create_state_from_driver(crawl_context.get_temp_var('current_driver_actions'))
        
        crawl_context.crawl_queue.enqueue(initial_state)
        
        return crawl_context
    
    
    def on_startup(self, crawl_context: CrawlContext, stages: dict[LifeCycleStage, StageRepository]) -> CrawlContext:
        config: dict = self.read_config(config_path=crawl_context.temp_vars.get('config_path', None))
        config_obj: Config = Config.from_dict(config)
        
        if config_obj.base_url is None:
            raise ValueError('base_url is required in config')
        
        driver = self.initialize_driver(config_obj)
        
        new_context = crawl_context.set_config(config_obj)
        new_context = new_context.set_driver(driver)
        
        new_context = self.initialize_variables(new_context, stages)
        
        return new_context