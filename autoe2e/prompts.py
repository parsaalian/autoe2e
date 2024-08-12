import json

from langchain_core.messages import HumanMessage

from .utils import clean_children_html


CONTEXT_EXTRACTION_SYSTEM_PROMPT = """
Given the provided information about a webpage, your task is to provide a brief and abstract description of the webpage's primary purpose or function.
Output Guidelines:
* Brevity: Keep the description concise (aim for 1-2 sentences).
* Abstraction: Avoid specific details or variable names. Use general terms to describe the content and function. (Example: Instead of "a page showing results for searching for a TV," say "a page displaying search results for a product query.")
* Focus on Purpose: Prioritize describing the main intent of the page. What is it designed for the user to do or learn?
* No Extra Explanations: Just provide the context. Avoid adding commentary or assumptions.
""".strip()


CONTEXT_EXTRACTION_USER_PROMPT = """
The description of the website is: {description}
The previous state was: {previous_state}
The previous action was: {previous_action}
""".strip()


FUNCTIONALITY_EXTRACTION_SYSTEM_PROMPT = """
Given a webpage's purpose and content (webpage_context), the outerHTML of an action element (action_element), and optionally the user's last action that led to this state, your task is to infer the most likely functionalities associated with that action element.
These functionalities should be user-centric actions that produce measurable outcomes within the application, are testable through E2E testing, and are essential to the presence of the action element.

Output Format:
Your is enclosed in two tags:
<Reasoning>:
- An enumerated list of at most five functionalities potentially connected to the element.
- For each functionality, answer the following questions concisely:
    1. Would developers write E2E test cases for this in the real world? It should be non-navigational, not menu-related, and not validation.
    2. Is the functionality a final user goal in itself or is it always a step in doing something else?
    3. Is this overly abstract/vague? If so, break it down into more testable sub-functionalities.
- Avoid repeating the questions in your responses every time.
<Response>:
- A JSON array of objects, each containing:
    - probability: (0.0 to 1.0) Likelihood of this functionality exists.
    - feature: A concise description of the user action (e.g., "add item to cart").
- Sorted by probability in descending order.
- Parsable by `json.loads`.
- Can be an empty array if no valid functionalities are found.
""".strip()


SIMILARITY_SYSTEM_PROMPT = """
Given a description of a software feature and a list of other software feature descriptions, your task is to determine if the initial feature matches any features in the list.

Output format:
Your analysis is enclosed in two tags:
<Reasoning>:
- For each item in the list, argue why the base feature and the feature in the list are or aren't describing the same action being performed in the app.
    - Are they exactly or semantically equivalent?
    - If they are different, how are they different?
- Avoid repeating the questions in your responses every time.
- Your analyses should be short and concise.
<Response>:
- A JSON object containing the following keys:
    - match: true If any feature in the list matches the base feature, false if not.
    - match_index: An array of indices of matched features in the list. Only include this key if there is a matching feature.
    - combined_text: If the features match, a concise description of that feature. Only include this key if there is a matching feature. You can omit some of the redundant words to keep this sentence simple.
- Parsable by `json.loads`.
""".strip()


FINALITY_SYSTEM_PROMPT = """
Given the context of a webpage, an action element, and a list of features and scenarios, your task is to determine whether the action is the final action in the chain of actions for performing each of the features.

Output format:
Your analysis is enclosed in two tags:
<Reasoning>:
- For each feature in the list, argue why executing the action would or would not conclude the feature.
- Avoid repeating the description of the feature.
- Your analyses should be short and concise.
<Response>:
- An array of Python booleans, where index i is True if the action concludes feature i.
""".strip()


CRITICAL_ACTION_SYSTEM_PROMPT = """
Given an element in a web application, your task is to determine if the element is a critical action.
A critical action is an action that its effects are irreversible, such as deleting an account or making a purchase.
Please return a boolean value indicating if the element is a critical action. The boolean should be in Python format (True or False).
Just return the boolean and no further explanation.
""".strip()


FORM_VALUE_SYSTEM_PROMPT = """
Given a form element in a web application, your task is to generate a set of values so that the form can be submitted successfully.
The format for your response should be a JSON where the keys are the data-testid attributes of the input elements and the values are the values that should be filled in.
If the elements are radios or checkboxes, the values should be booleans.
If the elements are selects, the values should be the value attribute of the selected option.
Your response should be parsable by json.loads. Just include your response in the JSON, no additional information is needed. Avoid formatting the JSON for markdown or any other format.
""".strip()


def create_simple_user_messages(prompt):
    return HumanMessage(content=[
        { "type": "text", "text": prompt }
    ])


def create_context_user_messages(text_inputs, base64_image):
    return HumanMessage(content=[
        {
            "type": "text", "text": CONTEXT_EXTRACTION_USER_PROMPT.format(**text_inputs)
        },
        {
            "type": "image_url",
            "image_url": {
                "url": f"data:image/png;base64,{base64_image}"
            },
        }
    ])


def create_functionality_user_messages(context, action_element, previous_action=None):
    data = {
        "webpage_context": context,
        "action_element": clean_children_html(action_element),
    }

    if previous_action:
        data["previous_action"] = previous_action
    
    return HumanMessage(content=[
        { "type": "text", "text": json.dumps(data) }
    ])


def create_similarity_user_messages(base_functionality, functionalities):
    return HumanMessage(content=[
        {
            "type": "text",
            "text": f'Base feature:\n{base_functionality}\nThe list of functionalities:\n{functionalities}'
        }
    ])


def create_finality_user_messages(context, action_element, functionalities):
    return HumanMessage(content=[
        {
            "type": "text",
            "text": f'The context of the webpage is: {context}\nThe action element is: {clean_children_html(action_element)}\nThe list of functionalities:\n{functionalities}'
        }
    ])
