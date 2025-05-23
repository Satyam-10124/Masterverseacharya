#!/usr/bin/env python3
import os
import json
import logging
import requests
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Telegram Bot Token (loaded from environment variable)
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")

# MasterversAcharya API Configuration (loaded from environment variable or default)
BASE_URL = os.environ.get("MASTERVERSACHARYA_API_BASE_URL", "http://127.0.0.1:9876")

# Check if TELEGRAM_TOKEN is set
if not TELEGRAM_TOKEN:
    logger.error("TELEGRAM_TOKEN not found. Please set it in your .env file or environment variables.")
    exit(1)
APP_NAME = "masterversacharya"

# Configure request retry settings
requests.adapters.DEFAULT_RETRIES = 2  # Set default retries for requests

# User session mapping (in-memory storage)
user_sessions = {}

# Start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a welcome message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        f"🙏 Welcome to MasterversAcharya Bot, {user.mention_html()}!\n\n"
        f"I can help you learn about Buddhism, meditation, and more. "
        f"Use /newsession to start a new conversation or simply ask me a question."
    )

# Help command handler
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    help_text = (
        "🧘 *MasterversAcharya Bot Commands:*\n\n"
        "/start - Welcome message\n"
        "/help - Show this help message\n"
        "/newsession - Create a new conversation session\n"
        "/listsessions - List your active sessions\n"
        "/deletesession - Delete your current session\n\n"
        "Simply type a message to ask about Buddhism, meditation, or request a meditation guide!"
    )
    await update.message.reply_markdown(help_text)

