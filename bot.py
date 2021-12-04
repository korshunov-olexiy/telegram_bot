from itertools import groupby
from urllib.parse import urlparse

import telebot
import validators
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from config_bot import config

TOKEN = config['token']
bot = telebot.TeleBot(TOKEN)

chrome_options = Options()
chrome_options.add_argument('--headless')

def norm_spaces(s: str) -> str:
    '''replace many spaces to one space in string'''
    return ''.join(' ' if chr == ' ' else ''.join(times) for chr,times in groupby(s))

@bot.message_handler(commands=['start'])
def hello_user(message) -> None:
    bot.send_message(message.chat.id, "Hello. This bot returns you an image of the site you specified. Use /url command and address of site")

@bot.message_handler(commands=['help'])
def show_help(message) -> None:
    bot.send_message(message.chat.id, 'To get a screenshot of the site, use the /url command.\nExample: /url https://www.google.com')

@bot.message_handler(commands=['url'])
def get_screenshot(message) -> None:
    uid = message.chat.id
    url = ""
    try:
        url = norm_spaces(message.text).split(' ')[1]
        image_name = f"{urlparse(url).netloc}.png"
    except IndexError:
        bot.send_message(uid, 'After the command /url, you need to enter a valid URL!')
        return
    if not validators.url(url):
        bot.send_message(uid, 'I could not open the URL. Try later.')
    else:
        driver = webdriver.Chrome(executable_path='./chromedriver', options=chrome_options)
        driver.set_window_size(1920, 1080)
        try:
            driver.get(url)
            png = driver.get_screenshot_as_png()
            bot.send_document(uid, png, visible_file_name=image_name)
        except Exception as err:
            print(err)
        finally:
            driver.quit()

if __name__ == '__main__':
    bot.infinity_polling()

