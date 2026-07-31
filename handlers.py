from aiogram import Router, types
from aiogram.filters import Command, CommandStart
from aiogram.filters import Command, CommandObject  # CORRECT
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from models import User, Todo
router = Router()

#ensures user profile exists in database
async def get_or_create_user(tg_id: int, full_name: str, session: AsyncSession) -> User:
    stmt = select(User).where(User.tg_id == tg_id)
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()
    
    if not user:
        user = User(tg_id=tg_id, full_name=full_name)
        session.add(user)
        await session.commit()
    return user

@router.message(CommandStart())
async def cmd_start(message: types.Message, db_session: AsyncSession):
    user = await get_or_create_user(message.from_user.id, message.from_user.full_name, db_session)
    await message.answer(
        f"Hello, {user.full_name}! Welcome.\n"
        "Use /help to see all available commands."
    )

@router.message(Command("help"))
async def cmd_help(message: types.Message):
    help_text = (
        "**Available To-Do List Commands:**\n\n"
        "/add <task> — Add a new task to your list\n"
        "/list — Display your active and completed tasks\n"
        "/done <task_number> — Mark a specific task as completed\n"
        "/delete <task_number> — Permanently remove a task\n"
        "/help — Display this help overview documentation"
    )
    await message.answer(help_text, parse_mode="Markdown")

@router.message(Command("add"))
async def cmd_add(message: types.Message, command: CommandObject, db_session: AsyncSession):
    if not command.args:
        return await message.answer("Please provide a task name. Example: `/add task1`", parse_mode="Markdown")
    
    await get_or_create_user(message.from_user.id, message.from_user.full_name, db_session)
    
    new_task = Todo(user_id=message.from_user.id, task=command.args)
    db_session.add(new_task)
    await db_session.commit()
    
    await message.answer(f"Added task: *{command.args}*", parse_mode="Markdown")

@router.message(Command("list"))
async def cmd_list(message: types.Message, db_session: AsyncSession):
    await get_or_create_user(message.from_user.id, message.from_user.full_name, db_session)
    
    stmt = select(Todo).where(Todo.user_id == message.from_user.id).order_by(Todo.id)
    result = await db_session.execute(stmt)
    todos = result.scalars().all()
    
    if not todos:
        return await message.answer("Your to-do list is empty! Use `/add` to build a new task.", parse_mode="Markdown")
    
    response = "**Your To-Do List:**\n\n"
    for index, item in enumerate(todos, start=1):
        status_icon = "✅" if item.is_done else "⏳"
        task_text = f"~{item.task}~" if item.is_done else item.task
        response += f"{index}. {status_icon} {task_text} *(ID: {index})*\n"
        
    await message.answer(response, parse_mode="Markdown")

@router.message(Command("done"))
async def cmd_done(message: types.Message, command: CommandObject, db_session: AsyncSession):
    if not command.args or not command.args.isdigit():
        return await message.answer("Please provide a valid task index number. Example: `/done 1`", parse_mode="Markdown")
    
    target_index = int(command.args)
    stmt = select(Todo).where(Todo.user_id == message.from_user.id).order_by(Todo.id)
    result = await db_session.execute(stmt)
    todos = result.scalars().all()
    
    if target_index < 1 or target_index > len(todos):
        return await message.answer("Invalid task index number. Use `/list` to check available tasks.")
    
    target_task = todos[target_index - 1]
    target_task.is_done = True
    await db_session.commit()
    
    await message.answer(f"✅ Marked task *{target_task.task}* as completed!", parse_mode="Markdown")

@router.message(Command("delete"))
async def cmd_delete(message: types.Message, command: CommandObject, db_session: AsyncSession):
    if not command.args or not command.args.isdigit():
        return await message.answer("Please provide a valid task index number. Example: `/delete 1`", parse_mode="Markdown")
    
    target_index = int(command.args)
    stmt = select(Todo).where(Todo.user_id == message.from_user.id).order_by(Todo.id)
    result = await db_session.execute(stmt)
    todos = result.scalars().all()
    
    if target_index < 1 or target_index > len(todos):
        return await message.answer("Invalid task index number. Use `/list` to check available tasks.")
    
    target_task = todos[target_index - 1]
    await db_session.delete(target_task)
    await db_session.commit()
    
    await message.answer(f"Deleted task: *{target_task.task}*", parse_mode="Markdown")

