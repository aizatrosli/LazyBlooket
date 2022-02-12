### https://github.com/aizatrosli/LazyBooklet
from selenium.webdriver.common.keys import Keys
from seleniumwire import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time, argparse, random, sys, os, gzip

random.seed(100)
parser = argparse.ArgumentParser(description="LazyBooklet")
parser.add_argument('-d', '--delay', help='delay execution', default=0.2)
requiredNamed = parser.add_argument_group('required named arguments')
requiredNamed.add_argument('-i', '--id', help='Game ID', required=True)
requiredNamed.add_argument('-n', '--name', help='Your Name', required=True)
args = parser.parse_args()

params = {
	'gameid': args.id,
	'name': args.name,
	'wait': args.delay,
	'lobbywait': 60*5,
}

options=webdriver.ChromeOptions()
options.use_chromium=True
options.add_argument("--start-maximized")
options.add_argument('--disable-extensions')
options.add_argument("--disable-plugins-discovery")
options.add_argument('--profile-directory=Default')
options.add_experimental_option('excludeSwitches',['enable-logging'])
options.binary_location='chromium-browser'


stage = 'question'
lazypath = '//*[@id="app"]/div/div/div[2]/div/div'
counter = 0
resultstr = ''

def resultstage(driver, cheatbook):
	try:
		trueans, falseans = [], []
		resultboxes = driver.find_elements_by_xpath(lazypath)
		res = resultboxes[0].text
		if res == "INCORRECT":
			falseans.append(ans)
			clearswap(driver)
			correctans = resultboxes[2].text.replace('Correct Answers: ','').split('&')
			trueans.extend(correctans)
		else:
			trueans.append(ans)
		if cheatbook.get(ques, None) is not None:
			trueans.extend(cheatbook.get(ques, None)[True])
			falseans.extend(cheatbook.get(ques, None)[False])
		cheatbook[ques] = {True: list(set([t.strip() for t in trueans])), False: list(set([f.strip() for f in falseans]))}
		clearswap(driver)
		resultboxes[-1].click()
		return res
	except:
		clearswap(driver)
		return 'INCORRECT'

def clearswap(driver):
	try:
		#//*[@id="app"]/div/div/div[3]/div/div/div[2]
		driver.find_elements_by_xpath('//*[@id="app"]/div/div/div[3]/div/div/div[2]').click()
	except:
		pass

def cheststage(driver):
	chestboxes = driver.find_elements_by_xpath(lazypath)
	roll = random.randint(1, len(chestboxes)-1)
	clearswap(driver)
	chestboxes[roll].click()
	time.sleep(0.5)
	clearswap(driver)
	chestboxes[roll].click()
	try:
		clearswap(driver)
		driver.find_element_by_xpath('//*[@id="app"]/div/div/div[2]/div[4]/div[2]/div[1]/div/div[2]/div[2]/div').click()
	except:
		pass

def checkstage(driver):
	try:
		strlastbox = driver.find_elements_by_xpath(lazypath)[-1].text
		if  strlastbox == 'Click Anywhere to Go Next':
			stage = 'result'
		elif not strlastbox:
			stage = 'chest'
		else:
			stage = 'question'
		return stage
	except:
		clearswap(driver)
		return stage

driver=webdriver.Chrome(executable_path='chromedriver')
driver.get('https://www.blooket.com/play')
driver.find_element_by_xpath('//*[@id="app"]/div/div/div[2]/div/form/input').send_keys(params['gameid'])
driver.find_element_by_xpath('//*[@id="app"]/div/div/div[2]/div/form/div[2]').click()
WebDriverWait(driver, params['lobbywait']).until(EC.url_contains("register"))
time.sleep(1)
driver.find_element_by_xpath('//*[@id="app"]/div/div/div[2]/div/form/div[2]/input').send_keys(params['name'])
driver.find_element_by_xpath('//*[@id="app"]/div/div/div[2]/div/form/div[2]/div').click()
WebDriverWait(driver, params['lobbywait']).until(EC.url_contains("lobby"))
time.sleep(1)
print(f'Waiting other players !!!')
WebDriverWait(driver, params['lobbywait']).until(EC.url_contains("gold"))
print('#'*50)
cheatbook = {}
while not driver.current_url.endswith('final'):
	try:
		if cheatbook:
			print(f'{"="*50} \n No.{counter} | {resultstr}\n{cheatbook}\n{"="*50}')
		while stage != 'question':
			stage = checkstage(driver)
			time.sleep(params['wait'])
		print(f'> question stage ', end='')
		questionboxes = driver.find_elements_by_xpath(lazypath)
		ques = questionboxes[0].text
		if cheatbook.get(ques, None) is None:
			clearswap(driver)	
			ans = questionboxes[1].text
			questionboxes[1].click()
		else:
			correctans = cheatbook.get(ques, None)[True]
			for quesbox in questionboxes[1:]:
				clearswap(driver)
				ans = quesbox.text
				if ans in correctans:
					quesbox.click()
					break
		while stage != 'result':
			stage = checkstage(driver)
			time.sleep(params['wait'])
		print(f'> result stage ', end='')
		resultstr = resultstage(driver, cheatbook)
		if resultstr == 'CORRECT':
			while stage != 'chest':
				stage = checkstage(driver)
				time.sleep(params['wait'])
			print(f'> chest stage ')
			cheststage(driver)
		counter += 1
		print('*'*50)
	except:
		if driver.current_url.endswith('final'):
			break
		clearswap(driver)
		print('Waiting to navigate back to Question stage!')
		while stage != 'question':
			stage = checkstage(driver)
			time.sleep(params['wait'])
		pass





