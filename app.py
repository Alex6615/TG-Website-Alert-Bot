import os 

import logging
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

from secret_telegram import TELEGRAM_TOKEN
t_token = TELEGRAM_TOKEN

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


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="❤️ I'm a Website_alerts Bot")

async def usercount(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if len(args) == 0 :
        count = Get_Wking_UserCount()
        reply = '<b>🌏 Wking Online Users Now : </b>'
        reply = reply + '<code>' + count + '</code>'
        await context.bot.send_message(chat_id=update.effective_chat.id, text=reply, parse_mode='HTML')
    else :
        await context.bot.send_message(chat_id=update.effective_chat.id, text="no site avaliable now", parse_mode='HTML')

async def rank5(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if len(args) == 0 :
        domain_rank = Get_Domain_Rank()
        reply = f"<b>💵 Wking Top</b> <code>5</code> <b>Domains Been Accessed During 1 Hour </b>\n"
        domain_rank_converted = domain_rank_reply_converter(domain_rank)
        reply = reply + domain_rank_converted
        await context.bot.send_message(chat_id=update.effective_chat.id, text=reply, parse_mode='HTML')
    elif len(args) == 1 :
        domain_rank = Get_Domain_Rank(range=args[0])
        reply = f"<b>💵 Wking Top</b> <code>5</code> <b>Domains Been Accessed During {args[0]} Hour </b>\n"
        domain_rank_converted = domain_rank_reply_converter(domain_rank)
        reply = reply + domain_rank_converted
        await context.bot.send_message(chat_id=update.effective_chat.id, text=reply, parse_mode='HTML')


async def rank10(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if len(args) == 0 :
        domain_rank = Get_Domain_Rank(size=10)
        reply = f"<b>💵 Wking Top</b> <code>10</code> <b>Domains Been Accessed During 1 Hour </b>\n"
        domain_rank_converted = domain_rank_reply_converter(domain_rank)
        reply = reply + domain_rank_converted
        await context.bot.send_message(chat_id=update.effective_chat.id, text=reply, parse_mode='HTML')
    elif len(args) == 1 :
        domain_rank = Get_Domain_Rank(size=10, range=args[0])
        reply = f"<b>💵 Wking Top</b> <code>10</code> <b>Domains Been Accessed During {args[0]} Hour </b>\n"
        domain_rank_converted = domain_rank_reply_converter(domain_rank)
        reply = reply + domain_rank_converted
        await context.bot.send_message(chat_id=update.effective_chat.id, text=reply, parse_mode='HTML')






if __name__ == '__main__':

    """Run the bot."""

    start_handler = CommandHandler('start', start)
    usercount_handler = CommandHandler('usercount', usercount)
    rank5_handler = CommandHandler('rank5', rank5)
    rank10_handler = CommandHandler('rank10', rank10)


    application = Application.Builder().token(t_token).build()
    
    application.add_handler(start_handler)
    application.add_handler(usercount_handler)
    application.add_handler(rank5_handler)
    application.add_handler(rank10_handler)


    application.run_polling()
    