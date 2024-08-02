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

from oraclai.form_nexus.utils import create_driver, get_xpath, get_application_context


# In[2]:


load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Global Variables
HEADLESS = False
TEXT_EMBEDDING_METHOD = 'ADA'
GRAPH_EMBEDDING_METHOD = 'NODE2VEC'

URL = 'https://www.united.com/en/us'
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
            '//BODY/HEADER[1]/DIV[2]/DIV[1]/DIV[1]/SECTION[2]/DIV[2]/FORM[1]'
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


try:
    app_context = get_application_context(driver).replace('\n', ' ')
except:
    app_context = None


# In[8]:


input_widget_context = ''

for i in inputs:
    if i.tag_name != 'input':
        continue
    
    input_id = i.get_attribute('id')
    
    try:
        label = form.find_element(By.XPATH, f'//*[@for="{input_id}"]').text.replace('\n', ' ')
        input_widget_context += f'This input is about {label}. {label} is [MASK]. '
    except:
        label = i.get_attribute('title') or i.get_attribute('placeholder') or i.get_attribute('name') or i.get_attribute('id')
        if label is not None:
            input_widget_context += f'This input is about {label}. {label} is [MASK]. '

# print(input_widget_context)


# In[3]:


FORM_FUNC = 'Search'

prompt = f'''
The app is {app_context if app_context is not None else ''}, in its {FORM_FUNC} form. {input_widget_context}
'''.strip()


# In[ ]:


prompt


# In[14]:


from openai import OpenAI
client = OpenAI()

response = client.chat.completions.create(
  model="gpt-4",
  messages=[
    {
      "role": "system",
      "content": "You are required to generate values for a given input or list of inputs given in a text. Please create an array of values, the first element is a passing value for the inputs, and the rest are failing values. Consider the relationships of fields for generating failing values. Please note that each [MASK] is showing a different input. Give the values for different inputs in arrays, like the following format (exclude the comments from your answer):\n[\n{\n[first_input_name]: [first_input_value],\n[second_input_name]: [second_input_value]\n...\n},\n{\n[first_input_name]: [first_input_value],\n[second_input_name]: [second_input_value]\n...\n},\n...\n]"
    },
    {
      "role": "user",
      "content": prompt
    }
  ],
  temperature=0,
  max_tokens=2048,
  top_p=1,
  frequency_penalty=0,
  presence_penalty=0
)


# In[15]:


values = json.loads(response.choices[0].message.content)

passing = values[0]
failing = values[1:]

print("Passing:", passing)
print()

for f in failing:
    print("Failing:", f)
    print()


# In[ ]:




