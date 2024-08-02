#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().run_line_magic('load_ext', 'autoreload')
get_ipython().run_line_magic('autoreload', '2')


import os
import time
import copy
import json
import openai
from dotenv import load_dotenv

from bs4 import BeautifulSoup as bs
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from method.models import generate_random_values, generate_static_values, generate_llm_values
from oraclai.form_nexus.utils import create_driver, get_xpath, interact_with_input
from oraclai.form_nexus.history import HistoryTable
from oraclai.form_nexus.feedback import get_global_feedback


# In[2]:


load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Global Variables
HEADLESS = False
TEXT_EMBEDDING_METHOD = 'ADA'
GRAPH_EMBEDDING_METHOD = 'NODE2VEC'

URL = 'https://www.stubhub.ca/'
# 'https://www.macys.com/'
# 'https://www.amazon.com/'
# 'https://www.carmax.com/'
# 'https://www.rei.com/'
# 'https://www.uhaul.com/'
# 'https://www.ups.com/us/en/Home.page'
# 'https://www.thumbtack.com/'
# 'https://www.healthgrades.com/'
# 'https://www.webmd.com/drugs/2/index'
# 'https://www.babycenter.com/child-height-predictor'
# 'https://www.babycenter.com/pregnancy-weight-gain-estimator'
# 'https://seatgeek.ca/'
# 'https://www.stubhub.ca/'
# 'https://app.invoicing.co/#/register'
# 'http://localhost:3000/default-channel/en-US/account/register/'
# 'http://localhost:9000/dashboard/discounts/sales/add'
# 'http://localhost:9000/dashboard/customers/add'
# 'http://localhost:8080/'
# 'https://www.budget.com/en/home'
# 'https://www.thetrainline.com/en-us'
# 'https://www.mbta.com/'
# 'https://www.tripadvisor.com/'
# 'https://resy.com/'
# 'https://www.yelp.com/'
# 'https://www.aa.com/homePage.do'
# 'https://www.jetblue.com/'
# 'https://www.united.com/en/us'
# 'https://www.aircanada.com/ca/en/aco/home.html'


def get_to_form(driver):
    try:
        driver.get(URL)
        
        '''
        # UPS - Quote
        time.sleep(2)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'tabs_0_tab_1'))
        ).click()
        '''
        
        '''
        # Saleor
        try:
            time.sleep(2)
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((
                    By.XPATH,
                    '//BODY/DIV[1]/MAIN[1]/DIV[1]/DIV[1]/DIV[1]/FORM[1]/DIV[2]/DIV[1]/INPUT[1]')
                )
            ).send_keys('admin@example.com')
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((
                    By.XPATH,
                    '//BODY/DIV[1]/MAIN[1]/DIV[1]/DIV[1]/DIV[1]/FORM[1]/DIV[4]/DIV[1]/DIV[1]/INPUT[1]')
                )
            ).send_keys('admin')
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((
                    By.XPATH,
                    '//BODY/DIV[1]/MAIN[1]/DIV[1]/DIV[1]/DIV[1]/FORM[1]/DIV[5]/BUTTON[1]')
                )
            ).click()
        except:
            pass
        
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((
                By.XPATH,
                '//BODY/DIV[1]/MAIN[1]/DIV[1]/DIV[2]/MAIN[1]/FORM[1]/DIV[1]/DIV[2]/DIV[4]/DIV[2]/LABEL[1]/SPAN[1]/SPAN[1]/INPUT[1]')
            )
        ).click()
        '''
        
        '''
        # Pet Clinic - Add Owner
        time.sleep(2)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((
                By.XPATH,
                '//BODY/APP-ROOT[1]/DIV[1]/NAV[1]/DIV[1]/UL[1]/LI[2]')
            )
        ).click()
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((
                By.XPATH,
                '//BODY/APP-ROOT[1]/DIV[1]/NAV[1]/DIV[1]/UL[1]/LI[2]/UL[1]/LI[2]')
            )
        ).click()
        '''
        
        '''
        # Budget - Reservation
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, 'PicLoc_value'))
        ).click()
        '''
        
        '''
        # MBTA
        time.sleep(2)
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, '//BODY/DIV[1]/DIV[2]/MAIN[1]/DIV[1]/DIV[1]/DIV[1]/DIV[2]/A[1]'))
        ).click()
        '''
        
        '''
        # AC - My Bookings
        time.sleep(2)
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, 'bkmg-tab-button-mngBook'))
        ).click()
        '''
        
        '''
        # AC - Multi-city
        time.sleep(2)
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, 'bkmgFlights_tripTypeSelector_M'))
        ).click()
        '''
        
    except:
        print('timeout')


