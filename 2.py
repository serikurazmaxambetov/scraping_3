from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
import pickle
import lxml
from bs4 import BeautifulSoup
from telebot import types
import telebot
from webdriver_manager.chrome import ChromeDriverManager


client = telebot.TeleBot('your api')
@client.message_handler(commands=['start'])
def sen_hello(message):	
	try:
		
	
		if message.chat.id == 1931048734:
			
			oy = 0
			client.send_message(message.chat.id, "Второй бот начинает работу!")
			options = webdriver.ChromeOptions()
			options.add_argument("--no-sandbox")
			options.add_argument('--disable-dev-shm-usage')  
			options.headless = True
			options.add_argument("--disable-extensions")
			driver = webdriver.Chrome(ChromeDriverManager().install(), options = options)
			arr = []	
			driver.get("https://ambasada-r-moldova-in-f-rusa.reservio.com/client/login?_fid=0u55")
			sleep(2)
			for cookie in pickle.load(open("login_cookies", "rb")):
				driver.add_cookie(cookie)
			sleep(2)
			
			while True:
				print(oy)
				links = [
								'https://ambasada-r-moldova-in-f-rusa.reservio.com/booking?businessId=09250556-2450-437f-aede-82e78712f114&serviceId=c2fbd5eb-6966-4ead-b7c1-1a0eb65cf295',
								'https://ambasada-r-moldova-in-f-rusa.reservio.com/booking?businessId=09250556-2450-437f-aede-82e78712f114&serviceId=63fe0e8c-b127-43e3-874a-bac9c660045b',
								'https://ambasada-r-moldova-in-f-rusa.reservio.com/booking?businessId=09250556-2450-437f-aede-82e78712f114&serviceId=038869df-58b5-437e-b3cf-60c5419ab053',
								'https://ambasada-r-moldova-in-f-rusa.reservio.com/booking?businessId=09250556-2450-437f-aede-82e78712f114&serviceId=59c845fa-48c9-4f79-b7b2-1d07f895f2e6'
							]
				try:
					for link in links:
						
						driver.get(link)
						sleep(15)
						oy+=1
						print(oy)
						if "Нет свободных мест" in driver.page_source or "Бронирование не доступно" in driver.page_source:
							continue

						elif "Нет свободных мест" not in driver.page_source or "Бронирование не доступно" not in driver.page_source:
							bs = BeautifulSoup(driver.page_source, "lxml")
							число = bs.find('div', class_='box-date__calendar').text.replace("\n", " ")
							times = bs.find('div', class_= 'booking-time-items').find_all('a')
							услуга = bs.find('div', class_="list__itemHeaderContent-desc").text
							for i in times:
								if [число, услуга, i.text] not in arr:

									keyboard = types.InlineKeyboardMarkup()
									tex = f'{число} ' + f'{i.text}'
									url_button = types.InlineKeyboardButton(text=tex, url='https://ambasada-r-moldova-in-f-rusa.reservio.com' + i.get('href'))
									keyboard.add(url_button)
									client.send_message(message.chat.id, "Услуга - " + услуга, reply_markup=keyboard)
									arr.append([число, услуга, i.text])
								else:
									continue
				except Exception as e:
					print(oy)
					oy+=1
					continue
		elif message.chat.id != 1931048734:
			client.send_message(message.chat.id, "Вы не являетесь хозяйном этого бота")
	except Exception as e:
		client.send_message(message.chat.id, 'Возникла ошибка, Введите старт для перезагрузки')
client.polling(none_stop = True)
