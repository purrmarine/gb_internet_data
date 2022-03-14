from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from pymongo import MongoClient
from pprint import pprint
import time

client = MongoClient('127.0.0.1', 27017)
db = client['mail']
letters = db.letters

s = Service('./chromedriver')
options = Options()
options.add_argument('start-maximized')

driver = webdriver.Chrome(service=s, options=options)
driver.implicitly_wait(10)

driver.get('https://mail.ru/')

mailbox = driver.find_element(By.CLASS_NAME, 'mailbox-service')
driver.get(mailbox.get_attribute('href'))

elem = driver.find_element(By.NAME, 'username')
elem.send_keys("study.ai_172")
elem.send_keys(Keys.ENTER)

elem = driver.find_element(By.NAME, 'password')
elem.send_keys("NextPassword172#")
elem.send_keys(Keys.ENTER)

links = set()

last_len = 0
while True:
    mail_letters = driver.find_elements(By.XPATH, "//a[contains(@href,'/inbox/0:')]")
    for letter in mail_letters:
        link = letter.get_attribute('href')
        links.add(link)
    if len(links) > last_len:
        last_len = len(links)
    else:
        break
    actions = ActionChains(driver)
    actions.move_to_element(mail_letters[-1])
    actions.perform()
    time.sleep(1)

for link in links:
    item_info = {}

    driver.get(link)

    contact = driver.find_element(By.CLASS_NAME, 'letter-contact').text
    date = driver.find_element(By.CLASS_NAME, 'letter__date').text
    topic = driver.find_element(By.CLASS_NAME, 'thread-subject').text
    text = driver.find_element(By.CLASS_NAME, 'letter-body').text

    item_info['contact'] = contact
    item_info['date'] = date
    item_info['topic'] = topic
    item_info['text'] = text

    if not letters.find_one({'topic': item_info['topic'], 'contact': item_info['contact'], 'date': item_info['date']}):
        letters.insert_one(item_info)

driver.close()

for doc in letters.find({}):
    pprint(doc)
