import PyPDF2
import pandas
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager


options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(options=options, service=ChromeService(ChromeDriverManager().install()))


driver.get('http://www.google.com/');

time.sleep(5) # Let the user actually see something!

search_box = driver.find_element(By.XPATH,'/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/textarea')

search_box.send_keys('Hola')

search_box.submit()

hola = driver.find_element(By.XPATH,'/html/body/div[7]/div/div[13]/div[1]/div[2]/div[2]/div/div/div[1]/div/div/div/div/div/div/div/div[1]/a/h3')

time.sleep(5) # Let the user actually see something!

driver.quit()