# AutoE2E

Source code and benchmark subjects for "AutoE2E: Feature-Driven End-To-End Test Generation."

![AutoE2E Workflow](./workflow.png)

## Project Structure

```
autoe2e/
├── main.py                      # Main entry point for running AutoE2E
├── requirements.txt             # Python package dependencies
├── baseline-prompts.md          # Baseline prompts used for evaluation
├── README.md                    # Project documentation
├── workflow.png                 # Workflow diagram
├── .env.example                 # Environment variables template
│
├── autoe2e/                     # Main source code directory
│   ├── __init__.py
│   ├── prompts.py               # LLM prompts for context and feature extraction
│   ├── llm_api_call.py          # API calls to LLM providers (Anthropic, OpenAI)
│   ├── infer_utils.py           # Inference utilities and model chains
│   ├── init_utils.py            # Initialization utilities
│   ├── loop_utils.py            # Main loop logic for test generation
│   ├── manual_ndd.py            # Manual navigation and interaction logic
│   ├── mongo_utils.py           # MongoDB database operations
│   │
│   ├── browser/                 # Browser automation components
│   │   ├── driver.py            # WebDriver setup and configuration
│   │   └── utils.py             # Browser utility functions
│   │
│   ├── crawler/                 # Web crawling functionality
│   │   ├── crawl_context.py     # Crawling context management
│   │   ├── action/              # Action-related modules
│   │   ├── config/              # Crawler configuration
│   │   └── state/               # State management
│   │
│   └── utils/                   # General utilities
│       ├── hash.py              # Hashing utilities
│       ├── logger.py            # Logging configuration
│       ├── queue.py             # Queue data structures
│       └── singleton.py         # Singleton pattern implementation
│
├── benchmark/                   # Evaluation subjects and testing server
│   ├── _log-server/             # Server for tracking feature execution
│   │   ├── extract.py           # Flask app for coverage evaluation
│   │   ├── coverage.py          # Coverage calculation logic
│   │   └── requirements.txt     # Server dependencies
│   │
│   ├── dimeshift/               # DimeShift application subject
│   ├── ever-traduora/           # Ever Traduora application subject
│   ├── mantisbt/                # MantisBT application subject
│   ├── pet-clinic/              # PetClinic application subject
│   ├── realworld/               # RealWorld application subject
│   ├── saleor/                  # Saleor application subject
│   └── taskcafe/                # TaskCafe application subject
│
└── configs/                     # Application configuration files
    ├── ADMIN.json               # Admin application config
    ├── DIMESHIFT.json           # DimeShift config
    ├── EVERTRADUORA.json        # Ever Traduora config
    ├── MANTISBT.json            # MantisBT config
    ├── PETCLINIC.json           # PetClinic config
    ├── REALWORLD.json           # RealWorld config
    ├── SALEOR.json              # Saleor config
    └── TASKCAFE.json            # TaskCafe config
```


## Prerequisites

- **Python 3.11 or higher** is required to run this project. The installation will fail on older Python versions.

To check your Python version:
```bash
python --version
```

