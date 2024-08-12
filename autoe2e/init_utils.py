import json
from selenium.webdriver.remote.webdriver import WebDriver

from oraclai.utils import logger

from oraclai.core.config import Config
from oraclai.core.browser import get_driver_container
from oraclai.core.crawl_context import CrawlContext
from oraclai.core.state import State
from oraclai.core.action import Action, CandidateActionExtractor


def read_config(config_path: str) -> dict:
    logger.info(f'Reading config from {config_path}')
    
    with open(config_path, 'r', encoding='utf-8') as file:
        return json.load(file)


def initialize_driver(config: Config) -> WebDriver:
    logger.info('Initializing driver')
    return get_driver_container(config).get_driver()


def initialize_variables(crawl_context: CrawlContext) -> CrawlContext:
    logger.info('Initializing classes with initial state')
    
    crawl_context.driver.get(crawl_context.config.base_url)

    crawl_context.crawl_queue.reset()
    crawl_context.state_machine.reset()

    actions: list[Action] = CandidateActionExtractor.extract_candidate_actions(crawl_context.driver)
    
    initial_state: State = crawl_context.create_state_from_driver(actions)
    
    crawl_context.crawl_queue.enqueue(initial_state)
    
    return crawl_context
