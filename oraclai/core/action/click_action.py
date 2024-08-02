from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.action_chains import ActionChains

from oraclai.core.action.action import Action, ActionType
from oraclai.core.action.element import Element
from selenium.common.exceptions import TimeoutException
import sys


class ClickActionType(ActionType):
    def __init__(self):
        super().__init__('click')


class ClickAction(Action):
    def __init__(self, element: Element):
        super().__init__(element, action_type=ClickActionType())
    
    
    def execute(self, driver: WebDriver) -> None:
        try:
            element = self.element.get(driver)
            driver.execute_script("arguments[0].scrollIntoView(true);", element)
            ActionChains(driver).move_to_element(element).click(element).perform()
            
        except TimeoutException as toe:
            print(driver.current_url)
            print(toe)
            print("-----")
            print(str(toe))
            print("-----")
            print(toe.args)
            print("ELEMENT ID:", self.element.get_id())
            driver.quit()
            sys.exit(1)
