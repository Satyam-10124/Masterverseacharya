#!/bin/bash

# API Testing Script for MasterversAcharya

# Base URL
BASE_URL="http://0.0.0.0:8000"

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}===============================================${NC}"
echo -e "${BLUE}    MasterversAcharya API Testing Script      ${NC}"
echo -e "${BLUE}===============================================${NC}"

# Check if API server is running
echo -e "\n${YELLOW}Checking if API server is running...${NC}"
if curl -s -f -o /dev/null "$BASE_URL/list-apps"; then
    echo -e "${GREEN}✓ API server is running!${NC}"
else
    echo -e "${RED}✗ API server not running! Please start with 'adk api_server'${NC}"
    exit 1
fi

# Test 1: List Applications
echo -e "\n${YELLOW}Test 1: List Applications${NC}"
APPS_RESPONSE=$(curl -s -X GET $BASE_URL/list-apps)
echo -e "Response: $APPS_RESPONSE"
if [ "$APPS_RESPONSE" != "[]" ] && [ "$APPS_RESPONSE" != "" ]; then
    echo -e "${GREEN}✓ Successfully listed applications${NC}"
else
    echo -e "${RED}✗ Failed to list applications${NC}"
fi

# Test 2: Create a new session
echo -e "\n${YELLOW}Test 2: Create Session${NC}"
SESSION_RESPONSE=$(curl -s -X POST "$BASE_URL/apps/masterversacharya/users/user123/sessions" \
  -H "Content-Type: application/json" \
  -d '{"state": {}}')
echo -e "Response: $SESSION_RESPONSE"

# Extract session ID
SESSION_ID=$(echo $SESSION_RESPONSE | grep -o '"id":"[^"]*' | cut -d'"' -f4)

if [ -z "$SESSION_ID" ]; then
    echo -e "${RED}✗ Failed to create session or extract session ID${NC}"
    # Create a fallback session with specific ID for testing
    echo -e "${YELLOW}Creating session with fallback ID...${NC}"
    curl -s -X POST "$BASE_URL/apps/masterversacharya/users/user123/sessions/test_fallback_session" \
      -H "Content-Type: application/json" \
      -d '{"state": {}}'
    SESSION_ID="test_fallback_session"
else
    echo -e "${GREEN}✓ Successfully created session${NC}"
    echo -e "   Session ID: $SESSION_ID"
fi

# Test 3: List user sessions
echo -e "\n${YELLOW}Test 3: List User Sessions${NC}"
SESSIONS_RESPONSE=$(curl -s -X GET "$BASE_URL/apps/masterversacharya/users/user123/sessions" \
  -H "Content-Type: application/json")
echo -e "Response: $SESSIONS_RESPONSE"

if [[ $SESSIONS_RESPONSE == *"$SESSION_ID"* ]]; then
    echo -e "${GREEN}✓ Successfully listed sessions and found our session${NC}"
else
    echo -e "${RED}✗ Failed to find our session in the list${NC}"
fi

# Test 4: Get session information
echo -e "\n${YELLOW}Test 4: Get Session Information${NC}"
SESSION_INFO=$(curl -s -X GET "$BASE_URL/apps/masterversacharya/users/user123/sessions/$SESSION_ID" \
  -H "Content-Type: application/json")
echo -e "Response: $SESSION_INFO"

if [[ $SESSION_INFO == *"$SESSION_ID"* ]]; then
    echo -e "${GREEN}✓ Successfully retrieved session information${NC}"
else
    echo -e "${RED}✗ Failed to retrieve session information${NC}"
fi

# Test 5: Run agent with a query about Buddhism
echo -e "\n${YELLOW}Test 5: Run Agent Query - Buddhism${NC}"
echo -e "${BLUE}Querying: What is the meaning of karma in Buddhism?${NC}"
QUERY_RESPONSE=$(curl -s -X POST "$BASE_URL/run" \
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
  }')

echo -e "Response received. Length: ${#QUERY_RESPONSE} characters"
# Show a truncated version if successful
if [[ $QUERY_RESPONSE == *"model"* ]] && [[ $QUERY_RESPONSE != *"error"* ]]; then
    echo -e "${GREEN}✓ Successfully queried about karma in Buddhism${NC}"
    echo -e "${BLUE}Truncated response:${NC} ${QUERY_RESPONSE:0:200}..."
else
    echo -e "${RED}✗ Failed to get response for Buddhism query${NC}"
    echo "Full response: $QUERY_RESPONSE"
fi

# Test 6: Run agent with a query about meditation
echo -e "\n${YELLOW}Test 6: Run Agent Query - Meditation Guide${NC}"
echo -e "${BLUE}Querying: Create a 2-minute mindfulness meditation guide${NC}"
MEDITATION_RESPONSE=$(curl -s -X POST "$BASE_URL/run" \
  -H "Content-Type: application/json" \
  -d '{
    "app_name": "masterversacharya",
    "user_id": "user123",
    "session_id": "'$SESSION_ID'",
    "new_message": {
      "role": "user",
      "parts": [{
        "text": "Create a 2-minute mindfulness meditation guide"
      }]
    }
  }')

echo -e "Response received. Length: ${#MEDITATION_RESPONSE} characters"
if [[ $MEDITATION_RESPONSE == *"model"* ]] && [[ $MEDITATION_RESPONSE != *"error"* ]]; then
    echo -e "${GREEN}✓ Successfully created meditation guide${NC}"
    echo -e "${BLUE}Truncated response:${NC} ${MEDITATION_RESPONSE:0:200}..."
else
    echo -e "${RED}✗ Failed to get meditation guide response${NC}"
    echo "Full response: $MEDITATION_RESPONSE"
fi

# Test 7: List artifacts
echo -e "\n${YELLOW}Test 7: List Artifacts${NC}"
ARTIFACTS_RESPONSE=$(curl -s -X GET "$BASE_URL/apps/masterversacharya/users/user123/sessions/$SESSION_ID/artifacts" \
  -H "Content-Type: application/json")
echo -e "Response: $ARTIFACTS_RESPONSE"

if [[ $ARTIFACTS_RESPONSE == "[]" ]] || [[ $ARTIFACTS_RESPONSE == *"artifact"* ]]; then
    echo -e "${GREEN}✓ Successfully listed artifacts${NC}"
else
    echo -e "${RED}✗ Failed to list artifacts${NC}"
fi

# Test 8: Delete session (cleanup)
echo -e "\n${YELLOW}Test 8: Delete Session (Cleanup)${NC}"
DELETE_RESPONSE=$(curl -s -X DELETE "$BASE_URL/apps/masterversacharya/users/user123/sessions/$SESSION_ID" \
  -H "Content-Type: application/json")
echo -e "Response: $DELETE_RESPONSE"

# Test if we can still retrieve the deleted session
CHECK_DELETED=$(curl -s -X GET "$BASE_URL/apps/masterversacharya/users/user123/sessions/$SESSION_ID" \
  -H "Content-Type: application/json")

if [[ $CHECK_DELETED == *"not found"* ]] || [[ $CHECK_DELETED == *"error"* ]]; then
    echo -e "${GREEN}✓ Successfully deleted session${NC}"
else
    echo -e "${RED}✗ Failed to delete session${NC}"
fi

echo -e "\n${BLUE}===============================================${NC}"
echo -e "${GREEN}All API tests completed!${NC}"
echo -e "${BLUE}===============================================${NC}"

echo -e "\n${YELLOW}For detailed information and more tests, refer to:${NC}"
echo -e "- docs/API.md - Main API documentation"
echo -e "- docs/API_TESTS.md - Comprehensive test guide"
