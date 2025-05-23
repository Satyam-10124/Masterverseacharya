# MasterversAcharya Technical Architecture

This document outlines the technical architecture of the MasterversAcharya spiritual guidance agent system.

## System Overview

MasterversAcharya is built using Google's Agent Development Kit (ADK) and provides spiritual guidance across multiple religious and philosophical traditions. The system can operate in two modes:

1. **Interactive Mode**: Direct conversation through the ADK CLI
2. **API Mode**: RESTful API service for integration with other applications

## Core Components

### 1. Agent Core (`masterversacharya/agent.py`)

The central component, located at `masterversacharya/agent.py`, defines the agent's capabilities and behavior within the Google ADK framework:

- **Function Tools**: Specialized Python functions that act as tools for the agent to access spiritual knowledge (via `SpiritualKnowledgeAPI`).
- **Agent Configuration**: Settings for the underlying generative AI model (e.g., Gemini).
- **Response Generation**: Orchestrates conversational responses to user queries by utilizing its tools and the AI model.

### 2. Spiritual Knowledge API (`masterversacharya/spiritual_api.py`)

This module, at `masterversacharya/spiritual_api.py`, provides the core logic for accessing and processing spiritual information:

- **Content Generation**: Constructs prompts and interfaces with Google's Generative AI model (Gemini) to generate spiritual content.
- **Data Definitions**: Includes mappings for religions, philosophies, and categories.
- **Caching**: Implements a simple in-memory cache to store responses and reduce redundant AI model calls.

### 3. ADK API Server

The RESTful API is provided by the Google Agent Development Kit (ADK) itself. It's typically run using the command `adk api_server`. This server loads the `masterversacharya` agent (as defined in `masterversacharya/agent.py` and configured in `setup.py`) and exposes it via a FastAPI interface.

- **Endpoints**: Standard ADK RESTful interface for agent interaction (listing apps, session management, running the agent).
- **Session Management**: Handled by ADK's session services (e.g., InMemorySessionService by default).
- **Error Handling**: Provided by the ADK framework.
- **Documentation**: Auto-generated API docs available via the FastAPI server (usually at `/docs`).

### 4. API Clients (e.g., `telegram_bot.py`, `test_api.sh`)

Clients interact with the ADK API Server. Examples in this project include:
- **`telegram_bot.py`**: A Python-based Telegram bot that acts as a client to the API.
- **`test_api.sh`**: A shell script using `curl` to send requests to the API for testing purposes.
- An `api_client_example.py` is mentioned in some contexts but is not present in the main project structure; if it were a dedicated example client, it would demonstrate direct API interaction.

## Data Flow

```
┌─────────────┐    ┌───────────────┐    ┌───────────────────┐
│ User/Client │───▶│ API Server    │───▶│ Agent Core        │
└─────────────┘    └───────────────┘    └───────────────────┘
                          │                       │
                          │                       ▼
                          │               ┌───────────────────┐
                          └──────────────▶│ Spiritual API     │
                                          └───────────────────┘
```

1. User sends a query via CLI or API
2. Query is processed by the agent core
3. Agent uses spiritual knowledge functions as needed
4. Response is generated and returned to the user

## Technical Stack

- **Language**: Python 3.12+
- **AI Model**: Google Gemini 2.0 Flash
- **Framework**: Google ADK for agent capabilities
- **API**: FastAPI for RESTful service
- **Documentation**: Swagger/OpenAPI
- **Session Management**: InMemorySessionService (ADK)

## Deployment Options

### Local Development

```bash
# To run the agent interactively via CLI
adk run masterversacharya

# To start the API server for the agent
adk api_server
```
Ensure the `masterversacharya` package is installed (`pip install -e .`) before running these commands.

### Production Deployment

Options include:

- **Containerization**: Docker for consistent deployment
- **Cloud Hosting**: Google Cloud Run, AWS Lambda, or similar
- **API Gateway**: For security and rate limiting
- **Database**: Replace InMemorySessionService with persistent storage

## Multi-Agent Architecture (Future)

The system can be extended to a multi-agent architecture:

- **Coordinator Agent**: Routes queries to specialized agents
- **Specialized Agents**: Experts in specific traditions
- **Workflow Agents**: Handle complex multi-step processes

## Security Considerations

- **API Authentication**: Not currently implemented, recommended for production
- **Rate Limiting**: Recommended for production deployment
- **Content Filtering**: Implemented in agent instructions
- **Data Privacy**: No user data is stored persistently

## Monitoring and Logging

- **ADK Logs**: Available at `/var/folders/*/T/agents_log/agent.latest.log`
- **API Logs**: Standard FastAPI logging
- **Error Tracking**: Exceptions are logged but not currently sent to monitoring services

## Future Enhancements

1. **Web Interface**: Frontend for direct user interaction
2. **Multi-Agent System**: Specialized agents for different traditions
3. **Persistent Storage**: Database for conversation history
4. **Authentication**: User accounts and API keys
5. **Analytics**: Usage tracking and performance monitoring
