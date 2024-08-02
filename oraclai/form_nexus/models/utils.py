from selenium.webdriver.common.by import By

from oraclai.form_nexus.utils import get_xpath, interact_with_input


def rule_based_value_generator(driver, inputs, rules):
    values = {}
    
    for element in inputs:
        tag = element.tag_name
        element_xpath = get_xpath(driver, element)
        input_type = element.get_attribute('type') or 'text'
        
        if tag == 'select':
            values[element_xpath] = rules['select'](element)
        
        elif input_type == 'checkbox' or input_type == 'radio':
            values[element_xpath] = rules['boolean']()
        
        else:
            values[element_xpath] = rules[input_type]()
    
    return values


def fill_form_with_values(driver, form_xpath, xpaths, values):
    for element_xpath in xpaths:
        element = driver.find_element(By.XPATH, element_xpath)
        element_value = values[element_xpath]

        if element.get_attribute('type') in ['checkbox', 'radio']:
            continue

        try:
            interact_with_input(element, element_value)
        except Exception as e:
            print(e)
    
    submit_button = driver.find_element(By.XPATH, f'{form_xpath}//*[@type = "submit"]')
    submit_button.click()