# Create a new session
async def new_session(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Create a new API session for the user."""
    user_id = str(update.effective_user.id)
    telegram_username = update.effective_user.username or f"user{user_id}"
    
    try:
        # Create a new session via API
        response = requests.post(
            f"{BASE_URL}/apps/{APP_NAME}/users/{telegram_username}/sessions",
            json={"state": {}},
            timeout=10  # Add timeout of 10 seconds
        )
        
        if response.status_code == 200:
            session_data = response.json()
            session_id = session_data.get("id")
            
            # Store session info
            user_sessions[user_id] = {
                "session_id": session_id,
                "telegram_username": telegram_username
            }
            
            await update.message.reply_text(
                f"✅ New session created successfully!\nSession ID: `{session_id}`\n\n"
                f"You can now ask me anything about Buddhism or meditation.",
                parse_mode="Markdown"
            )
        else:
            await update.message.reply_text(
                f"❌ Failed to create session. Error: {response.text}"
            )
    except Exception as e:
        logger.error(f"Error creating session: {e}")
        await update.message.reply_text(
            "⚠️ Something went wrong while creating your session. Please try again later."
        )

# List user sessions
async def list_sessions(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """List all sessions for the user."""
    user_id = str(update.effective_user.id)
    telegram_username = update.effective_user.username or f"user{user_id}"
    
    try:
        # Get sessions from API
        response = requests.get(
            f"{BASE_URL}/apps/{APP_NAME}/users/{telegram_username}/sessions",
            timeout=10  # Add timeout of 10 seconds
        )
        
        if response.status_code == 200:
            sessions = response.json()
            
            if not sessions:
                await update.message.reply_text(
                    "You don't have any active sessions. Use /newsession to create one."
                )
                return
                
            # Create keyboard with session options
            keyboard = []
            for session in sessions:
                session_id = session.get("id")
                created_at = session.get("created_at", "Unknown date")
                # Truncate session ID for display
                display_id = session_id[:8] + "..." if len(session_id) > 10 else session_id
                keyboard.append([
                    InlineKeyboardButton(f"Session {display_id} ({created_at})", callback_data=f"select_session:{session_id}")
                ])
            
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_text(
                "🔍 Your active sessions:\nClick to select one:",
                reply_markup=reply_markup
            )
        else:
            await update.message.reply_text(
                f"❌ Failed to retrieve sessions. Error: {response.text}"
            )
    except Exception as e:
        logger.error(f"Error listing sessions: {e}")
        await update.message.reply_text(
            "⚠️ Something went wrong while retrieving your sessions. Please try again later."
        )

# Handle session selection
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Process button callbacks."""
    query = update.callback_query
    await query.answer()
    
    # Get the callback data
    data = query.data
    user_id = str(update.effective_user.id)
    telegram_username = update.effective_user.username or f"user{user_id}"
    
    if data.startswith("select_session:"):
        session_id = data.split(":")[1]
        
        # Update the user's current session
        user_sessions[user_id] = {
            "session_id": session_id,
            "telegram_username": telegram_username
        }
        
        await query.edit_message_text(
            f"✅ Selected session: `{session_id}`\n\nYou can now continue your conversation.",
            parse_mode="Markdown"
        )
    elif data == "confirm_delete":
        if user_id in user_sessions:
            session_id = user_sessions[user_id]["session_id"]
            
            # Delete the session via API
            try:
                response = requests.delete(
                    f"{BASE_URL}/apps/{APP_NAME}/users/{telegram_username}/sessions/{session_id}",
                    timeout=10  # Add timeout of 10 seconds
                )
                
                if response.status_code == 200:
                    # Remove from local storage
                    del user_sessions[user_id]
                    await query.edit_message_text("✅ Session deleted successfully!")
                else:
                    await query.edit_message_text(
                        f"❌ Failed to delete session. Error: {response.text}"
                    )
            except Exception as e:
                logger.error(f"Error deleting session: {e}")
                await query.edit_message_text(
                    "⚠️ Something went wrong while deleting your session."
                )
        else:
            await query.edit_message_text(
                "You don't have an active session to delete."
            )
    elif data == "cancel_delete":
        await query.edit_message_text("Session deletion cancelled.")

# Delete current session
async def delete_session(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Delete the user's current session."""
    user_id = str(update.effective_user.id)
    
    if user_id not in user_sessions:
        await update.message.reply_text(
            "You don't have an active session. Use /newsession to create one."
        )
        return
    
    session_id = user_sessions[user_id]["session_id"]
    
    # Confirm deletion with inline keyboard
    keyboard = [
        [
            InlineKeyboardButton("✅ Yes, delete it", callback_data="confirm_delete"),
            InlineKeyboardButton("❌ No, keep it", callback_data="cancel_delete"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        f"Are you sure you want to delete your current session?\nSession ID: `{session_id}`",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

# Handle user messages and queries
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Process user messages and send them to the MasterversAcharya API."""
    user_id = str(update.effective_user.id)
    telegram_username = update.effective_user.username or f"user{user_id}"
    user_message = update.message.text
    
    # Check if user has an active session
    if user_id not in user_sessions:
        # Create a new session automatically
        try:
            response = requests.post(
                f"{BASE_URL}/apps/{APP_NAME}/users/{telegram_username}/sessions",
                json={"state": {}}
            )
            
            if response.status_code == 200:
                session_data = response.json()
                session_id = session_data.get("id")
                
                user_sessions[user_id] = {
                    "session_id": session_id,
                    "telegram_username": telegram_username
                }
                
                await update.message.reply_text(
                    f"✨ I've created a new session for you automatically.\nSession ID: `{session_id}`",
                    parse_mode="Markdown"
                )
            else:
                await update.message.reply_text(
                    f"❌ Failed to create a session. Please use /newsession to create one manually."
                )
                return
        except Exception as e:
            logger.error(f"Error creating automatic session: {e}")
            await update.message.reply_text(
                "⚠️ Something went wrong. Please use /newsession to create a session manually."
            )
            return
    
    # Get the session ID
    session_id = user_sessions[user_id]["session_id"]
    
    # Show typing indicator
    await context.bot.send_chat_action(chat_id=update.message.chat_id, action="typing")
    
    # Send message to API
    try:
        api_request = {
            "app_name": APP_NAME,
            "user_id": telegram_username,
            "session_id": session_id,
            "new_message": {
                "role": "user",
                "parts": [{
                    "text": user_message
                }]
            }
        }
        
        response = requests.post(
            f"{BASE_URL}/run",
            json=api_request,
            timeout=15  # Add timeout of 15 seconds for API calls
        )
        
        if response.status_code == 200:
            api_response = response.json()
            
            # Log the API response for debugging
            logger.info(f"API Response received: {api_response}")
            
            # Extract the model's response text
            model_response = ""
            
            # Parse the correct response format from the ADK API logs
            # Format: {"candidates":[{"content":{"parts":[{"text":"response text"}],"role":"model"},"finish_reason":"STOP",...
            if "candidates" in api_response and len(api_response["candidates"]) > 0:
                first_candidate = api_response["candidates"][0]
                if "content" in first_candidate and "parts" in first_candidate["content"]:
                    parts = first_candidate["content"]["parts"]
                    if parts and len(parts) > 0 and "text" in parts[0]:
                        model_response = parts[0]["text"]
            
            # Try other formats used in test_api.sh
            if not model_response and isinstance(api_response, list) and len(api_response) > 0:
                first_item = api_response[0]
                if 'content' in first_item and 'parts' in first_item['content']:
                    parts = first_item['content']['parts']
                    if parts and len(parts) > 0 and 'text' in parts[0]:
                        model_response = parts[0]['text']
            
            # Fallback to other possible formats
            if not model_response and "response" in api_response:
                response_obj = api_response["response"]
                if isinstance(response_obj, dict) and "parts" in response_obj:
                    parts = response_obj["parts"]
                    if parts and len(parts) > 0 and "text" in parts[0]:
                        model_response = parts[0]["text"]
                        
            # Try the data.messages format
            if not model_response and "data" in api_response and "messages" in api_response["data"]:
                messages = api_response["data"]["messages"]
                if messages and len(messages) > 0:
                    for message in reversed(messages):
                        if message.get("role") == "model":
                            parts = message.get("parts", [])
                            for part in parts:
                                if "text" in part:
                                    model_response += part["text"]
                            break
            
            if not model_response:
                model_response = "I received your message but couldn't generate a proper response."
            
            # Check if there are any artifacts we should inform the user about
            artifacts_response = requests.get(
                f"{BASE_URL}/apps/{APP_NAME}/users/{telegram_username}/sessions/{session_id}/artifacts",
                timeout=10  # Add timeout of 10 seconds
            )
            
            if artifacts_response.status_code == 200:
                artifacts = artifacts_response.json()
                if artifacts and len(artifacts) > 0:
                    model_response += "\n\n📎 *Note:* There are artifacts available in this session that can't be displayed in Telegram."
            
            # Send the response back to the user
            await update.message.reply_text(model_response, parse_mode="Markdown")
        else:
            await update.message.reply_text(
                f"❌ Failed to get a response. Error: {response.text}\n\nPlease try again or create a new session with /newsession"
            )
    except Exception as e:
        logger.error(f"Error processing message: {e}")
        await update.message.reply_text(
            "⚠️ Something went wrong while processing your message. Please try again later."
        )

# Check if API server is running
def check_api_server():
    try:
        response = requests.get(f"{BASE_URL}/list-apps", timeout=5)
        return response.status_code == 200
    except:
        return False

def main() -> None:
    """Start the bot."""
    # Check if API server is running
    if not check_api_server():
        logger.error(f"MasterversAcharya API server is not running at {BASE_URL}")
        print("⚠️ API server not running! Please start with 'adk api_server' before running this bot.")
        return
    
    # Create the Application
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("newsession", new_session))
    application.add_handler(CommandHandler("listsessions", list_sessions))
    application.add_handler(CommandHandler("deletesession", delete_session))
    
    # Add callback query handler for inline buttons
    application.add_handler(CallbackQueryHandler(button_callback))
    
    # Add message handler
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Run the bot until the user presses Ctrl-C
    print("🚀 MasterversAcharya Telegram Bot is running!")
    application.run_polling()

if __name__ == '__main__':
    main()