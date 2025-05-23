# MasterversAcharya Telegram Bot - Installation and Setup Guide

This guide will help you set up and run the MasterversAcharya Telegram Bot that connects to the MasterversAcharya API. The bot provides a user-friendly interface for interacting with the MasterversAcharya spiritual guidance agent through Telegram.

## Prerequisites

Before starting, make sure you have:

- Python 3.8 or higher installed
- The MasterversAcharya API server running (on `http://0.0.0.0:8000` by default)
- A Telegram account

## Step 1: Create a Telegram Bot

1. Open Telegram and search for `@BotFather`
2. Start a chat with BotFather and send the command `/newbot`
3. Follow the instructions to create your bot:
   - Choose a name for your bot (e.g., "MasterversAcharya Bot")
   - Choose a username for your bot (e.g., "masterversacharya_bot")
4. Once created, BotFather will provide you with a **token**. Save this token as you'll need it later.

## Step 2: Install Required Python Packages

Create a virtual environment and install the required packages:

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install required packages
pip install python-telegram-bot requests
```

## Step 3: Configure the Bot

The bot is configured using environment variables, typically managed in a `.env` file in the project root directory. Refer to the main `README.md` for instructions on creating and populating the `.env` file.

1.  **Telegram Bot Token**:
    Ensure your `TELEGRAM_BOT_TOKEN` (obtained from BotFather) is set in your `.env` file:
    ```
    TELEGRAM_BOT_TOKEN=your_actual_telegram_bot_token_here
    ```
    The `telegram_bot.py` script should be adapted to load this token from the environment.

2.  **API Server URL (Optional)**:
    The bot defaults to connecting to the API server at `http://127.0.0.1:8000`. If your API server (run with `adk api_server`) is on a different address or port, you can configure this by setting the `MASTERVERSACHARYA_API_BASE_URL` in your `.env` file:
    ```
    MASTERVERSACHARYA_API_BASE_URL=http://your_api_server_address:port
    ```
    The `telegram_bot.py` script should be adapted to use this environment variable if set, otherwise falling back to the default.

**Note:** For these configurations to take effect, the `telegram_bot.py` script needs to be modified to load these values from environment variables (e.g., using `os.getenv()` and the `python-dotenv` library). The current version in the repository may have these values hardcoded.

## Step 4: Run the Bot

1. Make sure the MasterversAcharya API server is running
2. Run the Telegram bot:

```bash
# Make sure the virtual environment is activated
python telegram_bot.py
```

You should see the message: "🚀 MasterversAcharya Telegram Bot is running!"

## Step 5: Start Using the Bot

1. Open Telegram and search for your bot using the username you created
2. Start a chat with your bot and send the `/start` command
3. The bot will welcome you and you can start using the available commands:

| Command | Description |
|---------|-------------|
| `/start` | Welcome message |
| `/help` | Show help message |
| `/newsession` | Create a new conversation session |
| `/listsessions` | List your active sessions with clickable options |
| `/deletesession` | Delete your current session (with confirmation) |

You can also simply send a message to ask about Buddhism, meditation, or request a meditation guide!

## Features and Capabilities

### Session Management

The bot provides comprehensive session management capabilities:

- **Automatic Session Creation**: When a user sends their first message, the bot automatically creates a new session
- **Manual Session Creation**: Users can explicitly create a new session using `/newsession`
- **Session Listing**: The `/listsessions` command displays all active sessions with an interactive interface
- **Session Selection**: Users can select a previous session from the list to continue a conversation
- **Session Deletion**: The `/deletesession` command provides a confirmation interface to safely delete sessions

### API Integration

The bot integrates seamlessly with the MasterversAcharya API:

- **Direct API Communication**: Connects to the MasterversAcharya API server to process user queries
- **Robust Response Handling**: Processes API responses to extract the appropriate content
- **Content Formatting**: Formats responses for optimal display in Telegram's interface
- **Artifact Notification**: Notifies users when additional artifacts are available but can't be displayed in Telegram

### User Experience

- **Typing Indicators**: Shows typing indicators while processing requests to let users know the bot is working
- **Friendly Welcome**: Provides a clear, welcoming introduction to new users
- **Help Guidance**: Detailed help command explaining all available features
- **Inline Button Interface**: Uses Telegram's inline buttons for an interactive experience
- **Error Handling**: Provides user-friendly error messages and recovery options

## Troubleshooting

- **Bot not responding**: Make sure the script is running and the token is correct
- **API connection errors**: Verify that the MasterversAcharya API server (started with `adk api_server`) is running and accessible. By default, the bot tries `http://127.0.0.1:8000`. If you've configured a custom URL via `MASTERVERSACHARYA_API_BASE_URL` in your `.env` file, ensure it's correct and the server is listening there.
- **Permission errors**: Ensure your bot has the necessary permissions (managed through BotFather)
- **Conflict errors**: If you see `telegram.error.Conflict` errors, ensure only one instance of the bot is running
- **Session handling issues**: If sessions aren't being created/managed correctly, check the API logs for detailed error information

## Extending the Bot

You can extend the bot by:

1. Adding new commands in the `main()` function
2. Creating new handler functions for additional features
3. Implementing more API endpoints from the MasterversAcharya API
4. Enhancing the response parsing to handle additional content types
5. Adding more interactive elements using Telegram's inline keyboard features
6. Implementing media handling for sending images, audio or documents
7. Adding scheduled reminders or daily wisdom using the built-in scheduler

## Security Considerations

- The current implementation stores session data in memory. For production use, consider using a database.
- Implement proper authentication and user verification for sensitive operations.
- Consider hosting the bot on a secure server with proper monitoring.
- Keep your bot token secure. Never commit it directly to version control. Use environment variables (e.g., via a `.env` file loaded by `python-dotenv`) as recommended for storing sensitive credentials like `TELEGRAM_BOT_TOKEN`.
- Consider implementing rate limiting to prevent abuse.
- For shared hosting, ensure your environment variables and configuration files have appropriate permissions.
- Regularly update dependencies to address potential security vulnerabilities.

## Technical Details

### API Payload Structure

The bot sends requests to the MasterversAcharya API with this structure:

```json
{
  "app_name": "masterversacharya",
  "user_id": "[telegram_username]",
  "session_id": "[session_id]",
  "new_message": {
    "role": "user",
    "parts": [{
      "text": "[user_message]"
    }]
  }
}
```

### Response Handling

The bot can handle various response formats, including:

```json
{
  "candidates": [{
    "content": {
      "parts": [{
        "text": "[response_text]"
      }],
      "role": "model"
    }
  }]
}
```

And other fallback formats for maximum compatibility.