If you need to install or upgrade Python, visit [python.org/downloads](https://www.python.org/downloads/).

## Setup

### Virtual Environment (Recommended)

It is strongly recommended to use a virtual environment to isolate project dependencies and avoid conflicts with other Python projects.

**Option 1: Using venv (built-in)**

```bash
# Create virtual environment
python -m venv venv

# Activate on Linux/macOS
source venv/bin/activate

# Activate on Windows
venv\Scripts\activate
```

**Option 2: Using virtualenv**

```bash
# Install virtualenv if not already installed
pip install virtualenv

# Create virtual environment
virtualenv venv

# Activate on Linux/macOS
source venv/bin/activate

# Activate on Windows
venv\Scripts\activate
```

**Option 3: Using conda**

```bash
# Create virtual environment
conda create -n autoe2e python=3.11

# Activate environment
conda activate autoe2e
```

Once activated, your terminal prompt should show the environment name (e.g., `(venv)` or `(autoe2e)`).


## Requirements

Install the required packages using the following command:

```bash
pip install -r requirements.txt
```

## Setup

### Virtual Environment (Recommended)

It is strongly recommended to use a virtual environment to isolate project dependencies and avoid conflicts with other Python projects.

**Option 1: Using venv (built-in)**

```bash
# Create virtual environment
python -m venv venv

# Activate on Linux/macOS
source venv/bin/activate

# Activate on Windows
venv\Scripts\activate
```

**Option 2: Using virtualenv**

```bash
# Install virtualenv if not already installed
pip install virtualenv

# Create virtual environment
virtualenv venv

# Activate on Linux/macOS
source venv/bin/activate

# Activate on Windows
venv\Scripts\activate
```

**Option 3: Using conda**

```bash
# Create virtual environment
conda create -n autoe2e python=3.11

# Activate environment
conda activate autoe2e
```

Once activated, your terminal prompt should show the environment name (e.g., `(venv)` or `(autoe2e)`).

## Usage

### Docker (Recommended)

The easiest way to run AutoE2E is using Docker Compose. See [DOCKER.md](DOCKER.md) for complete setup instructions.

**Quick start:**
```bash
cd autoe2e
# Create .env file with your API keys
docker-compose up --build
```

### Local Development

Before running the project locally, you need to set the environment variables in the `.env` file. This includes:

1. `APP_NAME`: The name of the application you want to generate E2E test cases for. This needs to match one of the configs in `./configs` folder.
2. `ANTHROPIC_API_KEY`: The API key for the Anthropic platform. You can get this by signing up at [Anthropic](https://anthropic.com/).
3. `OPENAI_API_KEY`: The API key for OpenAI (required for embeddings). Get this at [OpenAI Platform](https://platform.openai.com/).
4. `ATLAS_URI`: The MongoDB Atlas URI for storing the Action-Feature Database (AFD) and Feature Database (FD).
Before running the project, you need to create and configure a `.env` file with the required environment variables.

### Step 1: Create the .env file

Create your `.env` file from the provided template:

```bash
cp .env.example .env
```

This file is required before running `main.py`. Without it, you will encounter runtime errors about missing environment variables.

### Step 2: Configure Environment Variables

Open the newly created `.env` file and populate it with your own API keys and configuration values. The required variables are:

1. `APP_NAME`: The name of the application you want to generate E2E test cases for. This needs to match one of the configs in `./configs` folder.

2. `ANTHROPIC_API_KEY`: The API key for the Anthropic platform used for primary model reasoning.

   - Sign up at [Anthropic Console](https://console.anthropic.com/)
   - Navigate to the API Keys section
   - Click "Create Key" and give it a name
   - Copy the generated API key to your `.env` file
   - **Important**: Verify that the model version in `autoe2e/llm_api_call.py` is the latest version, otherwise the application will crash
   - **Optional**: You can switch from Anthropic's Sonnet to OpenAI's GPT-4 by changing `sonnet_chain` to `gpt4o_chain` in `autoe2e/infer_utils.py` (requires OpenAI API key)

3. `OPENAI_API_KEY`: The API key for OpenAI platform used for generating feature embeddings.

   - Sign up or log in at [OpenAI Platform](https://platform.openai.com/)
   - Navigate to [API Keys](https://platform.openai.com/api-keys)
   - Click "Create new secret key" and give it a name
   - Copy the generated API key to your `.env` file (you won't be able to see it again)
   - **Note**: This is required even if using Anthropic for reasoning, as OpenAI's embedding model is used to create feature embeddings for database storage

4. `ATLAS_URI`: The MongoDB Atlas URI for storing the Action-Feature Database (AFD) and Feature Database (FD).

   - Sign up for a free account at [MongoDB Atlas](https://www.mongodb.com/cloud/atlas/register)
   - Create a new project (or use an existing one)
   - Click "Build a Database" and select the free tier (M0)
   - Choose your preferred cloud provider and region
   - Click "Create Cluster" (this may take a few minutes)
   - **Set up database access:**
     - Go to "Database Access" in the left sidebar
     - Click "Add New Database User"
     - Choose authentication method (Username/Password recommended)
     - Create a username and password (save these securely)
     - Set user privileges to "Read and write to any database"
     - Click "Add User"
   - **Set up network access:**
     - Go to "Network Access" in the left sidebar
     - Click "Add IP Address"
     - For development, click "Allow Access from Anywhere" (0.0.0.0/0)
     - For production, add only your specific IP addresses
     - Click "Confirm"
   - **Get your connection string:**
     - Go to "Database" in the left sidebar
     - Click "Connect" on your cluster
     - Select "Connect your application"
     - Choose "Python" as the driver and select your version
     - Copy the connection string (it looks like: `mongodb+srv://<username>:<password>@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority`)
     - Replace `<username>` with your database username
     - Replace `<password>` with your database password
     - Paste the complete URI into your `.env` file as the value for `ATLAS_URI`

### Step 3: Run the Project

Once your `.env` file is configured with the appropriate values, you can run the project using the following command:

```bash
python main.py
```

**Note:** For local development, you'll also need to manually start the backend and frontend services. See the benchmark applications for setup instructions.

## LLM Prompts

The prompts used for different parts of our workflow is available in `./autoe2e/prompts.py` file. We use the following prompt for context extraction:

> Given the provided information about a webpage, your task is to provide a brief and abstract description of the webpage's primary purpose or function.
> Output Guidelines:
>
> - Brevity: Keep the description concise (aim for 1-2 sentences).
> - Abstraction: Avoid specific details or variable names. Use general terms to describe the content and function. (Example: Instead of "a page showing results for searching for a TV," say "a page displaying search results for a product query.")
> - Focus on Purpose: Prioritize describing the main intent of the page. What is it designed for the user to do or learn?
> - No Extra Explanations: Just provide the context. Avoid adding commentary or assumptions.

and the following for feature extraction:

> Given a webpage's purpose and content (webpage_context), the outerHTML of an action element (action_element), and optionally the user's last action that led to this state, your task is to infer the most likely functionalities associated with that action element.
> These functionalities should be user-centric actions that produce measurable outcomes within the application, are testable through E2E testing, and are essential to the presence of the action element.
> Output Format:
> Your is enclosed in two tags:
> \<Reasoning>:
>
> - An enumerated list of at most five functionalities potentially connected to the element.
> - For each functionality, answer the following questions concisely:
>   1. Would developers write E2E test cases for this in the real world? It should be non-navigational, not menu-related, and not validation.
>   2. Is the functionality a final user goal in itself or is it always a step in doing something else?
>   3. Is this overly abstract/vague? If so, break it down into more testable sub-functionalities.
> - Avoid repeating the questions in your responses every time.
>   \<Response>:
> - A JSON array of objects, each containing:
>   - probability: (0.0 to 1.0) Likelihood of this functionality exists.
>   - feature: A concise description of the user action (e.g., "add item to cart").
> - Sorted by probability in descending order.
> - Parsable by `json.loads`.
> - Can be an empty array if no valid functionalities are found.

Furthermore, the baseline prompts are available in `./baseline-prompts.md`.

## Subjects

The subjects used in our evaluations are available in `./benchmark` folder. Furthermore, the server created for tracking the execution of features is available in `./benchmark/_log-server` folder. You need to have a `Redis` server installed and running to be able to use the server.

To run the server:

```bash
cd benchmark/_log-server

pip install -r requirements.txt

flask --app extract.py --debug run
```

### Server Endpoints

The server has the following endpoints:

1. `/start-evaluate/<app-name>`: Start the coverage evaluation for the given application.
2. `/end-evaluate`: End the coverage evaluation for the given application. It will return the coverage rate.

To test the server, you can run the `PetClinic` application located in `./benchmark/pet-clinic` and use the server.
