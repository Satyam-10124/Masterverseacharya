# MasterversAcharya API Tests

This document provides a comprehensive set of test API calls for the MasterversAcharya API. Use these commands to test each endpoint and verify your implementation.

## Prerequisites

Before running these tests:

1. Make sure the MasterversAcharya package is installed in development mode:
   ```bash
   pip install -e .
   ```

2. Start the ADK API server:
   ```bash
   adk api_server
   ```

3. Ensure you have the `GOOGLE_API_KEY` environment variable set or in a `.env` file.

## Test Commands

### 1. Application Management

#### List Applications
Test if you can retrieve the list of available applications:

```bash
curl -X GET http://0.0.0.0:8000/list-apps
```

Expected response:
```json
["masterversacharya"]
```

### 2. Session Management

#### Create a New Session with Auto-generated ID

```bash
curl -X POST http://0.0.0.0:8000/apps/masterversacharya/users/user123/sessions \
  -H "Content-Type: application/json" \
  -d '{"state": {}}'
```

Expected response (ID will vary):
```json
{
  "id": "8411db2d-a8ee-4b9b-a4b9-1052bc1e7810",
  "app_name": "masterversacharya",
  "user_id": "user123",
  "state": {"state":{}},
  "events": [],
  "last_update_time": 1747760092.170412
}
```

#### Create a New Session with Specific ID

```bash
curl -X POST http://0.0.0.0:8000/apps/masterversacharya/users/user123/sessions/test_session_id \
  -H "Content-Type: application/json" \
  -d '{"state": {}}'
```

Expected response:
```json
{
  "id": "test_session_id",
  "app_name": "masterversacharya",
  "user_id": "user123",
  "state": {"state":{}},
  "events": [],
  "last_update_time": 1747760092.170412
}
```

#### Get Session Information

```bash
# Replace SESSION_ID with the actual session ID from the create session response
curl -X GET http://0.0.0.0:8000/apps/masterversacharya/users/user123/sessions/SESSION_ID \
  -H "Content-Type: application/json"
```

#### List User Sessions

```bash
curl -X GET http://0.0.0.0:8000/apps/masterversacharya/users/user123/sessions \
  -H "Content-Type: application/json"
```

Expected response (will contain all active sessions):
```json
[
  {
    "id": "8411db2d-a8ee-4b9b-a4b9-1052bc1e7810",
    "app_name": "masterversacharya",
    "user_id": "user123",
    "state": {"state":{}},
    "events": [],
    "last_update_time": 1747760092.170412
  },
  {
    "id": "test_session_id",
    "app_name": "masterversacharya",
    "user_id": "user123",
    "state": {"state":{}},
    "events": [],
    "last_update_time": 1747760092.170412
  }
]
```

#### Delete Session

```bash
# Replace SESSION_ID with the actual session ID you want to delete
curl -X DELETE http://0.0.0.0:8000/apps/masterversacharya/users/user123/sessions/SESSION_ID \
  -H "Content-Type: application/json"
```

### 3. Agent Interaction

#### Run Agent (Non-Streaming)

```bash
# Replace SESSION_ID with a valid session ID
curl -X POST http://0.0.0.0:8000/run \
  -H "Content-Type: application/json" \
  -d '{
    "app_name": "masterversacharya",
    "user_id": "user123",
    "session_id": "SESSION_ID",
    "new_message": {
      "role": "user",
      "parts": [{
        "text": "What is the meaning of karma in Buddhism?"
      }]
    }
  }'
```

Expected response (truncated):
```json
[{"content":{"parts":[{"text":"...explanation of karma in Buddhism..."}],"role":"model"},"invocation_id":"...","author":"MasterversAcharya","actions":{"state_delta":{},"artifact_delta":{},"requested_auth_configs":{}},"id":"...","timestamp":...}]
```

#### Test Different Spiritual Questions

```bash
# Replace SESSION_ID with a valid session ID
curl -X POST http://0.0.0.0:8000/run \
  -H "Content-Type: application/json" \
  -d '{
    "app_name": "masterversacharya",
    "user_id": "user123",
    "session_id": "SESSION_ID",
    "new_message": {
      "role": "user",
      "parts": [{
        "text": "Compare Buddhism and Hinduism views on meditation"
      }]
    }
  }'
```

#### Run Agent (Streaming)

```bash
# Replace SESSION_ID with a valid session ID
curl -X POST http://0.0.0.0:8000/run_sse \
  -H "Content-Type: application/json" \
  -d '{
    "app_name": "masterversacharya",
    "user_id": "user123",
    "session_id": "SESSION_ID",
    "new_message": {
      "role": "user",
      "parts": [{
        "text": "What are the core beliefs of Christianity?"
      }]
    },
    "streaming": true
  }'
```

#### Using Agent Functions

Test specific agent functions by asking targeted questions:

1. Religious Information:
```bash
# Replace SESSION_ID with a valid session ID
curl -X POST http://0.0.0.0:8000/run \
  -H "Content-Type: application/json" \
  -d '{
    "app_name": "masterversacharya",
    "user_id": "user123",
    "session_id": "SESSION_ID",
    "new_message": {
      "role": "user",
      "parts": [{
        "text": "What are the key practices in Islam?"
      }]
    }
  }'
```

