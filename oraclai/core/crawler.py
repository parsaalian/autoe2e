from oraclai.utils import logger
from oraclai.core.lifecycle import LifeCycle
from oraclai.core.crawl_context import CrawlContext
from oraclai.core.state import State


class Crawler:
    def run(self, lifecycle: LifeCycle, crawl_context: CrawlContext):
        while len(crawl_context.crawl_queue) > 0:
            state: State = crawl_context.crawl_queue.dequeue()
            logger.info(f"Visiting state {state.get_id()}")
            
            crawl_context.state_machine.set_current_state(state)
            # if not lifecycle.should_visit(crawl_context):
            #     continue
            lifecycle.on_visit(crawl_context, None)
            # lifecycle.adjust_priority(crawl_context)
