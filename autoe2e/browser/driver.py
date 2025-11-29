import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webdriver import WebDriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

from autoe2e.utils import AbstractSingleton
from autoe2e.crawler.config import Config


# TODO: if the connection is closed create a new driver
class DriverContainer(AbstractSingleton):
    def __init__(self, config: Config):
        # Configure Chrome options for Docker/headless mode
        chrome_options = Options()
        
        # Enable headless mode if running in Docker or CHROME_HEADLESS is set
        if os.getenv('CHROME_HEADLESS', 'false').lower() == 'true' or os.path.exists('/.dockerenv'):
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--window-size=1920,1080')
        
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options
        )
        # driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))
        # wait for elements to load on page if necessary
        # driver.implicitly_wait(10)
        self.driver = driver
    
    
    def get_driver(self) -> WebDriver:
        return self.driver


def get_driver_container(config: Config) -> DriverContainer:
    driver_container = DriverContainer(config)
    return driver_container
