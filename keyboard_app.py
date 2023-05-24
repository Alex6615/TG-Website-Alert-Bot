from secret_telegram import TELEGRAM_TOKEN
t_token = TELEGRAM_TOKEN
import logging
from typing import Dict

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
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

from query_tools import *

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

CHOOSING, TYPING_REPLY, ADVANCE_CHOICE = range(3)

# Sites
reply_keyboard = [
    ["wking"],
    ["Done"],
]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True)

# functions
functions_keyboard = [
    ["rank5", "rank10", "usercount"],
    ["Done"],
]
functions_markup = ReplyKeyboardMarkup(functions_keyboard, one_time_keyboard=True, resize_keyboard=True)

# time range
time_range_keyboard = [
    ["1 HR",  "6 HR",  "12 HR"],
    ["18 HR", "24 HR"],
    ["Done"],
]
time_range_markup = ReplyKeyboardMarkup(time_range_keyboard, one_time_keyboard=True, resize_keyboard=True)

def facts_to_str(user_data: Dict[str, str]) -> str:
    """Helper function for formatting the gathered user info."""
    facts = [f"{key} - {value}" for key, value in user_data.items()]
    return "\n".join(facts).join(["\n", "\n"])

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

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Start the conversation and ask user for input."""
    print(update.message.from_user.first_name)
    client = update.message.from_user.first_name
    await update.message.reply_text(
        f"✔️ {client} 請選擇一個站點",
        reply_markup=markup,
    )
    return CHOOSING

functions = []
async def functions_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    context.user_data["site"] = text
    client = update.message.from_user.first_name
    await update.message.reply_text(
        f"✔️ {client} 請選擇一個功能",
        reply_markup=functions_markup,
    )
    return TYPING_REPLY

async def received_information(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_data = context.user_data
    text = update.message.text
    client = update.message.from_user.first_name
    if text not in functions_keyboard[0] :
        await update.message.reply_text(
            f" {client} Function Error !",
            reply_markup=ReplyKeyboardRemove(),
        )
        return ConversationHandler.END
    context.user_data["function"] = text
    funs_need_to_advance = ['rank5', 'rank10']
    if user_data["function"] in funs_need_to_advance :
        await update.message.reply_text(
            f"✔️ {client} 請選擇時間區間",
            reply_markup=time_range_markup,
        )
        return ADVANCE_CHOICE
    else :
        if user_data['site'] == "wking" :
            count = Get_Wking_UserCount()
            reply = '<b>🌏 Wking Online Users Now : </b>'
            reply = reply + '<code>' + count + '</code>'
            await context.bot.send_message(chat_id=update.effective_chat.id, text=reply, parse_mode='HTML', reply_markup=ReplyKeyboardRemove())
        # 待有新的站點再添加判斷
        else :
            pass
        user_data.clear()
        return ConversationHandler.END


async def advance_arguments(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_data = context.user_data
    text = update.message.text
    client = update.message.from_user.first_name
    if text not in time_range_keyboard[0] and text not in time_range_keyboard[1] :
        await update.message.reply_text(
            f"{client} Time Format Error !",
            reply_markup=ReplyKeyboardRemove(),
        )
        return ConversationHandler.END
    user_data["range"] = text
    if user_data['site'] == 'wking' :
        if user_data['function'] == 'rank5' :
            domain_rank = Get_Domain_Rank(range = int(user_data['range'].split(' ')[0]))
            reply = f"<b>💵 Wking Top</b> <code>5</code> <b>Domains Been Accessed During {user_data['range']} </b>\n"
        else :
            domain_rank = Get_Domain_Rank(size = 10, range = int(user_data['range'].split(' ')[0]))
            reply = f"<b>💵 Wking Top</b> <code>10</code> <b>Domains Been Accessed During {user_data['range']} </b>\n"
    # 待有新的站點再添加判斷
    else :
        pass
    domain_rank_converted = domain_rank_reply_converter(domain_rank)
    reply = reply + domain_rank_converted
    await context.bot.send_message(chat_id=update.effective_chat.id, text=reply, parse_mode='HTML', reply_markup=ReplyKeyboardRemove())
    user_data.clear()
    return ConversationHandler.END

async def done(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Display the gathered info and end the conversation."""
    user_data = context.user_data
    client = update.message.from_user.first_name
    await update.message.reply_text(
        f"{client} Bye ~",
        reply_markup=ReplyKeyboardRemove(),
    )
    user_data.clear()
    return ConversationHandler.END


def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(t_token).build()

    # Add conversation handler with the states CHOOSING, TYPING_CHOICE and TYPING_REPLY
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("status", start)],
        states={
            CHOOSING: [
                MessageHandler(
                    filters.Regex("^(wking)$"), functions_choice
                ),
            ],
            TYPING_REPLY: [
                MessageHandler(
                    filters.TEXT & ~(filters.COMMAND | filters.Regex("^Done$")), received_information
                )
            ],
            ADVANCE_CHOICE: [
                MessageHandler(
                    filters.TEXT & ~(filters.COMMAND | filters.Regex("^Done$")), advance_arguments
                ) 
            ]
        },
        fallbacks=[MessageHandler(filters.Regex("^Done$"), done)],
    )

    application.add_handler(conv_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()