# bruh minutes timer bot

from typing import Callable

from datetime import datetime
from random import randint, uniform as randfloat
import asyncio

from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler


__version__ = "2.2.3"


HELP_MESSAGE: str = ("""
/help - get some help

/all - ping all

/t <number> <message> - set timer for <nubmer> bruh.minutes, with repeating <message>

/summon @username - summoning jutsu

/shower @username - timer for shower

/eat @username - timer for foodage consumage
""")

NODEAL: str = "1-900-902-NODEAL"



BOT_TOKEN: str

ALLOWED_USERNAMES: list[str]

CHAT_ID_TO_USERNAMES: dict[int, str]

NUMBER_OF_TIMERS_RUNNING: int = 0



def now() -> datetime:
    return datetime.now()


def generate_bruh_minutes_in_seconds():
    # FOR TESTING:
    #return randint(4, 7)
    # FOR PRODUCTION:
    return randint(60 * 4, 60 * 7)


def print_number_of_timers_running():
    print(f"Number of timers running: {NUMBER_OF_TIMERS_RUNNING}")



async def command_help(update: Update, _: ContextTypes.DEFAULT_TYPE):
    print(f"{now()}: @{update.message.from_user.username}: {update.message.text}")
    if update.message.from_user.username not in ALLOWED_USERNAMES:
        print(f"{now()}: @{update.message.from_user.username} -> unknown user, NODEAL")
        await update.message.reply_text(NODEAL)
        return

    await update.message.reply_text(HELP_MESSAGE)



async def countdown(
        update: Update,
        *,
        number_of_messages: int,    # messages are printed every `delay` seconds
        get_message: Callable[[], str],
        delay: Callable[[], int | float] = generate_bruh_minutes_in_seconds,
        ):
    if update.message.from_user.username not in ALLOWED_USERNAMES:
        print(f"{now()}: @{update.message.from_user.username} -> unknown user, NODEAL")
        await update.message.reply_text(NODEAL)
        return

    global NUMBER_OF_TIMERS_RUNNING
    NUMBER_OF_TIMERS_RUNNING += 1
    print_number_of_timers_running()
    for minutes_left in range(number_of_messages, 0, -1):
        bruh_minutes_left_text = "bruh.minutes left" if minutes_left > 1 else "bruh.minute left"
        message: str = get_message()
        status : str = f"\n\n{minutes_left} {bruh_minutes_left_text}" if (delay == generate_bruh_minutes_in_seconds) else ""
        message_full: str = f"{message}{status}"
        await update.message.reply_text(message_full)
        await asyncio.sleep(delay())

    if delay == generate_bruh_minutes_in_seconds:
        message: str = get_message()
        status : str = "\n\ntime is up, prepare for execution!"
        await update.message.reply_text(f"{message}{status}")

    NUMBER_OF_TIMERS_RUNNING -= 1
    print_number_of_timers_running()



async def command_t(update: Update, _: ContextTypes.DEFAULT_TYPE):
    print(f"{now()}: @{update.message.from_user.username}: {update.message.text}")

    if update.message.from_user.username not in ALLOWED_USERNAMES:
        print(f"{now()}: @{update.message.from_user.username} -> unknown user, NODEAL")
        await update.message.reply_text(NODEAL)
        return

    try:
        parts: list[str] = update.message.text.split(' ')
        number_of_bruh_minutes: int = int(parts[1])
        message_to_repeat: str = ' '.join(parts[2:])
    except:
        await update.message.reply_text("instructions misunderstood. pls /help to seek some help")
        return

    if number_of_bruh_minutes > 60:
        await update.message.reply_text("bruuuuuuh, im not getting paid enough")
        return

    await countdown(
        update,
        number_of_messages=number_of_bruh_minutes,
        get_message=lambda: message_to_repeat,
    )



async def command_summon(update: Update, _: ContextTypes.DEFAULT_TYPE):
    print(f"{now()}: @{update.message.from_user.username}: {update.message.text}")

    if update.message.from_user.username not in ALLOWED_USERNAMES:
        print(f"{now()}: @{update.message.from_user.username} -> unknown user, NODEAL")
        await update.message.reply_text(NODEAL)
        return

    try:
        parts: list[str] = update.message.text.split(' ')
        username: str = parts[1]
    except:
        await update.message.reply_text("instructions misunderstood. pls /help to seek some help")
        return

    def generate_message():
        message_to_repeat = "SUMMONING JUTSU\n"
        for _ in range(randint(1, 5) * randint(1, 5) * randint(1, 5)):
            message_to_repeat += username + ' ' * randint(1, 5)
        return message_to_repeat

    await countdown(
        update,
        number_of_messages = randint(5, 10),
        get_message = generate_message,
        delay = lambda: randfloat(0.5, 3),
    )



