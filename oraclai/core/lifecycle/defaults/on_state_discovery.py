from oraclai.utils import logger
from oraclai.core.lifecycle.abstracts.on_state_discovery import OnStateDiscovery
from oraclai.core.crawl_context import CrawlContext
from oraclai.core.action import Action, CandidateActionExtractor


class DefaultOnStateDiscovery(OnStateDiscovery):
    def on_state_discovery(self, crawl_context: CrawlContext) -> CrawlContext:
        logger.info('New state discovered. Extracting actions.')
        
        crawl_context.reset_temp_var('current_driver_actions')
        actions: list[Action] = CandidateActionExtractor.extract_candidate_actions(crawl_context.driver)
        crawl_context.set_temp_var('current_driver_actions', actions)
        return crawl_context
