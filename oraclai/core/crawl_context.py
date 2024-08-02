from typing import Any, Self

from selenium.webdriver.remote.webdriver import WebDriver

from oraclai.core.config import Config
from oraclai.core.state import State, StateMachine
from oraclai.core.action import Action
from oraclai.utils import Queue


class CrawlContext:
    def __init__(self):
        # change to config later
        self.config: Config | None = None
        self.driver: WebDriver | None = None
        self.crawl_queue: Queue[State] = Queue()
        self.state_machine: StateMachine = StateMachine()
        self.temp_vars: dict = {}
    
    
    def set_config(self, config: Config) -> Self:
        if self.config is not None:
            raise ValueError('config is already set')
        self.config = config
        return self
    
    
    def set_driver(self, driver: WebDriver) -> Self:
        if self.driver is not None:
            raise ValueError('driver is already set')
        self.driver = driver
        return self

    
    def load_state(self, state: State) -> None:
        self.driver.get(self.config.base_url)
        for action in state.crawl_path.get_actions():
            action.execute(self.driver)
    
    
    def create_state_from_driver(self, actions: list[Action]) -> State:
        state: State = State(
            url=self.driver.current_url,
            dom=self.driver.page_source,
            actions=actions
        )
        for action in state.get_actions():
            action.set_parent_state_id(state.get_id())
        return state
    
    
    def set_temp_var(self, key: str, value: Any) -> Self:
        self.temp_vars[key] = value
        return self
    
    
    def get_temp_var(self, key: str) -> Any:
        return self.temp_vars.get(key, None)
    
    
    def reset_temp_var(self, key: str) -> Self:
        self.temp_vars.pop(key, None)
        return self
    
    
    def clear_temp_vars(self) -> Self:
        self.temp_vars = {}
        return self
