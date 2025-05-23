# MasterversAcharya: AI-Powered Spiritual Guidance Agent

MasterversAcharya is an AI-powered chatbot that serves as a spiritual guide for individuals across multiple religions and those who identify as non-religious. The agent provides insights, learning resources, and personalized responses to spiritual and religious queries, fostering inclusivity and knowledge-sharing in a respectful and engaging manner.

## Table of Contents

- [Overview](#overview)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Components](#running-the-components)
- [API Documentation](#api-documentation)
- [Telegram Bot](#telegram-bot)
- [Testing](#testing)
- [Debugging](#debugging)
- [Contributing](#contributing)

## Overview

MasterversAcharya combines Google's Generative AI with a custom-built spiritual knowledge framework to provide users with:

- Religious information across major world religions
- Philosophical perspectives on spiritual topics
- Comparative religious insights
- Daily spiritual wisdom and quotes
- Guided meditation instructions
- Interfaith dialogue facilitation
- Spiritual practice guides

The system is accessible through a RESTful API and a Telegram bot interface, allowing users to engage with the spiritual AI assistant from their preferred platform.

## Project Structure

```
/Masterverseacharya/                  # Project Root
├── .env                            # Environment variables (e.g., API keys)
├── docs/                           # Documentation files
│   ├── API.md                      # API reference documentation
│   ├── API_TESTS.md                # API testing guidelines and examples
│   ├── ARCHITECTURE.md             # System architecture documentation
│   └── TELEGRAM_BOT_SETUP.md       # Telegram bot setup and usage guide
│
├── masterversacharya/              # Core Python package for the agent
│   ├── __init__.py                 # Package initialization
│   ├── agent.py                    # Main MasterversAcharya agent (ADK based)
│   └── spiritual_api.py            # Core spiritual knowledge API logic
│
├── requirements.txt                # Project dependencies
├── setup.py                        # Package installation configuration
├── telegram_bot.py                 # Telegram bot implementation
├── test_api.sh                     # API testing shell script
├── README.md                       # This file
├── .gitattributes                  # Git attributes
├── .gitignore                      # Git ignore rules (if present)
├── spiritual_responses.csv         # Example spiritual responses
├── spiritual_responses_comprehensive.csv # Comprehensive spiritual responses
├── test_spiritual_questions.sh     # Shell script for testing spiritual questions
└── agent.py                        # Legacy/alternative agent (at root, consider removal if redundant)
└── spiritual_api.py                # Legacy/alternative spiritual API (at root, consider removal if redundant)
```

**Note:** The primary application code resides within the `masterversacharya` package. The `agent.py` and `spiritual_api.py` files at the project root are likely legacy or development versions and are not used by the ADK agent when run as a package. For clarity, consider removing them if they are no longer needed.

## Component Descriptions

### Core Components

- **`masterversacharya/agent.py`**: The main implementation of the MasterversAcharya agent, built on Google's ADK (Agent Development Kit). It defines the agent's functionality, personality, and API tools. This is the agent loaded by the `adk api_server`.

- **`masterversacharya/spiritual_api.py`**: Defines the `SpiritualKnowledgeAPI` class, which is utilized by `masterversacharya/agent.py`. It handles the logic for querying the generative AI model and providing structured spiritual knowledge.

- **`telegram_bot.py`**: A full-featured Telegram bot that allows users to interact with the MasterversAcharya agent via the ADK API server. Supports session management, conversation tracking, and user-friendly commands.

### Support Files

- **requirements.txt**: Lists all Python dependencies required for the project.

- **setup.py**: Configuration for packaging and distributing the MasterversAcharya application.

- **test_api.sh**: Bash script for testing the API endpoints and verifying functionality.

## Installation

### Prerequisites

- Python 3.8 or higher
- Google ADK (Agent Development Kit)
- A Telegram bot token (if using the Telegram interface)

### Steps

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd Acharya
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Install the package in development mode:
   ```bash
   pip install -e .
   ```

## Configuration

### Environment Variables

Create a `.env` file in the root directory with the following variables:

```
# For Google Generative AI
GOOGLE_API_KEY=your_google_api_key

# For Telegram Bot
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
```

## Running the Components

### Starting the API Server

The MasterversAcharya agent runs on Google's ADK server:

```bash
adk api_server
```

This starts the server on http://127.0.0.1:8000 by default.

### Running the Telegram Bot

```bash
python telegram_bot.py
```

Make sure the API server is running before starting the Telegram bot.

## API Documentation

Detailed API documentation is available in `docs/API.md`. The API supports the following endpoints:

- **/list-apps**: List available applications
- **/run**: Send a message to the MasterversAcharya agent
- **/apps/{app_name}/users/{user_id}/sessions**: Manage user sessions

See `docs/API_TESTS.md` for example API calls and usage patterns.

## Telegram Bot

The Telegram bot provides a user-friendly interface to interact with MasterversAcharya. It supports:

- Session management with `/newsession`, `/listsessions`, and `/deletesession` commands
- Natural language conversations with the spiritual guide
- Interactive inline buttons for selecting options
- Automatic session creation for new users

Full documentation is available in `docs/TELEGRAM_BOT_SETUP.md`.

## Testing

### API Testing

Run the test script to verify API functionality:

```bash
bash test_api.sh
```

This script tests various API endpoints including session creation, message handling, and response generation.

## Debugging

### Common Issues and Solutions

#### API Server Issues

- **404 Not Found Error**: Ensure the agent class in `masterversacharya/agent.py` is correctly defined and that the `masterversacharya` package is installed (e.g., `pip install -e .`). The ADK server needs to find a valid agent implementation within this package.

- **Module Import Errors**: Verify that `masterversacharya/spiritual_api.py` is correctly imported by `masterversacharya/agent.py`. Check import paths and ensure the package structure is intact.

- **API Not Responding**: Make sure the ADK server is running (e.g., `adk api_server`) and that the `masterversacharya` agent is correctly registered and loaded.

#### Telegram Bot Issues

- **Conflict Errors**: If you see `telegram.error.Conflict` errors, ensure only one instance of the bot is running. Kill other instances with `ps aux | grep telegram_bot.py` followed by `kill <PID>`.

- **Connection Refused**: Check that the API server is running and the `BASE_URL` in `telegram_bot.py` is correct (default: http://127.0.0.1:8000).

- **Missing Dependencies**: Ensure all requirements from `requirements.txt` are installed.

- **Token Issues**: Verify your Telegram bot token is correctly set in your configuration.

### Logging

Both the API server and Telegram bot output detailed logs to help with debugging:

- **API Server Logs**: View logs directly in the terminal where `adk api_server` is running.

- **Telegram Bot Logs**: The bot outputs logs to the console with timestamps, message content, and API responses.

### Debugging Steps

1. **Check Server Status**: Verify the ADK server is running with `adk list-apps`.
2. **Test Direct API Calls**: Use `test_api.sh` to test API functionality directly.
3. **Review Logs**: Check both API server and bot logs for error messages.
4. **Verify Configuration**: Ensure all environment variables and settings are correct.
5. **Kill Conflicting Processes**: For Telegram bot issues, ensure no duplicate instances are running.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

Developed by MasterversAcharya Team

- **Multi-Religious Knowledge Base**: Covers major religions (Christianity, Islam, Hinduism, Buddhism, Judaism, Sikhism, etc.) and spiritual philosophies.
- **Non-Religious & Philosophical Support**: Provides answers for those exploring atheism, agnosticism, and humanist views.
- **AI-Driven Personalized Responses**: Answers tailored to user beliefs and spiritual interests.
- **Question & Answer Mechanism**: Allows users to ask specific queries related to faith, rituals, traditions, philosophy, and spirituality.
- **Daily Spiritual Insights & Quotes**: Provides daily affirmations, scriptures, or philosophical thoughts.
- **Interactive Learning Modules**: Guided lessons on different faiths, meditation practices, and spiritual philosophies.
- **Meditation Guides**: Offers guided meditation scripts based on various traditions.
- **Interfaith Dialogue**: Generates educational dialogues between different religious perspectives.

## Installation

1. Clone this repository:
```
git clone <repository-url>
cd masterversacharya
```

2. Install the required dependencies:
```
pip install -r requirements.txt
```

3. Set up environment variables by creating a `.env` file with your API keys:
```
GOOGLE_API_KEY=your_google_api_key
```

## Usage

### Running the Agent with Google ADK

To run the MasterversAcharya agent using Google ADK in interactive mode:

```bash
adk run masterversacharya
```

You can also save the session for later use:

```bash
adk run masterversacharya --save_session
```

### Running the Agent with ADK API Server

ADK provides a built-in API server that follows standard protocols. To run MasterversAcharya as an API server:

```bash
adk api_server
```

This will start a FastAPI server on http://0.0.0.0:8000.

#### Creating a Session

```bash
curl -X POST http://0.0.0.0:8000/apps/masterversacharya/users/u_123/sessions/s_123 \
  -H "Content-Type: application/json" \
  -d '{"state": {}}'
```

#### Sending a Query

```bash
curl -X POST http://0.0.0.0:8000/run \
-H "Content-Type: application/json" \
-d '{
"app_name": "masterversacharya",
"user_id": "u_123",
"session_id": "s_123",
"new_message": {
    "role": "user",
    "parts": [{
    "text": "What is the meaning of karma in Buddhism?"
    }]
}
}'
```

#### Streaming Responses

For streaming responses:

```bash
curl -X POST http://0.0.0.0:8000/run_sse \
-H "Content-Type: application/json" \
-d '{
"app_name": "masterversacharya",
"user_id": "u_123",
"session_id": "s_123",
"new_message": {
    "role": "user",
    "parts": [{
    "text": "What is the meaning of karma in Buddhism?"
    }]
},
"streaming": true
}'
```

### Running the Agent with Web UI

ADK also provides a web-based user interface for interacting with your agent:

```bash
adk web
```

This will start a web server with a user-friendly interface for interacting with MasterversAcharya.



## Available Functions

- `get_religious_information`: Get information about a specific religion
- `get_philosophical_perspective`: Get information about a philosophical perspective
- `compare_religions`: Compare two religions on a specific aspect
- `get_daily_spiritual_insight`: Get a daily spiritual insight or quote
- `get_meditation_guide`: Get a guided meditation based on spiritual traditions
- `get_available_religions`: Get a list of available religions in the knowledge base
- `get_available_philosophies`: Get a list of available philosophical traditions
- `get_interfaith_dialogue`: Generate an interfaith dialogue on a specific topic
- `get_spiritual_practice_guide`: Get a guide for a specific spiritual practice

## Project Structure

- `agent.py`: Main agent file with function definitions and ADK agent configuration
- `spiritual_api.py`: API client for fetching spiritual information
- `setup.py`: Package setup for installation with pip
- `requirements.txt`: Required Python dependencies
- `.env`: Environment variables for API keys
- `ARCHITECTURE.md`: Technical architecture documentation
- `API.md`: API usage documentation

## Supported Religions and Philosophies

### Religions
- Christianity
- Islam
- Hinduism
- Buddhism
- Judaism
- Sikhism
- Taoism
- Jainism
- Shintoism
- Zoroastrianism
- Baha'i Faith
- Confucianism
- Atheism
- Agnosticism
- Humanism

### Philosophical Traditions
- Stoicism
- Existentialism
- Nihilism
- Pragmatism
- Utilitarianism
- Hedonism
- Rationalism
- Empiricism
- Idealism
- Materialism

## License

[Specify License]
