import PyPDF2
import pandas
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

user = "tabaress@globalhitss.com"
psw = "123456"
cerrar_emerg1 = '/html/body/div[1]/div/div[3]/div/div/div[1]/button/span'
cerrar_emerg2 = '/html/body/div[1]/div/div[2]/div/div/div[3]/button'
Xpath_usuario = '/html/body/div[1]/div/div[1]/div/form/div[1]/input'
Xpath_contrasena = '/html/body/div[1]/div/div[1]/div/form/div[2]/input'
boton_ingresar = '/html/body/div[1]/div/div[1]/div/form/div[4]/input'

url = 'https://www.talentosclaro.com/Account/Login?ReturnUrl=%2FEmployees%2FUnCertificate'
#archivo_pdf =  open('1-EticaLaboral.pdf', 'rb')

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(options=options, service=ChromeService(ChromeDriverManager().install()))


#driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
#driver = webdriver.Chrome(executable_path=r"G:\Mi unidad\Carrera\PrácticaClaro\validacionCertificados\chromedriver.exe")
#driver.maximize_window()

driver.get(url)

#wait = WebDriverWait(driver,10)
#wait.until(ec.visibility_of_all_elements_located((By.XPATH, cerrar_emerg1)))
time.sleep(5)
driver.find_element(By.XPATH, "/html/body/div[1]/div/div[3]/div/div/div[3]/button").click


print(driver.find_element(By.XPATH, cerrar_emerg1))
time.sleep(5)
driver.quit()

