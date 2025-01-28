# Bot Development Guide

This guide covers advanced topics in bot development using the framework.

## Bot Architecture

### Base Bot Class

The `BotBase` class provides core functionality:

```python
class BotBase:
    def __init__(self):
        self.application = None
        self.state = {}
        self._status = 'starting'
        self._setup()
    
    def _setup(self):
        """Initialize bot application and load state."""
        self.application = Application.builder().token(
            os.getenv('BOT_TOKEN')
        ).build()
        self.state = self._load_state()
    
    async def start(self):
        """Initialize and start the bot."""
        raise NotImplementedError
    
    async def stop(self):
        """Clean up and stop the bot."""
        raise NotImplementedError
    
    def update_status(self, status, error=None, webhook_url=None):
        """Update bot status in Redis."""
        self._status = status
        # Update status in Redis
```

## Handler Types

1. **Command Handlers**:
```python
from telegram.ext import CommandHandler

async def cmd_help(self, update, context):
    await update.message.reply_text("Help message")

self.application.add_handler(
    CommandHandler("help", self.cmd_help)
)
```

2. **Message Handlers**:
```python
from telegram.ext import MessageHandler, filters

async def handle_text(self, update, context):
    await update.message.reply_text("Got your message!")

self.application.add_handler(
    MessageHandler(filters.TEXT, self.handle_text)
)
```

3. **Callback Query Handlers**:
```python
from telegram.ext import CallbackQueryHandler

async def button_press(self, update, context):
    await update.callback_query.answer()
    await update.callback_query.message.edit_text("Button pressed!")

self.application.add_handler(
    CallbackQueryHandler(self.button_press)
)
```

## Advanced Features

### Conversation Handlers

Manage multi-step interactions:

```python
from telegram.ext import ConversationHandler, CommandHandler, MessageHandler

FIRST, SECOND = range(2)

class RegistrationBot(BotBase):
    async def start_registration(self, update, context):
        await update.message.reply_text("What's your name?")
        return FIRST
    
    async def get_name(self, update, context):
        context.user_data['name'] = update.message.text
        await update.message.reply_text("What's your age?")
        return SECOND
    
    async def get_age(self, update, context):
        context.user_data['age'] = update.message.text
        await update.message.reply_text("Registration complete!")
        return ConversationHandler.END
    
    async def cancel(self, update, context):
        await update.message.reply_text("Registration cancelled.")
        return ConversationHandler.END
    
    async def start(self):
        conv_handler = ConversationHandler(
            entry_points=[CommandHandler('register', self.start_registration)],
            states={
                FIRST: [MessageHandler(filters.TEXT, self.get_name)],
                SECOND: [MessageHandler(filters.TEXT, self.get_age)]
            },
            fallbacks=[CommandHandler('cancel', self.cancel)]
        )
        self.application.add_handler(conv_handler)
```

### Inline Keyboards

Create interactive buttons:

```python
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

async def show_options(self, update, context):
    keyboard = [
        [
            InlineKeyboardButton("Option 1", callback_data='1'),
            InlineKeyboardButton("Option 2", callback_data='2')
        ],
        [InlineKeyboardButton("Help", callback_data='help')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        'Please choose:', 
        reply_markup=reply_markup
    )
```

### Job Queue

Schedule tasks:

```python
async def scheduled_task(self, context):
    """Run scheduled task."""
    chat_id = context.job.data['chat_id']
    await context.bot.send_message(
        chat_id=chat_id,
        text="Scheduled reminder!"
    )

async def start(self):
    """Set up scheduled tasks."""
    job_queue = self.application.job_queue
    
    # Run every hour
    job_queue.run_repeating(
        self.scheduled_task,
        interval=3600,
        first=0,
        data={'chat_id': ADMIN_CHAT_ID}
    )
    
    # Run once after 5 minutes
    job_queue.run_once(
        self.scheduled_task,
        when=300,
        data={'chat_id': ADMIN_CHAT_ID}
    )
```

## State Management

### Complex State Example

```python
class GameBot(BotBase):
    def __init__(self):
        super().__init__()
        self.state = {
            'players': {},
            'current_round': 0,
            'scores': {},
            'settings': {
                'max_rounds': 10,
                'time_limit': 60
            }
        }
    
    def add_player(self, user_id, username):
        """Add new player."""
        self.state['players'][user_id] = {
            'username': username,
            'joined_at': time.time(),
            'games_played': 0
        }
    
    def update_score(self, user_id, points):
        """Update player score."""
        if user_id not in self.state['scores']:
            self.state['scores'][user_id] = 0
        self.state['scores'][user_id] += points
```

## Error Handling

### Comprehensive Error Handling

```python
import logging
logger = logging.getLogger(__name__)

class RobustBot(BotBase):
    async def safe_operation(self, update, context):
        try:
            result = await self.risky_operation()
        except ConnectionError as e:
            logger.error("Connection failed", exc_info=True)
            self.update_status('error', str(e))
            await update.message.reply_text(
                "Sorry, connection failed. Please try again."
            )
        except ValueError as e:
            logger.warning("Invalid input", exc_info=True)
            await update.message.reply_text(
                "Invalid input. Please check and try again."
            )
        except Exception as e:
            logger.critical("Unexpected error", exc_info=True)
            self.update_status('error', str(e))
            await update.message.reply_text(
                "An unexpected error occurred."
            )
```

## Testing

### Unit Testing Example

```python
import pytest
from unittest.mock import AsyncMock, patch

@pytest.fixture
def bot():
    return MyBot()

@pytest.mark.asyncio
async def test_start_command(bot):
    update = AsyncMock()
    context = AsyncMock()
    
    await bot.cmd_start(update, context)
    
    update.message.reply_text.assert_called_once_with(
        "Welcome message"
    )

@pytest.mark.asyncio
async def test_state_management(bot):
    # Test state updates
    bot.state['counter'] = 0
    await bot.increment_counter(AsyncMock(), AsyncMock())
    assert bot.state['counter'] == 1
```

## Best Practices

1. **State Management**:
   - Keep state minimal and relevant
   - Use atomic operations
   - Regular state validation
   - Implement state recovery

2. **Error Handling**:
   - Catch specific exceptions
   - Log errors appropriately
   - Provide user-friendly messages
   - Update bot status on errors

3. **Resource Management**:
   - Clean up resources in stop()
   - Use context managers
   - Implement graceful shutdown
   - Monitor resource usage

4. **Security**:
   - Validate user input
   - Use rate limiting
   - Implement access control
   - Secure sensitive data

5. **Performance**:
   - Use async operations
   - Implement caching
   - Optimize database queries
   - Monitor memory usage