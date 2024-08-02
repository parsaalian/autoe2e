from oraclai.utils import logger

from oraclai.core.lifecycle.abstracts import OnVisit
from oraclai.core.lifecycle.stage_repository import LifeCycleStage, StageRepository
from oraclai.core.crawl_context import CrawlContext
from oraclai.core.state import State
from oraclai.core.action import Action


class DefaultOnVisit(OnVisit):
    def on_visit(self, crawl_context: CrawlContext, stages: dict[LifeCycleStage, StageRepository]) -> CrawlContext:
        current_state: State = crawl_context.state_machine.get_current_state()
        current_actions: list[Action] = current_state.get_actions()
        
        crawl_context.load_state(current_state)
        
        for action in current_actions:
            try:
                logger.info(f'Executing action {action.get_id()}')
                
                action.execute(crawl_context.driver)
                crawl_context.state_machine.set_last_executed_action(action)
                # Error: This executes both state discoveries. We first need to extract actions and then work with Claude
                # Maybe I need to add more refined lifecycle stages.
                stages[LifeCycleStage.ON_STATE_DISCOVERY].execute_stage(crawl_context, None)
                new_state: State = crawl_context.create_state_from_driver(crawl_context.get_temp_var('current_driver_actions'))
                
                # crawl_context.state_machine.set_visible_state(new_state)
                
                # TODO: possibly move this to a separate lifecycle stage.
                if new_state.get_id() not in crawl_context.state_machine.state_graph.states:
                    crawl_context.crawl_queue.enqueue(new_state)
                    crawl_context.state_machine.add_state_from_current_state(new_state, action)
                crawl_context.load_state(crawl_context.state_machine.get_current_state())
            except Exception as e:
                logger.error(f"An error occurred while executing action {action.get_id()}: {e}")
        
        return crawl_context
