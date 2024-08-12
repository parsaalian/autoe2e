from abc import ABC, abstractmethod

from selenium.webdriver.remote.webdriver import WebDriver

from autoe2e.utils import hash_string
from autoe2e.crawler.action.element import Element


class ActionType:
    def __init__(self, value: str):
        self._value = value
    
    
    def get_value(self):
        return self._value


class Action(ABC):
    def __init__(self, element: Element, action_type: ActionType):
        self.element: Element = element
        self.action_type = action_type
        self.should_execute = True
        self.parent_state_id = None
    
    
    def get_id_hashed(self):
        return hash_string(self.element.get_id())
    
    
    def get_id(self):
        return self.element.get_id()
    
    
    def get_type(self):
        return self.action_type
    
    
    def get_element(self) -> Element:
        return self.element
    
    
    def set_should_execute(self, should_execute: bool) -> None:
        self.should_execute = should_execute
    
    
    def get_should_execute(self) -> bool:
        return self.should_execute
    
    
    def set_parent_state_id(self, parent_state_id: str) -> None:
        self.parent_state_id = parent_state_id
    
    
    def get_parent_state_id(self) -> str | None:
        return self.parent_state_id
    
    
    @abstractmethod
    def execute(self, driver: WebDriver) -> None:
        pass
