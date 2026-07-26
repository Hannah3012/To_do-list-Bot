import logging
from telegram import Update
from telegram.ext import ContextTypes

from database import get_session
from models import Todo

logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Hi! I'm your todo list bot.\n\n"
        "Commands:\n"
        "/add <add task>— add a new todo\n"
        "/list — show all your todos\n"
        "/done <id> — mark a todo as complete\n"
        "/delete <id> — remove a todo\n"
        "/help — show this message again"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await start(update, context)

async def add_todo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = " ".join(context.args).strip()

    if not text:
        await update.message.reply_text(
            "Usage: /add <tasks description>"
        )
        return
    
    with get_session() as session:
        todo = Todo(user_id=user_id, text=text)
        session.add(todo)
        session.flush()
        todo_id = todo.id

    await update.message.reply_text(f"✅ Added todo.\n#{todo_id}: {text}")
