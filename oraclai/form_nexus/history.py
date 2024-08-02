import json
import pandas as pd


test_file_template = '''
import time
import unittest

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from webdriver_manager.chrome import ChromeDriverManager


class FormTests(unittest.TestCase):
\tdef setUp(self):
\t\tself.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
\t\tself.driver.get("{url}")
    
    
\tdef tearDown(self):
\t\tself.driver.close()


\tdef _wait_for_element(self, xpath):
\t\telement = WebDriverWait(self.driver, 5).until(
\t\t\tEC.presence_of_element_located((By.XPATH, xpath))
\t\t)
\t\treturn element


{test_cases}


if __name__ == "__main__":
\tunittest.main()
'''


test_case_template = '''
\tdef test_{name}(self):
\t\t\'\'\'{description}\'\'\'
\t\tdriver = self.driver
{code}
'''


send_key_template = '''
\t\telement = self._wait_for_element("{xpath}")
\t\telement.send_keys("{value}")
'''


submit_template = '''
\t\tbutton = self._wait_for_element("{form_xpath}//*[@type='submit']")
\t\tdriver.execute_script('arguments[0].click()', button)
'''


assertion_template = '''
\t\ttime.sleep(1)
\t\tbody_text = driver.find_element(By.TAG_NAME, 'body').text
\t\tassert "{feedback}" in body_text
'''


class HistoryTable:
    def __init__(self, url, xpath):
        self.url = url
        self.xpath = xpath
        self.table = pd.DataFrame(columns=[
            'values',
            'variation_type',
            'feedback',
            'new_url'
        ])
    
    
    def add(self, values, variation_type, feedback, new_url):
        self.table = self.table.append({
            'values': json.dumps(values),
            'variation_type': variation_type,
            'feedback': 'FEEDBACK-DELIMITER'.join(feedback),
            'new_url': new_url
        }, ignore_index=True)
    
    
    def to_csv(self, output_file):
        self.table.to_csv(output_file, index=False)
    
    
    def to_test_case(self, output_file):
        test_cases = []
        
        for idx, row in self.table.iterrows():
            values = json.loads(row['values'].replace('\'', '"').lower())
            
            fields = []
            for xpath, value in values.items():
                send_key = send_key_template.format(
                    xpath=xpath,
                    value=value
                )
                fields.append(send_key)
            
            submit = submit_template.format(
                form_xpath=self.xpath
            )
            fields.append(submit)
            
            # TODO: add assertions on url
            # TODO: create a more unique string to split feedback
            assertions = []
            for feedback in row['feedback'].split('FEEDBACK-DELIMITER'):
                assertion = assertion_template.format(feedback=feedback)
                assertions.append(assertion)
                
            
            test_case = test_case_template.format(
                name=idx,
                description=idx,
                code='\n'.join([*fields, *assertions])
            )
            
            test_cases.append(test_case)

        test_file = test_file_template.format(
            url=self.url,
            test_cases='\n'.join(test_cases)
        )
        
        with open(output_file, 'w+') as f:
            f.write(test_file.strip())