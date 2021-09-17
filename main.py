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
from tkinter import filedialog, constants, Tk
import urllib.request

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


URL = 'https://unsplash.com/collections/8946027/moto'
image_size = input(
    'Please select the image size [S,M,L,(O)Original]: ').lower()

while image_size not in ['s', 'm', 'l', 'o']:
    image_size = input(
        'Please select the image size [S,M,L,(O)Original]: ').lower()

root = Tk()
root.directory = filedialog.askdirectory()
save_path = root.directory
root.destroy()


t.start()

options = webdriver.ChromeOptions()
# options.add_argument('headless')

driver = webdriver.Chrome(
    ChromeDriverManager().install(), options=options)

photos_links = {}


def grap_links():
    source = driver.page_source

    soup = bs(source, 'lxml')

    for a in soup.find_all('a', {'title': 'Download photo'}):
        if a['href'] in photos_links:
            pass
        else:
            photos_links[a['href']] = 0


driver.get(URL)

photos_count = 0

source = driver.page_source
soup = bs(source, 'lxml')
spans = soup.find('div', {'class': '_2sKzG _2sCnE PrOBO _1CR66'}).children
for span in spans:
    texts = span.text.split()
    photos_count = int(texts[0])

wait = WebDriverWait(driver, 10)

driver.execute_script("""
    var el = document.getElementsByClassName('_2gyVS _27Bp2')[0];
    el.parentNode.removeChild(el);

    var el = document.getElementsByClassName('_3c7Pb _2sCnE PrOBO _1CR66')[0];
    el.parentNode.removeChild(el);
""")


element = wait.until(EC.presence_of_element_located(
    (By.XPATH, '//*[@id="app"]/div/div[6]/div/button')))

grap_links()

element.click()


SCROLL_PAUSE_TIME = 0.2


while True:
    grap_links()

    driver.execute_script("""
        window.scrollBy(0,500)
    """)
    time.sleep(SCROLL_PAUSE_TIME)

    if len(photos_links) == photos_count:
        break


driver.close()


def download_photo(link, image_size, file_name):

    if image_size == 's':
        urllib.request.urlretrieve(link+'&w=640', save_path + "/"+file_name)
    elif image_size == 'm':
        urllib.request.urlretrieve(link+'&w=1920', save_path + "/"+file_name)
    elif image_size == 'l':
        urllib.request.urlretrieve(link+'&w=2400', save_path + "/"+file_name)
    elif image_size == 'o':
        urllib.request.urlretrieve(link, save_path + "/"+file_name)


counter = 1
for link in photos_links:
    download_photo(link, image_size, "photo_"+str(counter))
    counter += 1

done = True
