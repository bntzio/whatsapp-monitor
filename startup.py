#! /usr/local/bin/python3
from urllib.parse import quote
from time import sleep
from pyperclip import copy
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

TARGET = 'Sebastian New'
PRODUCTION = False
SCANNED = False
HOST = 'http://localhost:3000'

if PRODUCTION is True:
    HOST = 'http://whatsapp-monitor.now.sh'

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--window-size=1920x1080')
chrome_options.add_argument(
    'user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36'
)
browser = webdriver.Chrome(chrome_options=chrome_options)
browser.get('https://web.whatsapp.com')
while SCANNED is False:
    image = browser.find_element_by_tag_name('img')
    image_src = image.get_attribute('src')
    encoded = quote(image_src, safe='')
    url = HOST + '/' + encoded
    copy(url)
    print('\nLink copied to your clipboard, you got 20 seconds to visit it and scan your QR code.')
    print('Waiting QR Scanning...')
    sleep(20)
    try:
        notice = browser.find_element_by_class_name('iHhHL')
        if notice.text == 'Keep your phone connected':
            SCANNED = True
            print('Success!')
    except NoSuchElementException:
        pass
search = browser.find_element_by_id('input-chatlist-search')
search.send_keys(TARGET)
browser.save_screenshot('screenshot.png')
chats = browser.find_elements_by_class_name('_1wjpf')
for chat in chats:
    name = chat.get_attribute('title')
    if TARGET in name:
        chat.click()
        while True:
            try:
                online = browser.find_element_by_class_name('O90ur').text
                if online == 'online':
                    print(TARGET + ' is online!')
            except NoSuchElementException:
                pass
        sleep(2)
# browser.save_screenshot('screenshot.png')
