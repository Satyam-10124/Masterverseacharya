# MasterversAcharya API Documentation

This document provides comprehensive documentation for interacting with the MasterversAcharya agent through the ADK API server.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Project Structure](#project-structure)
3. [API Endpoints](#api-endpoints)
   - [Application Management](#application-management)
   - [Session Management](#session-management)
   - [Agent Interaction](#agent-interaction)
   - [Artifacts Management](#artifacts-management)
   - [Evaluation](#evaluation)
   - [Debugging](#debugging)
4. [Example Queries](#example-queries)
5. [Integrations](#integrations)
6. [Deployment](#deployment)
7. [Data Schemas](#data-schemas)
8. [Troubleshooting](#troubleshooting)

## Getting Started

### Prerequisites

- Python 3.9+ installed
- Google ADK installed
- Google API Key for Gemini (set as environment variable `GOOGLE_API_KEY`)

### Installation

Before using the ADK API server, you need to install the MasterversAcharya package in development mode:

```bash
# From the project root directory
pip install -e .
```

This step is crucial as it makes the masterversacharya module available to the ADK API server. The setup.py file should contain all the necessary dependencies for the project.

### Starting the API Server

To start the ADK API server:

```bash
adk api_server
```

This will launch a FastAPI server on http://0.0.0.0:8000.

## Project Structure

The MasterversAcharya project has the following structure:

```
/Acharya
├── docs/                      # Documentation files
│   └── API.md                 # This API documentation
├── masterversacharya/         # Main package directory
│   ├── __init__.py           # Package initialization
│   ├── agent.py              # Agent implementation using Google ADK
│   └── spiritual_api.py      # Spiritual knowledge API implementation
├── __init__.py               # Root initialization file
├── setup.py                  # Package setup for installation
└── requirements.txt          # Project dependencies
```

The package is structured to work with the ADK API server, which requires the package to be installed in development mode.

## API Endpoints

The ADK API server provides a comprehensive set of endpoints for managing your MasterversAcharya agent. Below is a complete reference of all available endpoints.

### Application Management

#### List Applications
- **Endpoint**: `GET /list-apps`
- **Description**: Lists all available agent applications on the server
- **Example**:
  ```bash
  curl -X GET http://0.0.0.0:8000/list-apps
  ```

### Session Management

#### Create Session with Specific ID
- **Endpoint**: `POST /apps/{app_name}/users/{user_id}/sessions/{session_id}`
- **Description**: Creates a new session with a specified ID
- **Example**:
  ```bash
  curl -X POST http://0.0.0.0:8000/apps/masterversacharya/users/user123/sessions/session456 \
    -H "Content-Type: application/json" \
    -d '{"state": {}}'
  ```
- **Response**:
  ```json
  {
    "id": "session456",
    "app_name": "masterversacharya",
    "user_id": "user123",
    "state": {"state":{}},
    "events": [],
    "last_update_time": 1747402506.573765
  }
  ```

#### Create Session with Auto-generated ID
- **Endpoint**: `POST /apps/{app_name}/users/{user_id}/sessions`
- **Description**: Creates a new session with an automatically generated ID
- **Example**:
  ```bash
  curl -X POST http://0.0.0.0:8000/apps/masterversacharya/users/user123/sessions \
    -H "Content-Type: application/json" \
    -d '{"state": {}}'
  ```

#### Get Session Information
- **Endpoint**: `GET /apps/{app_name}/users/{user_id}/sessions/{session_id}`
- **Description**: Retrieves information about an existing session
- **Example**:
  ```bash
  curl -X GET http://0.0.0.0:8000/apps/masterversacharya/users/user123/sessions/session456 \
    -H "Content-Type: application/json"
  ```

#### List User Sessions
- **Endpoint**: `GET /apps/{app_name}/users/{user_id}/sessions`
- **Description**: Lists all sessions for a specific user
- **Example**:
  ```bash
  curl -X GET http://0.0.0.0:8000/apps/masterversacharya/users/user123/sessions \
    -H "Content-Type: application/json"
  ```

#### Delete Session
- **Endpoint**: `DELETE /apps/{app_name}/users/{user_id}/sessions/{session_id}`
- **Description**: Deletes a specific session
- **Example**:
  ```bash
  curl -X DELETE http://0.0.0.0:8000/apps/masterversacharya/users/user123/sessions/session456 \
    -H "Content-Type: application/json"
  ```

### Agent Interaction

#### Run Agent (Non-Streaming)
- **Endpoint**: `POST /run`
- **Description**: Sends a query to the agent and receives a complete response
- **Example**:
  ```bash
  curl -X POST http://0.0.0.0:8000/run \
    -H "Content-Type: application/json" \
    -d '{
      "app_name": "masterversacharya",
      "user_id": "user123",
      "session_id": "session456",
      "new_message": {
        "role": "user",
        "parts": [{
          "text": "What is the meaning of karma in Buddhism?"
        }]
      }
    }'
  ```

#### Run Agent (Streaming)
- **Endpoint**: `POST /run_sse`
- **Description**: Sends a query to the agent and receives a streaming response using Server-Sent Events
- **Example**:
  ```bash
  curl -X POST http://0.0.0.0:8000/run_sse \
    -H "Content-Type: application/json" \
    -d '{
      "app_name": "masterversacharya",
      "user_id": "user123",
      "session_id": "session456",
      "new_message": {
        "role": "user",
        "parts": [{
          "text": "Compare Buddhism and Hinduism views on meditation"
        }]
      },
      "streaming": true
    }'
  ```

#### Get Event Graph
- **Endpoint**: `GET /apps/{app_name}/users/{user_id}/sessions/{session_id}/events/{event_id}/graph`
- **Description**: Retrieves the execution graph for a specific event
- **Example**:
  ```bash
  curl -X GET http://0.0.0.0:8000/apps/masterversacharya/users/user123/sessions/session456/events/event789/graph \
    -H "Content-Type: application/json"
  ```

### Artifacts Management

#### List Artifacts
- **Endpoint**: `GET /apps/{app_name}/users/{user_id}/sessions/{session_id}/artifacts`
- **Description**: Lists all artifacts associated with a session
- **Example**:
  ```bash
  curl -X GET http://0.0.0.0:8000/apps/masterversacharya/users/user123/sessions/session456/artifacts \
    -H "Content-Type: application/json"
  ```

#### Load Artifact
- **Endpoint**: `GET /apps/{app_name}/users/{user_id}/sessions/{session_id}/artifacts/{artifact_name}`
- **Description**: Retrieves a specific artifact
- **Example**:
  ```bash
  curl -X GET http://0.0.0.0:8000/apps/masterversacharya/users/user123/sessions/session456/artifacts/meditation_guide \
    -H "Content-Type: application/json"
  ```

#### Delete Artifact
- **Endpoint**: `DELETE /apps/{app_name}/users/{user_id}/sessions/{session_id}/artifacts/{artifact_name}`
- **Description**: Deletes a specific artifact
- **Example**:
  ```bash
  curl -X DELETE http://0.0.0.0:8000/apps/masterversacharya/users/user123/sessions/session456/artifacts/meditation_guide \
    -H "Content-Type: application/json"
  ```

#### List Artifact Versions
- **Endpoint**: `GET /apps/{app_name}/users/{user_id}/sessions/{session_id}/artifacts/{artifact_name}/versions`
- **Description**: Lists all versions of a specific artifact
- **Example**:
  ```bash
  curl -X GET http://0.0.0.0:8000/apps/masterversacharya/users/user123/sessions/session456/artifacts/meditation_guide/versions \
    -H "Content-Type: application/json"
  ```

#### Load Artifact Version
- **Endpoint**: `GET /apps/{app_name}/users/{user_id}/sessions/{session_id}/artifacts/{artifact_name}/versions/{version_id}`
- **Description**: Retrieves a specific version of an artifact
- **Example**:
  ```bash
  curl -X GET http://0.0.0.0:8000/apps/masterversacharya/users/user123/sessions/session456/artifacts/meditation_guide/versions/1 \
    -H "Content-Type: application/json"
  ```

### Evaluation

#### List Evaluation Sets
- **Endpoint**: `GET /apps/{app_name}/eval_sets`
- **Description**: Lists all evaluation sets for an application
- **Example**:
  ```bash
  curl -X GET http://0.0.0.0:8000/apps/masterversacharya/eval_sets \
    -H "Content-Type: application/json"
  ```

#### Create Evaluation Set
- **Endpoint**: `POST /apps/{app_name}/eval_sets/{eval_set_id}`
- **Description**: Creates a new evaluation set
- **Example**:
  ```bash
  curl -X POST http://0.0.0.0:8000/apps/masterversacharya/eval_sets/spiritual_guidance_eval \
    -H "Content-Type: application/json" \
    -d '{"description": "Evaluation set for spiritual guidance responses"}'
  ```

#### Add Session to Evaluation Set
- **Endpoint**: `POST /apps/{app_name}/eval_sets/{eval_set_id}/add_session`
- **Description**: Adds a session to an evaluation set
- **Example**:
  ```bash
  curl -X POST http://0.0.0.0:8000/apps/masterversacharya/eval_sets/spiritual_guidance_eval/add_session \
    -H "Content-Type: application/json" \
    -d '{"user_id": "user123", "session_id": "session456"}'
  ```

#### List Evaluations in Set
- **Endpoint**: `GET /apps/{app_name}/eval_sets/{eval_set_id}/evals`
- **Description**: Lists all evaluations in an evaluation set
- **Example**:
  ```bash
  curl -X GET http://0.0.0.0:8000/apps/masterversacharya/eval_sets/spiritual_guidance_eval/evals \
    -H "Content-Type: application/json"
  ```

#### Run Evaluation
- **Endpoint**: `POST /apps/{app_name}/eval_sets/{eval_set_id}/run_eval`
- **Description**: Runs an evaluation on an evaluation set
- **Example**:
  ```bash
  curl -X POST http://0.0.0.0:8000/apps/masterversacharya/eval_sets/spiritual_guidance_eval/run_eval \
    -H "Content-Type: application/json" \
    -d '{"eval_name": "accuracy_test"}'
  ```

### Debugging

#### Get Trace Dictionary
- **Endpoint**: `GET /debug/trace/{event_id}`
- **Description**: Retrieves debugging trace information for a specific event
- **Example**:
  ```bash
  curl -X GET http://0.0.0.0:8000/debug/trace/event789 \
    -H "Content-Type: application/json"
  ```

## Example Queries

### Spiritual Practices

```bash
curl -X POST http://0.0.0.0:8000/run \
  -H "Content-Type: application/json" \
  -d '{
    "app_name": "masterversacharya",
    "user_id": "user123",
    "session_id": "session456",
    "new_message": {
      "role": "user",
      "parts": [{
        "text": "Can you recommend a meditation practice for beginners?"
      }]
    }
  }'
```

### Religious Comparisons

```bash
curl -X POST http://0.0.0.0:8000/run \
  -H "Content-Type: application/json" \
  -d '{
    "app_name": "masterversacharya",
    "user_id": "user123",
    "session_id": "session456",
    "new_message": {
      "role": "user",
      "parts": [{
        "text": "What are the key differences between Christian and Islamic prayer practices?"
      }]
    }
  }'
```

### Philosophical Inquiries

```bash
curl -X POST http://0.0.0.0:8000/run \
  -H "Content-Type: application/json" \
  -d '{
    "app_name": "masterversacharya",
    "user_id": "user123",
    "session_id": "session456",
    "new_message": {
      "role": "user",
      "parts": [{
        "text": "How do different philosophical traditions view the concept of self?"
      }]
    }
  }'
```

### Daily Spiritual Insights

```bash
curl -X POST http://0.0.0.0:8000/run \
  -H "Content-Type: application/json" \
  -d '{
    "app_name": "masterversacharya",
    "user_id": "user123",
    "session_id": "session456",
    "new_message": {
      "role": "user",
      "parts": [{
        "text": "Can you provide a daily spiritual insight or quote?"
      }]
    }
  }'
```

### Interfaith Dialogue

```bash
curl -X POST http://0.0.0.0:8000/run \
  -H "Content-Type: application/json" \
  -d '{
    "app_name": "masterversacharya",
    "user_id": "user123",
    "session_id": "session456",
    "new_message": {
      "role": "user",
      "parts": [{
        "text": "Generate an interfaith dialogue on the concept of compassion."
      }]
    }

```
### Integrations

ADK uses Callbacks to integrate with third-party observability tools. These integrations capture detailed traces of agent calls and interactions, which are crucial for understanding behavior, debugging issues, and evaluating performance.

### Observability

The ADK API server can be integrated with various observability tools:

- **Vertex AI Agent Builder**: Provides a managed platform for deploying and monitoring agents.
- **Comet Opik**: An open-source LLM observability and evaluation platform that natively supports ADK. It helps track and analyze agent interactions.

### Setting Up Integrations

To set up integrations with observability tools, you would typically configure callbacks in your agent implementation. Refer to the ADK documentation for specific integration instructions.

## Data Schemas

The ADK API server uses the following data schemas for requests and responses:

- **Session**: Contains session information including ID, app name, user ID, state, events, and last update time
- **Event**: Represents an interaction event in a session
- **Part**: Content part in a message (text, image, etc.)
- **AgentRunRequest**: Request format for running an agent query
- **GroundingSupport**: Information about grounding sources used in responses
- **Artifact**: Data objects generated or used by the agent
- **EvalMetric**: Metrics used for evaluating agent performance
- **ValidationError**: Error information for invalid requests

For a complete reference of all data schemas, you can access the OpenAPI documentation at:
```
http://0.0.0.0:8000/openapi.json
```

Or view the interactive API documentation at:
```
http://0.0.0.0:8000/docs
```

## Deployment

After testing your MasterversAcharya agent locally, you can deploy it to production environments using the following options:

### Agent Engine (Vertex AI)

The easiest way to deploy your ADK agents is to a managed service in Vertex AI on Google Cloud:

```bash
# Deployment command would be provided by Google Cloud documentation
```

### Cloud Run

For more control over scaling and management, you can deploy to Cloud Run using serverless architecture on Google Cloud:

```bash
adk deploy cloud_run masterversacharya
```

Refer to the Google Cloud documentation for detailed deployment instructions specific to your Google Cloud project setup.

### Prerequisites for Deployment

1. Google Cloud account with appropriate permissions
2. Google Cloud project with necessary APIs enabled
3. Google Cloud SDK installed and configured
4. Proper authentication setup

## Troubleshooting

### Common Issues and Solutions

#### Module Not Found Error

If you see an error like `No module named 'masterversacharya'` when using the `/run` or `/run_sse` endpoints, it means the API server cannot find the masterversacharya package.

**Solution**: Ensure you have installed the package in development mode:

```bash
# From the project root directory
pip install -e .
```

#### Session Not Found Error

If you see an error like `{"detail":"Session not found"}` when using the `/run` endpoint:

**Solution**: Create a new session first using the session creation endpoint:

```bash
curl -X POST http://0.0.0.0:8000/apps/masterversacharya/users/user123/sessions \
  -H "Content-Type: application/json" \
  -d '{"state": {}}'
```

Then use the returned session ID in your run request.

#### Internal Server Error

If you encounter an "Internal Server Error" when using any endpoint:

**Solution**: Check the server logs for more details. This is often due to missing dependencies or configuration issues.

#### API Key Not Set

If your agent interactions fail due to missing API keys:

**Solution**: Make sure you have set the `GOOGLE_API_KEY` environment variable or provided it in a .env file in the project root or masterversacharya directory.

```bash
# In .env file
GOOGLE_API_KEY=your_api_key_here
```

### Debugging Tips

1. Check the server logs for detailed error messages
2. Ensure all required dependencies are installed
3. Verify the package structure matches the expected format
4. Test with simple queries first before trying complex interactions
5. If modifying code, restart the API server to apply changes
