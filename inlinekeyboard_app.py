#!/usr/bin/env python
# pylint: disable=unused-argument, wrong-import-position
# This program is dedicated to the public domain under the CC0 license.

"""
Basic example for a bot that uses inline keyboards. For an in-depth explanation, check out
 https://github.com/python-telegram-bot/python-telegram-bot/wiki/InlineKeyboard-Example.
"""
import logging
from secret_telegram import TELEGRAM_TOKEN
from secret_account import allow_groups
t_token = TELEGRAM_TOKEN
from telegram import __version__ as TG_VER

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes

from query_tools import *

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

def domain_rank_reply_converter(domain_rank):
    result = ""
    for domain in domain_rank :
        result = result              + \
            '👉 <b>Domain Name :</b>'+ \
            domain['key']            + \
            '\n'                     + \
            '        <b>Count : </b>'+ \
            str(domain['doc_count']) + \
            '\n'
    return result

serverId = ""
rank = ""

def Flush_data():
    global serverId
    global rank
    serverId = ""
    rank = ""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message.chat.id not in allow_groups :
        print(f"Group {update.message.chat.id} not allow !")
        return
    """Sends a message with three inline buttons attached."""
    keyboard = [
        [
            InlineKeyboardButton("wking", callback_data="wking"),
            InlineKeyboardButton("Developing...", callback_data="Nan"),
        ],
        [
            InlineKeyboardButton("Done", callback_data="-1"),   
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Please choose Site:", reply_markup=reply_markup)

async def Button_Sites(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text."""
    global serverId
    global rank
    query = update.callback_query
    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    await query.answer()
    if query.data == "-1" :
        await query.edit_message_text(text="Bye~")

    keyboard_functions = [
        [
            InlineKeyboardButton("rank5", callback_data="rank5"),
            InlineKeyboardButton("rank10", callback_data="rank10"),
            InlineKeyboardButton("usercount", callback_data="usercount"),
        ],
        [
            InlineKeyboardButton("Done", callback_data="-1"),   
        ]
    ]
    reply_markup_functions = InlineKeyboardMarkup(keyboard_functions)

    keyboard_hours = [
        [
            InlineKeyboardButton("1 HR", callback_data="1 "),
            InlineKeyboardButton("3 HR", callback_data="3"),
            InlineKeyboardButton("6 HR", callback_data="6"),
        ],
        [
            InlineKeyboardButton("9 HR", callback_data="9"),
            InlineKeyboardButton("12 HR", callback_data="12"),
            InlineKeyboardButton("15 HR", callback_data="15"),
        ],
        [
            InlineKeyboardButton("18 HR", callback_data="18"),
            InlineKeyboardButton("21 HR", callback_data="21"),
            InlineKeyboardButton("24 HR", callback_data="24"),
        ],
        [
            InlineKeyboardButton("Done", callback_data="-1"),   
        ]
    ]
    reply_markup_hours = InlineKeyboardMarkup(keyboard_hours)
    if query.data == "wking" :
        serverId = "9"
        await query.edit_message_text(text="Selected function: ", reply_markup=reply_markup_functions)
    elif query.data == "rank5" or query.data == "rank10" :
        rank = query.data
        await query.edit_message_text(text=f"Selected time range: ", reply_markup=reply_markup_hours)
    elif query.data == "usercount" :
        count = Get_Wking_UserCount()
        reply = '<b>🌏 Wking Online Users Now : </b>'
        reply = reply + '<code>' + count + '</code>'
        await query.edit_message_text(text=reply, parse_mode='HTML')
    elif isinstance(int(query.data), int) :
        if rank == "rank5" :
            domain_rank = Get_Domain_Rank(serverId=serverId, size=5, range=int(query.data))
            reply = f"<b>💵 Wking Top</b> <code>5</code> <b>Domains Been Accessed During {query.data} HR </b>\n"
            domain_rank_converted = domain_rank_reply_converter(domain_rank)
            reply = reply + domain_rank_converted
            await query.edit_message_text(text=reply, parse_mode='HTML')
            Flush_data()
        elif rank == "rank10" :
            domain_rank = Get_Domain_Rank(serverId=serverId, size=10, range=int(query.data))
            reply = f"<b>💵 Wking Top</b> <code>10</code> <b>Domains Been Accessed During {query.data} HR </b>\n"
            domain_rank_converted = domain_rank_reply_converter(domain_rank)
            reply = reply + domain_rank_converted
            await query.edit_message_text(text=reply, parse_mode='HTML')
            Flush_data()

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    # await query.answer()
    # await query.edit_message_text(text=f"Selected serverId: {query.data}", reply_markup=reply_markup_functions)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Displays info on how to use the bot."""
    await update.message.reply_text("Use /status to test this bot.")

def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(t_token).build()

    application.add_handler(CommandHandler("status", start))
    application.add_handler(CallbackQueryHandler(Button_Sites))
    application.add_handler(CommandHandler("help", help_command))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()