async def command_eat(update: Update, _: ContextTypes.DEFAULT_TYPE):
    print(f"{now()}: @{update.message.from_user.username}: {update.message.text}")

    if update.message.from_user.username not in ALLOWED_USERNAMES:
        print(f"{now()}: @{update.message.from_user.username} -> unknown user, NODEAL")
        await update.message.reply_text(NODEAL)
        return

    try:
        parts: list[str] = update.message.text.split(' ')
        username: str = parts[1]
    except:
        await update.message.reply_text("instructions misunderstood. pls /help to seek some help")
        return

    await countdown(
        update,
        number_of_messages = 6,
        get_message = lambda: f"Eat faster, {username}",
    )



async def command_shower(update: Update, _: ContextTypes.DEFAULT_TYPE):
    print(f"{now()}: @{update.message.from_user.username}: {update.message.text}")

    if update.message.from_user.username not in ALLOWED_USERNAMES:
        print(f"{now()}: @{update.message.from_user.username} -> unknown user, NODEAL")
        await update.message.reply_text(NODEAL)
        return

    try:
        parts: list[str] = update.message.text.split(' ')
        username: str = parts[1]
    except:
        await update.message.reply_text("instructions misunderstood. pls /help to seek some help")
        return

    await countdown(
        update,
        number_of_messages = 4,
        get_message = lambda: f"Dont drown, {username}",
    )



async def command_all(update: Update, _: ContextTypes.DEFAULT_TYPE):
    print(f"{now()}: @{update.message.from_user.username}: {update.message.text}")
    if update.message.from_user.username not in ALLOWED_USERNAMES:
        print(f"{now()}: @{update.message.from_user.username} -> unknown user, NODEAL")
        await update.message.reply_text(NODEAL)
        return

    chat_id: int = update.effective_chat.id # type: ignore
    usernames_in_chat: list[str] = CHAT_ID_TO_USERNAMES[chat_id].split(',')
    usernames_in_chat_with_at: list[str] = ['@'+username for username in usernames_in_chat]
    message: str = ' '.join(usernames_in_chat_with_at)
    await update.message.reply_text(message)



def init_global_vars():
    from os import environ as env
    global BOT_TOKEN, ALLOWED_USERNAMES, CHAT_ID_TO_USERNAMES
    if (bot_token_from_env := env.get("BOT_TOKEN", None)) != None:
        BOT_TOKEN = bot_token_from_env
    else:
        from secrets_ import BOT_TOKEN as bot_token_from_secrets
        BOT_TOKEN = bot_token_from_secrets

    if (chat_id_to_usernames := env.get("CHAT_ID_TO_USERNAMES", None)) != None:
        chats_to_commasep_users = chat_id_to_usernames.split(' ')
        CHAT_ID_TO_USERNAMES = {}
        for chat_to_commasep_users in chats_to_commasep_users:
            chat_id, commasep_users = chat_to_commasep_users.split(':')
            chat_id = int(chat_id)
            CHAT_ID_TO_USERNAMES[chat_id] = commasep_users
    else:
        #from secrets_ import ALLOWED_USERNAMES as allowed_usernames_from_secrets
        #ALLOWED_USERNAMES = allowed_usernames_from_secrets
        from secrets_ import CHAT_ID_TO_USERNAMES as chat_id_to_usernames
        CHAT_ID_TO_USERNAMES = chat_id_to_usernames

    ALLOWED_USERNAMES = []
    for key in CHAT_ID_TO_USERNAMES:
        value = CHAT_ID_TO_USERNAMES[key]
        users: list[str] = value.split(',')
        for user in users:
            if user not in ALLOWED_USERNAMES:
                ALLOWED_USERNAMES.append(user)
    print(f"{ALLOWED_USERNAMES = }")



def main():
    print(f"{now()}: Bruh Minutes Timer Bot v{__version__}.")
    print(f"{now()}: Initializing bot.")
    init_global_vars()
    app = ApplicationBuilder().token(BOT_TOKEN).concurrent_updates(True).build()
    app.add_handler(CommandHandler("help",    command_help))
    app.add_handler(CommandHandler("all",     command_all))
    app.add_handler(CommandHandler("summon",  command_summon))
    app.add_handler(CommandHandler("t",       command_t))
    app.add_handler(CommandHandler("eat",     command_eat))
    app.add_handler(CommandHandler("shower",  command_shower))
    print(f"{now()}: Starting bot polling.")
    app.run_polling()



if __name__ == "__main__":
    main()

