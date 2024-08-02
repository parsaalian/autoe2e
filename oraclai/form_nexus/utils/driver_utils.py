import os
from dotenv import load_dotenv

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from webdriver_manager.chrome import ChromeDriverManager

load_dotenv()


def create_driver(headless=False):
    chrome_options = Options()
    
    if headless:
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=3072x1920");
    
    chrome_options.add_experimental_option('prefs', {
        'profile.default_content_setting_values.geolocation': 2,
    })
    # chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36")
    # chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    # chrome_options.add_experimental_option('useAutomationExtension', False)

    # driver = webdriver.Chrome(executable_path=os.getenv("CHROME_DRIVER_EXECUTABLE"), options=chrome_options)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.set_page_load_timeout(15)
    
    if not headless:
        driver.maximize_window()
    
    return driver


def get_application_context(driver):
    title = driver.title
    description_tag = driver.find_element_by_xpath(
        "//meta[@name='description' or @name='og:description' or @property='og:description']"
    )
    description = description_tag.get_attribute('content')
    
    return f'''Title: {title}\nDescription: {description}'''


def get_xpath(driver, element):
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
    return driver.execute_script(xpath_script, element)


def get_visual_spans(element):
    # Get the location and size of the root element
    location = element.location
    size = element.size

    # Calculate the boundaries of the root element
    x_span = (location['x'], location['x'] + size['width'])
    y_span = (location['y'], location['y'] + size['height'])
    
    return x_span, y_span


def set_attribute(driver, element, key, value):
    driver.execute_script("arguments[0].setAttribute(arguments[1], arguments[2])", element, key, value)


def embed_properties_into_html(driver, root):
    '''
    This function embeds the x_span, y_span, and xpath
    properties into WebElement as attributes for processing
    in the next steps. We do this because we want to convert
    the WebElement into a BeautifulSoup document.
    '''
    x_span, y_span = get_visual_spans(root)
    xpath = get_xpath(driver, root)
    
    set_attribute(driver, root, 'xpath', xpath)
    set_attribute(driver, root, 'x_start', x_span[0])
    set_attribute(driver, root, 'x_end', x_span[1])
    set_attribute(driver, root, 'y_start', y_span[0])
    set_attribute(driver, root, 'y_end', y_span[1])
    
    for child in root.find_elements(By.XPATH, '*'):
        embed_properties_into_html(driver, child)
    
    return root


def wait_for_elements(driver, xpath, timeout=5):
    elements = WebDriverWait(driver, timeout).until(
        EC.presence_of_all_elements_located((By.XPATH, xpath))
    )
    return elements


def interact_with_input(element, value):
    try:
        element.clear()
    except:
        pass
    
    if value is None:
        return
    
    if element.tag_name == 'select':
        select = Select(element)
        try:
            select.select_by_value(value)
        except:
            select.select_by_visible_text(value)
    elif element.get_attribute('type') in ['checkbox', 'radio', 'submit', 'button'] and value:
        element.click()
    else:
        element.send_keys(value)
