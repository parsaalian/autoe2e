from selenium.webdriver.common.by import By

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement


def get_element_xpath(driver: WebDriver, element: WebElement) -> str:
    xpath_script = """
        function getPathTo(element) {
            // if (element.id !== '')
            //     return 'id(\"'+element.id+'\")';
            if (element === document.body)
                return element.tagName;
            var ix= 0;
            var siblings= element.parentNode.childNodes;
            for (var i= 0; i<siblings.length; i++) {
                var sibling= siblings[i];
                if (sibling===element)
                    return getPathTo(element.parentNode) + '/' + element.tagName + '[' + (ix + 1) + ']';
                if (sibling.nodeType===1 && sibling.tagName===element.tagName)
                    ix++;
            }
        }
        const path = getPathTo(arguments[0]);
        if (path.startsWith('id(')) {
            return path;
        }
        return '//' + path;
    """
    
    xpath = driver.execute_script(xpath_script, element)
    return xpath


def save_screenshot(driver: WebDriver, path: str = '/tmp/screenshot.png') -> None:
    # Ref: https://stackoverflow.com/a/52572919/
    original_size = driver.get_window_size()
    required_width = driver.execute_script('return document.body.parentNode.scrollWidth')
    required_height = driver.execute_script('return document.body.parentNode.scrollHeight')
    driver.set_window_size(required_width, required_height)
    # driver.save_screenshot(path)  # has scrollbar
    driver.find_element(By.TAG_NAME, 'body').screenshot(path)  # avoids scrollbar
    driver.set_window_size(original_size['width'], original_size['height'])