2. Philosophical Perspective:
```bash
# Replace SESSION_ID with a valid session ID
curl -X POST http://0.0.0.0:8000/run \
  -H "Content-Type: application/json" \
  -d '{
    "app_name": "masterversacharya",
    "user_id": "user123",
    "session_id": "SESSION_ID",
    "new_message": {
      "role": "user",
      "parts": [{
        "text": "Explain stoicism philosophy and its view on suffering"
      }]
    }
  }'
```

3. Compare Religions:
```bash
# Replace SESSION_ID with a valid session ID
curl -X POST http://0.0.0.0:8000/run \
  -H "Content-Type: application/json" \
  -d '{
    "app_name": "masterversacharya",
    "user_id": "user123",
    "session_id": "SESSION_ID",
    "new_message": {
      "role": "user",
      "parts": [{
        "text": "Compare Christianity and Judaism on their views of afterlife"
      }]
    }
  }'
```

4. Daily Spiritual Insight:
```bash
# Replace SESSION_ID with a valid session ID
curl -X POST http://0.0.0.0:8000/run \
  -H "Content-Type: application/json" \
  -d '{
    "app_name": "masterversacharya",
    "user_id": "user123",
    "session_id": "SESSION_ID",
    "new_message": {
      "role": "user",
      "parts": [{
        "text": "Give me a daily spiritual insight about peace"
      }]
    }
  }'
```

5. Meditation Guide:
```bash
# Replace SESSION_ID with a valid session ID
curl -X POST http://0.0.0.0:8000/run \
  -H "Content-Type: application/json" \
  -d '{
    "app_name": "masterversacharya",
    "user_id": "user123",
    "session_id": "SESSION_ID",
    "new_message": {
      "role": "user",
      "parts": [{
        "text": "Create a 5-minute Buddhist meditation guide focused on compassion"
      }]
    }
  }'
```

### 4. Artifacts Management

#### Create an Artifact through the Agent

First, send a request that will generate an artifact:

```bash
# Replace SESSION_ID with a valid session ID
curl -X POST http://0.0.0.0:8000/run \
  -H "Content-Type: application/json" \
  -d '{
    "app_name": "masterversacharya",
    "user_id": "user123",
    "session_id": "SESSION_ID",
    "new_message": {
      "role": "user",
      "parts": [{
        "text": "Create a meditation guide for mindfulness and save it as an artifact"
      }]
    }
  }'
```

#### List Artifacts

```bash
# Replace SESSION_ID with a valid session ID
curl -X GET http://0.0.0.0:8000/apps/masterversacharya/users/user123/sessions/SESSION_ID/artifacts \
  -H "Content-Type: application/json"
```

#### Load Specific Artifact

```bash
# Replace SESSION_ID and ARTIFACT_NAME with valid values
curl -X GET http://0.0.0.0:8000/apps/masterversacharya/users/user123/sessions/SESSION_ID/artifacts/ARTIFACT_NAME \
  -H "Content-Type: application/json"
```

#### Delete Artifact

```bash
# Replace SESSION_ID and ARTIFACT_NAME with valid values
curl -X DELETE http://0.0.0.0:8000/apps/masterversacharya/users/user123/sessions/SESSION_ID/artifacts/ARTIFACT_NAME \
  -H "Content-Type: application/json"
```

## Automated Test Script

You can create a basic shell script to automate some of these tests. Here's an example:

```bash
#!/bin/bash

# API Testing Script for MasterversAcharya

# Base URL
BASE_URL="http://0.0.0.0:8000"

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo "Starting MasterversAcharya API Tests..."

# Test 1: List Applications
echo -e "\n${GREEN}Test 1: List Applications${NC}"
curl -s -X GET $BASE_URL/list-apps

# Test 2: Create a new session
echo -e "\n\n${GREEN}Test 2: Create Session${NC}"
SESSION_RESPONSE=$(curl -s -X POST "$BASE_URL/apps/masterversacharya/users/user123/sessions" \
  -H "Content-Type: application/json" \
  -d '{"state": {}}')
echo $SESSION_RESPONSE

# Extract session ID using grep and cut
SESSION_ID=$(echo $SESSION_RESPONSE | grep -o '"id":"[^"]*' | cut -d'"' -f4)
echo -e "\nExtracted Session ID: $SESSION_ID"

# Test 3: List user sessions
echo -e "\n${GREEN}Test 3: List User Sessions${NC}"
curl -s -X GET "$BASE_URL/apps/masterversacharya/users/user123/sessions" \
  -H "Content-Type: application/json"

# Test 4: Run agent with a query
echo -e "\n\n${GREEN}Test 4: Run Agent Query${NC}"
curl -s -X POST "$BASE_URL/run" \
  -H "Content-Type: application/json" \
  -d '{
    "app_name": "masterversacharya",
    "user_id": "user123",
    "session_id": "'$SESSION_ID'",
    "new_message": {
      "role": "user",
      "parts": [{
        "text": "What is the meaning of karma in Buddhism?"
      }]
    }
  }'

echo -e "\n\nAPI tests completed!"
```

Save this as `test_api.sh` in your project directory and run with:

```bash
chmod +x test_api.sh
./test_api.sh
```

## Troubleshooting

If any of these tests fail, refer to the [Troubleshooting section](API.md#troubleshooting) in the main API documentation.

Common issues include:
- Package not installed properly
- API server not running
- Invalid session IDs
- Missing API keys
- Incorrect JSON formatting in requests

## Next Steps

After testing these endpoints, you can:
1. Build a client application that interacts with the API
2. Create a web interface using the streaming endpoint for real-time responses
3. Implement custom agents with additional spiritual tools
4. Deploy your solution to a production environment
