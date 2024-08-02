import uuid
from enum import Enum

from oraclai.utils import hash_string
from oraclai.core.state.crawl_path import CrawlPath
from oraclai.core.action import Action


class StateIdEvaluator(Enum):
    BY_UNIQUE = 'by_unique'
    BY_URL = 'by_url'
    BY_DOM = 'by_dom'
    BY_ACTIONS = 'by_actions'


class State:
    def __init__(
        self,
        url: str,
        dom: str,
        actions: list[Action],
        evaluator: StateIdEvaluator = StateIdEvaluator.BY_ACTIONS
    ):
        self.unique_id: str = str(uuid.uuid4())
        self.evaluator: StateIdEvaluator = evaluator
        self.url: str = url
        self.dom: str = dom
        self.context: str = ''
        self.actions: list[Action] = actions
        self.crawl_path: CrawlPath = CrawlPath()
    
    
    def get_crawl_path(self) -> CrawlPath:
        return self.crawl_path
    
    
    def set_context(self, context: str) -> None:
        self.context = context
    
    
    def get_context(self) -> str:
        return self.context
    
    
    def get_actions(self) -> list[Action]:
        return self.actions
    
    
    def set_evaluator(self, evaluator: StateIdEvaluator) -> None:
        self.evaluator = evaluator
    
    
    def set_crawl_path(self, crawl_path: CrawlPath) -> None:
        self.crawl_path = crawl_path
    
    
    def set_actions(self, actions: list[Action]) -> None:
        self.actions = actions
    
    
    def extend_actions(self, actions: list[Action]) -> None:
        self.actions.extend(actions)
    
    
    def get_id(self, specific_evaluator: StateIdEvaluator | None = None) -> str:
        evaluator = specific_evaluator if specific_evaluator else self.evaluator
        
        if evaluator == StateIdEvaluator.BY_URL:
            return self.url

        if evaluator == StateIdEvaluator.BY_DOM:
            return hash_string(self.dom)

        if evaluator == StateIdEvaluator.BY_ACTIONS:
            return hash_string(f'''{self.url}-{'-'.join(sorted([action.get_id() for action in self.actions]))}''')
        
        # Default, None, or BY_UNIQUE
        return self.unique_id
    
    
    def __eq__(self, other) -> bool:
        if self.dom == other.dom:
            return True
        
        if self.get_id(StateIdEvaluator.BY_ACTIONS) == other.get_id(StateIdEvaluator.BY_ACTIONS):
            return True
        
        return False


    def __ne__(self, other) -> bool:
        return not self.__eq__(other)