def find_form():
    return WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((
            By.XPATH,
            '//BODY/DIV[1]/DIV[1]/DIV[1]/DIV[2]/DIV[2]/DIV[1]/DIV[1]/DIV[1]/DIV[1]/DIV[1]/DIV[2]/DIV[1]/DIV[1]/DIV[2]/DIV[1]'
        ))
    )


def find_button():
    return None


# In[3]:


driver = create_driver(HEADLESS)
get_to_form(driver)


# In[4]:


html = driver.find_element(By.TAG_NAME, 'html').get_attribute('outerHTML')
form = find_form()
form_xpath = get_xpath(driver, form)

inputs = form.find_elements(
    By.XPATH,
    f'{form_xpath}//input | {form_xpath}//textarea | {form_xpath}//select'
)

inputs = list(filter(
    lambda x: x.get_attribute('type') != 'hidden' and x.get_attribute('hidden') != 'true',
    inputs
))


# In[5]:


history_table = HistoryTable(
    url=URL,
    xpath=form_xpath
)


# In[6]:


METHOD = 'llm'


# In[ ]:


values = None
if METHOD == 'static':
    values = generate_static_values(driver, inputs)
elif METHOD == 'random':
    values = generate_random_values(driver, inputs)
else:
    values = generate_llm_values(form.get_attribute('outerHTML'), openai.api_key)


# In[ ]:


values


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[13]:


def get_element(element_id):
    return driver.find_element(By.ID if METHOD == 'llm' else By.XPATH, element_id)


def send_values(elemend_ids, values):
    for element_id in elemend_ids:
        try:
            element = get_element(element_id)
        except:
            continue
        value = values[element_id]
        
        element_type = element.get_attribute('type') or 'text'
    
        if element_type in ['radio', 'checkbox'] or element.tag_name in ['button']:
            continue
        
        try:
            interact_with_input(element, value)
        except:
            pass

        
def submit_form(form):
    # submit = driver.find_element(By.XPATH, f'{form_xpath}//*[@type="submit"]')
    # driver.find_element(By.TAG_NAME, 'body').click()
    submit = find_button()
    
    for _ in range(3):
        try:
            interact_with_input(submit, True)
            time.sleep(0.5)
        except:
            break


# In[16]:


passing_set = {
    element_id: values[element_id]['passing'] for element_id in values.keys()
}


for element_id, element_values in values.items():
    get_to_form(driver)
    time.sleep(1)
    
    try:
        element = get_element(element_id)
    except:
        continue
    element_type = element.get_attribute('type') or 'text'
    
    if element_type in ['radio', 'checkbox', 'submit']:
        continue
    
    # print(element)
    
    for failing_value in element_values['failing']:
        # try:
        get_to_form(driver)
        time.sleep(1)
    
        passing_copy = copy.copy(passing_set)
        passing_copy[element_id] = failing_value
        send_values(values.keys(), passing_copy)

        time.sleep(1)

        submit_form(form)

        new_html = driver.find_element(By.TAG_NAME, 'body').get_attribute('outerHTML')
        global_feedback = get_global_feedback(html, new_html, remove_form_children=False)

        history_table.add(
            passing_copy,
            'base',
            global_feedback,
            driver.current_url
        )
        # except Exception as e:
        #     print(e)


# In[14]:


for i, v in enumerate(history_table.table['values']):
    jv = json.loads(v)
    for key, value in jv.items():
        if key not in history_table.table.columns:
            history_table.table[key] = None
        history_table.table.loc[i, key] = value


# In[19]:


history_table.table


# In[ ]:




