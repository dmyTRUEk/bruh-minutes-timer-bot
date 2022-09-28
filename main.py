# bruh minutes timer bot

from typing import Callable

from datetime import datetime
from random import randint, uniform as randfloat
import asyncio

from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

from secrets_ import BOT_TOKEN, ALLOWED_USERNAMES


__version__ = "2.1.1"


HELP_MESSAGE: str = ("""
/help - get some help

/all - ping all

/t <number> <message> - set timer for <nubmer> bruh.minutes, with repeating <message>

/summon @username - summoning jutsu

/shower @username - timer for shower

/eat @username - timer for foodage consumage
""")

NODEAL: str = "1-900-902-NODEAL"



NUMBER_OF_TIMERS_RUNNING: int = 0



async def command_help(update: Update, _: ContextTypes.DEFAULT_TYPE):
    print(f"{datetime.now()}: @{update.message.from_user.username}: /help")
    await update.message.reply_text(HELP_MESSAGE)



def generate_bruh_minutes_in_seconds():
    # FOR TESTING:
    #return randint(4, 7)
    # FOR PRODUCTION:
    return randint(60 * 4, 60 * 7)



def print_number_of_running_timers():
    if NUMBER_OF_TIMERS_RUNNING == 0:
        print("All timers finished.")
    else:
        timer_or_timers = "timer" if NUMBER_OF_TIMERS_RUNNING == 1 else "timers"
        print(f"Still {NUMBER_OF_TIMERS_RUNNING} {timer_or_timers} running.")



async def countdown(
        update: Update,
        *,
        number_of_messages: int,    # messages are printed every `delay` seconds
        get_message: Callable[[], str],
        delay: Callable[[], int | float] = generate_bruh_minutes_in_seconds,
        ):
    if update.message.from_user.username not in ALLOWED_USERNAMES:
        await update.message.reply_text(NODEAL)
        # TODO: print in log that unknown user detected?
        return

    global NUMBER_OF_TIMERS_RUNNING
    NUMBER_OF_TIMERS_RUNNING += 1
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
    print_number_of_running_timers()



async def command_t(update: Update, _: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.username not in ALLOWED_USERNAMES:
        await update.message.reply_text(NODEAL)
        # TODO: print in log that unknown user detected?
        return

    print(f"{datetime.now()}: @{update.message.from_user.username}: {update.message.text}")

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
    if update.message.from_user.username not in ALLOWED_USERNAMES:
        await update.message.reply_text(NODEAL)
        # TODO: print in log that unknown user detected?
        return

    print(f"{datetime.now()}: @{update.message.from_user.username}: {update.message.text}")

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
    if update.message.from_user.username not in ALLOWED_USERNAMES:
        await update.message.reply_text(NODEAL)
        # TODO: print in log that unknown user detected?
        return

    print(f"{datetime.now()}: @{update.message.from_user.username}: {update.message.text}")

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
    if update.message.from_user.username not in ALLOWED_USERNAMES:
        await update.message.reply_text(NODEAL)
        # TODO: print in log that unknown user detected?
        return

    print(f"{datetime.now()}: @{update.message.from_user.username}: {update.message.text}")

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
    if update.message.from_user.username not in ALLOWED_USERNAMES:
        await update.message.reply_text(NODEAL)
        # TODO: print in log that unknown user detected?
        return

    print(f"{datetime.now()}: @{update.message.from_user.username}: {update.message.text}")

    #usernames_in_chat: list[str] = []
    ##chat_id = update.effective_chat.id
    #for user in ALLOWED_USERS:
    #    try:
    #        # pylint: generated-members=update.effective_chat.get_member
    #        member = await update.effective_chat.get_member(user.userid)
    #    except:
    #        print(f"{user} -> NOT FOUND NOT FOUND NOT FOUND: not in chat or bad user_id?")
    #        continue
    #    usernames_in_chat.append(user.username)
    #    print(f"{user} -> {member.user.username}")

    #usernames_in_chat_with_at: list[str] = list(map(lambda username: '@'+username, usernames_in_chat))
    # usernames_in_chat_with_at: list[str] = ['@'+username for username in usernames_in_chat]

    # message: str = ' '.join(usernames_in_chat_with_at)

    await update.message.reply_text("/all is under maintenance, sorry :'(")
    # FOR PRODUCTION:
    #await update.message.reply_text(usernames_in_chat_with_at)



def main():
    print(f"{datetime.now()}: Started bot.")
    app = ApplicationBuilder().token(BOT_TOKEN).concurrent_updates(True).build()
    app.add_handler(CommandHandler("help",    command_help))
    app.add_handler(CommandHandler("all",     command_all))
    app.add_handler(CommandHandler("summon",  command_summon))
    app.add_handler(CommandHandler("t",       command_t))
    app.add_handler(CommandHandler("eat",     command_eat))
    app.add_handler(CommandHandler("shower",  command_shower))
    app.run_polling()



if __name__ == "__main__":
    main()

