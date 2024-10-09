# Prompt for Generating E2E Test Cases

## PromptA - Browsing the Web Application

### Goal
Given a web application hosted at {URL}, generate end-to-end (E2E) test cases that cover a wide range of user interactions and functionalities.
You must use Browsing Agent to interact with the web application.

### Steps
Use the following steps to generate E2E test cases for the web application:

1. With the help of the Browsing Agent, analyze the web application's states and transitions to understand its structure and key features.
2. Identify the main functionalities and user flows within the application, focusing on common actions such as logging in, searching for items, adding items to a cart, and checking out.
3. For each identified feature, create a detailed test scenario that includes:
   (a) The initial state of the application
   (b) A sequence of user actions to be performed
   (c) Expected outcomes and assertions to verify the correct behavior of the application
4. Ensure that the generated test cases are semantically meaningful and align with typical user behavior.
5. Provide the test cases in a format compatible with Selenium.

Use the example of an e-commerce application where a user adds a product to their shopping cart as a reference to generate similar test cases for other functionalities.


## PromptB - State transitions and user interactions

### Goal
Given a web application, generate end-to-end (E2E) test cases that cover a wide range of user interactions and functionalities.

### Steps
Use the following steps to generate E2E test cases for the web application:

1. Analyze the web application's states and transitions to understand its structure and key features from the given JSON file.
2. Identify the main functionalities and user flows within the application, focusing on common actions such as logging in, searching for items, adding items to a cart, and checking out.
3. For each identified feature, create a detailed test scenario that includes:
   (a) The initial state of the application
   (b) A sequence of user actions to be performed
   (c) Expected outcomes and assertions to verify the correct behavior of the application
4. Ensure that the generated test cases are semantically meaningful and align with typical user behavior.
5. Provide the test cases in a format compatible with Selenium.

Use the example of an e-commerce application where a user adds a product to their shopping cart as a reference to generate similar test cases for other functionalities.


## PromptC - Browsing and State transitions and user interactions

### Goal
Given a web application hosted at {URL}, generate end-to-end (E2E) test cases that cover a wide range of user interactions and functionalities.
You must use Browsing Agent to interact with the web application.

### Steps
Use the following steps to generate E2E test cases for the web application:

1. With the help of the Browsing Agent, analyze the web application. Also analyze the application states and transitions to understand its structure and key features from the given JSON file.
2. Identify the main functionalities and user flows within the application, focusing on common actions such as logging in, searching for items, adding items to a cart, and checking out.
3. For each identified feature, create a detailed test scenario that includes:
   (a) The initial state of the application
   (b) A sequence of user actions to be performed
   (c) Expected outcomes and assertions to verify the correct behavior of the application
4. Ensure that the generated test cases are semantically meaningful and align with typical user behavior.
5. Provide the test cases in a format compatible with Selenium.

Use the example of an e-commerce application where a user adds a product to their shopping cart as a reference to generate similar test cases for other functionalities.