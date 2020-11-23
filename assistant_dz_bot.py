from config import *
from handlers import *
from my_filter import Filter
from mailru_im_async_bot.bot import Bot
from mailru_im_async_bot.handler import MessageHandler, CommandHandler, DefaultHandler, StartCommandHandler


bot = Bot(token=TOKEN, name=NAME)

# Register your handlers here
# ---------------------------------------------------------------------
bot.dispatcher.add_handler(StartCommandHandler(callback=start))
bot.dispatcher.add_handler(MessageHandler(
        callback=del_schedule, 
        filters=Filter.chaotic_args(['удали', ['рассписание', 'расписание']])
    )
)
bot.dispatcher.add_handler(MessageHandler(
      callback=read_homework,
      filters=Filter.chaotic_args(['покажи', 'домашку', ['по', 'на']])
  ) 
)
bot.dispatcher.add_handler(MessageHandler(
      callback=v_stop,
      filters=Filter.regexp('(?i)^({})'.format('cтоп|никакие|никакой|нет'))
  )
)
bot.dispatcher.add_handler(MessageHandler(
      callback=write_schedule,
      filters=Filter.chaotic_args(['добавь', ['расписание', 'рассписание']])
  )
)
bot.dispatcher.add_handler(MessageHandler(
      callback=write_homework,
      filters=Filter.chaotic_args(['запиши', 'домашку', 'по'])
  )
)
bot.dispatcher.add_handler(MessageHandler(
      callback=all_homework,
      filters=Filter.chaotic_args([['покажи','что'], ['всю', 'мне'], ['домашку', 'задали', 'задали?']])
  )
)
bot.dispatcher.add_handler(DefaultHandler(
        callback=def_phrases
    )
)


with PidFile(NAME):
    try:
        loop.create_task(bot.start_polling())
        loop.run_forever()
    finally:
        loop.close()
