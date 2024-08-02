from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.remote.webdriver import WebDriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

from oraclai.utils import AbstractSingleton
from oraclai.core.config import Config


# TODO: if the connection is closed create a new driver
class DriverContainer(AbstractSingleton):
    def __init__(self, config: Config):
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        # driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))
        # wait for elements to load on page if necessary
        # driver.implicitly_wait(10)
        self.driver = driver
    
    
    def get_driver(self) -> WebDriver:
        return self.driver


def get_driver_container(config: Config) -> DriverContainer:
    driver_container = DriverContainer(config)
    return driver_container
