from re import T
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as bs
import itertools
import threading
import sys
import requests


# URL = input(
#     'Please enter the url for the collection you want to download, starting with https://www.:   ')
done = False


def loading_animation():
    for c in itertools.cycle(['|', '/', '-', '\\']):
        if done:
            break
        sys.stdout.write('\rloading ' + c)
        sys.stdout.flush()
        time.sleep(0.1)
    sys.stdout.write('\rDone!     ')


t = threading.Thread(target=loading_animation)


t.start()

URL = 'https://unsplash.com/collections/1522571/winter'
options = webdriver.ChromeOptions()
# options.add_argument('headless')

driver = webdriver.Chrome(
    ChromeDriverManager().install(), options=options)


driver.get(URL)

wait = WebDriverWait(driver, 10)

driver.execute_script("""
    var el = document.getElementsByClassName('_2gyVS _27Bp2')[0];
    el.parentNode.removeChild(el);

    var el = document.getElementsByClassName('_3c7Pb _2sCnE PrOBO _1CR66')[0];
    el.parentNode.removeChild(el);
""")


driver.execute_script(
    "window.scrollTo(0, (document.body.scrollHeight/2));")

time.sleep(3)

element = wait.until(EC.presence_of_element_located(
    (By.XPATH, '//*[@id="app"]/div/div[6]/div/button')))

element.click()

time.sleep(1)

SCROLL_PAUSE_TIME = 0.5

# Get scroll height
last_height = driver.execute_script("return document.body.scrollHeight-2000")


while True:
    # Scroll down to bottom
    driver.execute_script(
        "window.scrollTo(0, (document.body.scrollHeight-4000));")

    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)

    new_height = driver.execute_script(
        "return document.body.scrollHeight-4000")
    if new_height == last_height:
        break
    last_height = new_height


source = driver.page_source
soup = bs(source, 'lxml')
for a in soup.find_all('a', {'title': 'Download photo'}):
    pass

done = True
