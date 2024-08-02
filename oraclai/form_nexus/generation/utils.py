import time
from selenium.webdriver.common.by import By

from oraclai.form_nexus.utils import interact_with_input


class ValueTable:
    def __init__(self):
        self.entries = {}
    
    
    def add_entry(self, field_id, input_group, constraints):
        self.entries[field_id] = ValueTableEntry(input_group, constraints)
    
    
    def get_entry_by_field_id(self, field_id):
        return self.entries[field_id]
    
    
    def get_entry_by_input_group(self, input_group):
        filtered = list(filter(
            lambda x: x.input_group.node.xpath == input_group.node.xpath,
            self.entries.values()
        ))
        if len(filtered) > 0:
            return filtered[0]
        return None
    
    
    def print(self):
        for value_entry in self.entries.values():
            value_entry.print()
    
    
    def get_values_dict(self):
        values = {}
        for entry in self.entries.values():
            values[entry.input_group.node.xpath] = entry.value
        return values

    
    def copy(self):
        copy = ValueTable()
        for field_id, entry in self.entries.items():
            copy.add_entry(field_id, entry.input_group, entry.constraints)
            copy.get_entry_by_field_id(field_id).set_value(entry.value)
            copy.get_entry_by_field_id(field_id).set_feedback(entry.feedback)
        return copy


class ValueTableEntry:
    def __init__(self, input_group, constraints):
        self.input_group = input_group
        self.constraints = constraints
        self.feedback = None
        self.value = None
    
    
    def set_value(self, value):
        self.value = value
    
    
    def set_feedback(self, feedback):
        self.feedback = feedback
    
    
    def print(self):
        constraint_string = "\n".join(list(map(lambda x: x.to_prompt_string(), self.constraints)))
        
        output = f'''
        input field:
        {self.input_group.to_prompt_string()}
        constraints:
        {constraint_string}
        '''
        
        print(output)


def fill_form_with_value_table(driver, value_table, input_groups):
    for input_group in input_groups:
        entry = value_table.get_entry_by_input_group(input_group)
        
        if entry is None:
            continue
        
        print(entry.input_group.node)
        print(entry.value)
        
        try:
            element = driver.find_element(By.XPATH, entry.input_group.node.xpath)
            
            # skip form-changing elements for now. TODO: handle these cases
            if element.get_attribute('type') in ['submit', 'radio', 'checkbox']:
                continue
        
            interact_with_input(element, entry.value)
        except Exception as e:
            print('unable to fill input', entry.input_group.node.xpath, e)


def submit_form(driver, input_groups=None, explicit_submit=None):
    if explicit_submit is not None:
        submit = explicit_submit
    else:
        submit = list(filter(
            lambda x: 'type' in x.node.element.attrs and x.node.element.attrs['type'] == 'submit',
            input_groups
        ))[0]
    
    for i in range(5):
        try:
            if explicit_submit is not None:
                submit.click()
                print(i)
            else:
                interact_with_input(driver.find_element(By.XPATH, submit.node.xpath), True)
                time.sleep(0.5)
                print(i)
        except Exception as e:
            print(e)
            # break
            pass


def combine_contexts(app_context, form_context):
    return f'''
    {app_context}
    The following are all the labels in the form, which provide context for the functionality of the form: {form_context}
    '''.strip()