from random import randint, choice
from tarantool_utils import *
from config import *
import datetime


async def def_phrases(bot, event):
	if event.type.value == 'newMessage':
		user = User(user_id=event.from_chat).get()
		if user.old_mes['schedule']:
			await write_schedule(bot, event)
		elif user.old_mes['homework']:
			await write_homework(bot, event)
		elif user.old_mes['del_schedule']:
			await del_schedule(bot, event)
		else:
			if event.data['chat']['type'] == 'private':
				await start(bot, event)


async def v_stop(bot, event):
	user = User(user_id=event.from_chat).get()
	if user.old_mes['schedule'] or user.old_mes['homework'] or user.old_mes['text'] \
	or user.old_mes['del_schedule']:
		user.old_mes.update({'schedule': None, 'homework': None, 'text': None, 'del_schedule': None})
		user.save()
		await bot.send_text(
			chat_id=event.from_chat,
			text="Чтош. Давай просто поболтаем."
			)
	else:
		await def_phrases(bot, event)

async def del_schedule(bot, event):
	user = User(user_id=event.from_chat).get()
	if user.old_mes['del_schedule'] is None:
		user.old_mes['del_schedule'] = event.data['text'].lower()
	else:
		user.old_mes['del_schedule'] += " " + event.data['text'].lower()
	args = user.old_mes['del_schedule'].split()
	index_duplicate = is_duplicate(args, weekday)
	if index_duplicate:
		# ищем все дни недели в сообщении и удаляем их из бд если есть
		for index, c in enumerate(args):
			p = morph.parse(c)[0].normal_form
			p = cut_weekday[p] if cut_weekday.get(p) else p
			if p in weekday:
				if user.schedule.get(p):
					user.schedule.pop(p)
		await bot.send_text(
			chat_id=event.from_chat,
			text="Готово, удалил."
		)	
		user.old_mes['del_schedule'] = None
	else:
		await bot.send_text(
			chat_id=event.from_chat,
			text="Укажи дни, которые нужно очистить от расписание через запятую."
		)		
	user.save()


async def write_schedule(bot, event):
	chat_id = event.from_chat
	user = User(user_id=chat_id).get()
	# Записиваем последовательность всех сообщений юзера
	if user.old_mes['schedule'] is None:
		user.old_mes['schedule'] = event.data['text'].lower()
	else:
		user.old_mes['schedule'] += " " + event.data['text'].lower()
	# Находим индекс сообщения с днём недели
	args = user.old_mes['schedule'].split()
	index_duplicate = is_duplicate(args, weekday)
	if index_duplicate:
		# Находим все предметы, которые были записаны после слов с днём недели
		schedule = ' '.join(args[index_duplicate + 1:]).split(',')
		if len(schedule) >= 1 and len(args[index_duplicate + 1:]) >= 1:
			# Убираем пробелы в листе и ставим слова в Именительный падеж
			schedule_text = [str(index + 1) + ' Урок: ' + c.strip() for index, c in enumerate(schedule)]
			schedule = [morph.parse(c.strip())[0].normal_form for c in schedule]
			if cut_weekday.get(args[index_duplicate]):
				schedule_weekday = cut_weekday[args[index_duplicate]]
			else:
				schedule_weekday = args[index_duplicate]
			p = morph.parse(schedule_weekday)[0]
			schedule_weekday = p.inflect({'accs'}).word if p.tag.POS == 'NOUN' else schedule_weekday
			await bot.send_text(
				chat_id=chat_id,
				text="Готово. Твое расписание на {}:\n{}".format(schedule_weekday,
					'\n'.join(schedule_text))
			)
			# Ставим день недели в Именительный падеж
			p = morph.parse(schedule_weekday)[0].normal_form
			user.schedule[p] = schedule
			user.old_mes['schedule'] = None
		else:
			p = morph.parse(args[index_duplicate])[0]
			schedule_weekday = p.inflect({'accs'}).word if p.tag.POS == 'NOUN' else args[index_duplicate]
			await bot.send_text(
				chat_id=chat_id,
				text="Какие уроки у тебя в {}? (напиши все предметы через запятую)"\
				.format(schedule_weekday)
			)	
	else:
		await bot.send_text(
			chat_id=chat_id,
			text="На какой день?"
		)
	user.save()


