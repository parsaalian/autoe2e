import time
from urllib.parse import urlparse

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from autoe2e.crawler.action import Action, ClickAction, FormAction, Element


class CandidateActionExtractor:
    @staticmethod
    def extract_candidate_actions(driver: WebDriver) -> list[Action]:
        click_actions = CandidateActionExtractor.extract_click_actions(driver)
        form_actions = CandidateActionExtractor.extract_form_actions(driver)
        actions = click_actions + form_actions
        return actions


    @staticmethod
    def extract_click_actions(driver: WebDriver) -> list[Action]:
        '''
        CLICK_ACTION_TAGS = ['a', 'button']
        
        # list(map(lambda x: print(x.get_attribute('outerHTML')), driver.find_elements(By.TAG_NAME, 'a')))
        elements = CandidateActionExtractor.extract_action_group_elements(driver, CLICK_ACTION_TAGS)
        elements = list(filter(lambda x: "type=\"submit\"" not in x.outerHTML, elements))
        elements = list(filter(lambda x: CandidateActionExtractor.is_element_same_origin(driver, x), elements))
        actions: list[Action] = list(map(ClickAction, elements))
        return actions
        '''
        actionables = []

        response = driver.execute_cdp_cmd("Runtime.evaluate", {
            "expression": "document.querySelectorAll('body *')",
            "returnByValue": False
        })

        node_list_object_id = response['result']['objectId']

        properties = driver.execute_cdp_cmd("Runtime.getProperties", {
            "objectId": node_list_object_id
        })
        
        for p in properties['result']:
            if 'value' in p and 'objectId' in p['value']:
                try:
                    object_id = p['value']['objectId']
                    
                    tag_name = driver.execute_cdp_cmd("Runtime.callFunctionOn", {
                        "objectId": object_id,
                        "functionDeclaration": """
                            function() {
                                return this.tagName.toLowerCase();
                            }
                        """,
                        "returnByValue": True
                    })['result']['value']
            
                    actionable = (tag_name in ['a', 'button', 'input', 'select']) or (p['value']['className'] in ['HTMLButtonElement', 'HTMLAnchorElement', 'HTMLInputElement', 'HTMLSelectElement'])
                    
            
                    if not actionable:
                        try:
                            listeners = driver.execute_cdp_cmd("DOMDebugger.getEventListeners", {"objectId": object_id})['listeners']
                            actionable = any(l['type'] == 'click' for l in listeners)
                        except Exception as e:
                            pass
                    
                    if actionable:
                        xpath = driver.execute_cdp_cmd("Runtime.callFunctionOn", {
                            "objectId": object_id,
                            "functionDeclaration": """
                                function() {
                                    const xpathSegments = [];
                                    let currentElement = this;
                                    while (currentElement && currentElement.nodeType === Node.ELEMENT_NODE) {
                                        let segment;
                                        const parent = currentElement.parentNode;
                                        if (parent) {
                                            const children = Array.from(parent.children);
                                            const sameTagSiblings = children.filter(child => child.tagName === currentElement.tagName);
                                            if (sameTagSiblings.length > 1) {
                                                const index = sameTagSiblings.indexOf(currentElement) + 1;
                                                segment = `${currentElement.tagName.toLowerCase()}[${index}]`;
                                            } else {
                                                segment = currentElement.tagName.toLowerCase();
                                            }
                                        } else {
                                            segment = currentElement.tagName.toLowerCase();
                                        }
                                        xpathSegments.unshift(segment);
                                        currentElement = parent;
                                    }
                                    return xpathSegments.length ? '/' + xpathSegments.join('/') : null;
                                }
                            """,
                            "returnByValue": True
                        })['result']['value']
                        
                        element = driver.find_element(By.XPATH, xpath)
                        actionables.append(element)
                except:
                    pass
        
        elements = list(map(lambda e: Element(driver, e), actionables))
        
        visible_elements: list[Element] = []
        for e in elements:
            # try:
            if CandidateActionExtractor.is_element_visible(driver, e):
                visible_elements.append(e)
        
        visible_elements = list(filter(lambda x: "type=\"submit\"" not in x.outerHTML, visible_elements))
        visible_elements = list(filter(lambda x: CandidateActionExtractor.is_element_same_origin(driver, x), visible_elements))
        actions: list[Action] = list(map(ClickAction, visible_elements))
        return actions
    
    
    @staticmethod
    def extract_form_actions(driver: WebDriver) -> list[Action]:
        FORM_ACTION_TAGS = ['form']
        elements = CandidateActionExtractor.extract_action_group_elements(driver, FORM_ACTION_TAGS)
        actions: list[Action] = list(map(FormAction, elements))
        return actions
    
    
    @staticmethod
    def extract_action_group_elements(driver: WebDriver, tags: list[str]) -> list[Element]:
        elements = []
        
        for tag in tags:
            elements += CandidateActionExtractor._extract_tag_elements(driver, tag)
        
        visible_elements: list[Element] = []
        for e in elements:
            # try:
            if CandidateActionExtractor.is_element_visible(driver, e):
                visible_elements.append(e)
            # except:
            #     print('error extracting element', e)
        return visible_elements


    @staticmethod
    def is_element_visible(driver: WebDriver, element: Element) -> bool:
        return element.get(driver).is_displayed()
    
    
    @staticmethod
    def is_element_same_origin(driver: WebDriver, element: Element) -> bool:
        href = element.get(driver).get_attribute('href')
        if href is None:
            return True
        
        parsed1 = urlparse(driver.current_url)
        parsed2 = urlparse(href)
        
        return (parsed1.scheme == parsed2.scheme and
            parsed1.hostname == parsed2.hostname and
            parsed1.port == parsed2.port)
    
    
    @staticmethod
    def _extract_tag_elements(driver: WebDriver, tag: str) -> list[Element]:
        time.sleep(0.1)
        
        elements = []
        
        for e in driver.find_elements(By.TAG_NAME, tag):
            # print(e.get_attribute('outerHTML'))
            # try:
            elements.append(Element(driver, e))
            # except:
            #     print('error extracting element', e)
        return elements
