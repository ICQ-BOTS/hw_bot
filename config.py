import logging
from logging.config import fileConfig
from pid import PidFile
import pymorphy2
import configparser
import asyncio
import sys
import os


configs_path = os.path.realpath(os.path.dirname(sys.argv[0])) + "/"

if not os.path.isfile(os.path.join(configs_path, "logging.ini")):
        raise FileExistsError(f"File logging.ini not found in path {configs_path}")

logging.config.fileConfig(os.path.join(configs_path, "logging.ini"), disable_existing_loggers=False)
log = logging.getLogger(__name__)


NAME = "assistant_dz"
TOKEN = "***.**********.**********:*********"

loop = asyncio.get_event_loop()
morph = pymorphy2.MorphAnalyzer()


weekday = [
    'понедельник', 
    'вторник',
    'среда',
    'четверг',
    'пятница',
    'суббота',
    'воскресенье'
]

cut_weekday = {
    'пн': 'понедельник',
    'вт': 'вторник',
    'ср': 'среда',
    'чт': 'четверг',
    'пт': 'пятница',
    'сб': 'суббота',
    'вс': 'воскресенье'
}

rus_date = {
    1 : 'понедельник', 
    2 : 'вторник', 
    3 : 'среда', 
    4 : 'четверг', 
    5 : 'пятница',  
    6 : 'суббота', 
    7: 'воскресенье'
}