async def write_homework(bot, event):
	chat_id = event.from_chat
	user = User(user_id=chat_id).get()
	# Записиваем последовательность всех сообщений юзера
	if user.old_mes['homework'] is None:
		user.old_mes['homework'] = event.data['text']
	else:
		user.old_mes['homework'] += " " + event.data['text']	

	args = user.old_mes['homework'].lower().split()
	# ищем слово по, и проверяем то что оно стоит в конце
	index_text = args.index('по') + 1 if args.index('по') else 0
	if index_text == len(args) - 1:
		await bot.send_text(
			chat_id=chat_id,
			text="Что задали?"
		)	
		user.save()	
	elif index_text <= len(args) - 1:
		await bot.send_text(
			chat_id=chat_id,
			text="Готово, записал ДЗ по {}:\n- {}".format(args[index_text], ' '.join(user.old_mes['homework'].split()[index_text + 1:]))
		)
		# Переводим название предмета к нормальной форме
		p = morph.parse(args[index_text])[0].normal_form
		# Записываем всё, что идёт после названия предмета
		user.homework[p] = ' '.join(user.old_mes['homework'].split()[index_text + 1:])
		user.old_mes['homework'] = None
		user.save()
		user.update_stat(index=5)	
	else:
		await bot.send_text(
			chat_id=chat_id,
			text="По какому предмету записать ДЗ?"
		)
		user.save()
	


async def read_homework(bot, event):
	user = User(user_id=event.from_chat).get()
	# Полученый текст приводим к нормальной форме(именительный падеж) и получаем лист,
	# Для поиска, если укажут день недели
	args = [morph.parse(c)[0].normal_form for c in event.data['text'].lower().split()]
	index_duplicate = is_duplicate(args, weekday)
	# Ищем в сообщении пользователя предмет, который возможно он записал когда-то
	index_homework = get_gomework_object(args, user)
	text = ''
	if index_duplicate:
		# Ищем расписание на день недели, который написали
		text = get_homework(text, args[index_duplicate], user)
	elif index_homework:
		text = "Домашка по {}:\n{}".format(index_homework, user.homework[index_homework])
	else:
		data = datetime.datetime.today().isoweekday()
		i = data
		# Перебираем до тех пор. пока не найдём хоть одну домашку, на каком-то дне недели
		j = 0 
		while j < 7:
			# Следующий день недели, если не указали день недели 
			i = i + 1 if i <= 6 else 1
			text = get_homework(text, rus_date[i], user)
			if text != '':
				break
			j += 1
	if text == '':
		text = 'Нету домашки'	

	await bot.send_text(
			chat_id=event.from_chat,
			text=text
		)	



def get_gomework_object(args, user):
	for arg in args:
		if arg in user.homework.keys():
			return arg	


def get_homework(text, weekday, user):
	weekday = cut_weekday.get(weekday, weekday)
	get = user.schedule.get(weekday)
	if get:
		for c in get:
			if user.homework.get(c):
				text += "Домашка по {}:\n{}\n".format(c, user.homework[c])	
	return text 

async def all_homework(bot, event):
	user = User(user_id=event.from_chat).get()
	text = ''
	if len(user.homework) >= 1:
		for c in user.homework:
			text += "Домашка по {}:\n{}\n".format(c, user.homework[c])
	else:
		text += "Нету домашки"

	await bot.send_text(
			chat_id=event.from_chat,
			text=text
		)


def is_duplicate(list1, list2):
	for index, c in enumerate(list1):
		p = morph.parse(c)[0].normal_form
		p = cut_weekday[p] if cut_weekday.get(p) else p
		if p in list2:
			
			return index
	return False


async def start(bot, event):
	await bot.send_text(
			chat_id=event.from_chat,
			text="""😎 Привет! 

Я могу записывать твое расписание и дз. Добавь меня в общий чат класса, и все твои одноклассники смогут спрашивать у меня, что задали и какие уроки в пятницу. 

📒 Все доступные команды:
  
Добавь расписание
Удали расписание
Запиши домашку по *название предмета*
Что мне задали?
Покажи домашку на *день недели*
Покажи домашку по *название предмета*
Покажи всю домашку"""
		)

async def media(bot, event):
	await bot.send_text(
			chat_id=event.from_chat,
			text="Пришли, пожалуйста, текстовое сообщение"
		)	
