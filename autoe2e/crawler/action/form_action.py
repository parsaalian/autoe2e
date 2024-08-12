from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from autoe2e.crawler.action.action import Action, ActionType
from autoe2e.crawler.action.element import Element
from autoe2e.browser.utils import get_element_xpath

from autoe2e.manual_ndd import FORBIDDEN_ACTIONS


class FormActionType(ActionType):
    def __init__(self):
        super().__init__('form')


class FormAction(Action):
    def __init__(self, element: Element):
        super().__init__(element, action_type=FormActionType())
        self.params = None
    
    
    def set_params(self, params: dict[str, str | int | float | bool]) -> None:
        self.params = params
    
    
    def has_params(self) -> bool:
        return self.params is not None
    
    
    def execute(self, driver: WebDriver) -> None:
        if self.params is None:
            raise ValueError('Parameters are not set for the form action.')
        
        driver.execute_script("arguments[0].scrollIntoView(true);", self.element.get(driver))
        
        element: WebElement = self.element.get(driver)
        
        try:
            form_id = element.get_attribute('data-formid')
            
            for param_key, param_value in self.params.items():
                element.find_element(By.XPATH, f".//*[@data-testid='{param_key}']").send_keys(param_value)
            
            submit_button = driver.find_element(By.XPATH, f".//*[@data-submitid='{form_id}']")
            
            pair = (driver.current_url, get_element_xpath(driver, submit_button))
            
            if pair not in FORBIDDEN_ACTIONS:
                submit_button.click()
        except Exception as e:
            print(e)
            print("waiting for use to perform the form task")
            input("Press Enter to continue...")
