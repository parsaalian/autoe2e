import rstr
import random

from selenium.webdriver.support.ui import Select

from .utils import rule_based_value_generator


random_rules = {
    'text': lambda: rstr.xeger(r'.*'),
    'email': lambda: rstr.xeger(r'[A-Za-z0-9]{10}') + '@' + rstr.xeger(r'[A-Za-z0-9]{10}') + '.com',
    'password': lambda: rstr.xeger(r'.{10}'),
    'number': lambda: rstr.xeger(r'[0-9]*'),
    'range': lambda: rstr.xeger(r'[0-9]*'),
    'date': lambda: rstr.xeger(r'[0-9]{4}') + '-' + rstr.xeger(r'[0-9]{2}') + '-' + rstr.xeger(r'[0-9]{2}'),
    'time': lambda: rstr.xeger(r'[0-9]{2}') + ':' + rstr.xeger(r'[0-9]{2}'),
    'datetime-local': lambda: rstr.xeger(r'[0-9]{4}') + '-' + rstr.xeger(r'[0-9]{2}') + '-' + rstr.xeger(r'[0-9]{2}') + 'T' + rstr.xeger(r'[0-9]{2}') + ':' + rstr.xeger(r'[0-9]{2}'),
    'week': lambda: rstr.xeger(r'[0-9]{4}') + '-W' + rstr.xeger(r'[0-9]{2}'),
    'month': lambda: rstr.xeger(r'[0-9]{4}') + '-' + rstr.xeger(r'[0-9]{2}'),
    'tel': lambda: rstr.xeger(r'[0-9]{10}'),
    'url': lambda: 'https://' + rstr.xeger(r'[A-Za-z0-9]{10}') + '.com',
    'color': lambda: '#' + rstr.xeger(r'[0-9A-Fa-f]{6}'),
    
    'boolean': lambda: True if random.randint(0, 1) == 0 else False,
    'select': lambda element: random.randint(0, len(Select(element).options) - 1),
}

def generate_random_values(driver, inputs, value_count=10):
    values = {}
    success = rule_based_value_generator(driver, inputs, random_rules)
    fails = [
        rule_based_value_generator(driver, inputs, random_rules) for _ in range(value_count)
    ]
    for xpath, value in success.items():
        values[xpath] = {
            'passing': value,
            'failing': [fail[xpath] for fail in fails]
        }
    
    return values