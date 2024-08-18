#from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import selenium.webdriver.support.expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
#from selenium.webdriver.chrome.service import Service as ChromeService
#from webdriver_manager.chrome import ChromeDriverManager
import undetected_chromedriver as uc
import requests
import time
#import random
#import string

# Função para gerar email temporário
def gerar_email_temp():
    response = requests.get("https://www.1secmail.com/api/v1/?action=genRandomMailbox&count=1")
    email = response.json()[0]
    return email

# Função para verificar se o email foi recebido
def pegar_email_temp(email):
    login, domain = email.split('@')
    while True:
        response = requests.get(f"https://www.1secmail.com/api/v1/?action=getMessages&login={login}&domain={domain}")
        if response.json():
            id_message = response.json()[0]['id']
            return id_message
        time.sleep(5)

# Função para obter o link de confirmação no email
def pegar_link_confirmacao(email, id_message):
    login, domain = email.split('@')
    response = requests.get(f"https://www.1secmail.com/api/v1/?action=readMessage&login={login}&domain={domain}&id={id_message}")
    link_confirmacao = response.json()['body'].split('href="')[1].split('"')[0]
    return link_confirmacao

# Configuração do Selenium
if __name__ == "__main__":
    driver = uc.Chrome(headless=False,use_subprocess=False)
    driver.implicitly_wait(20)
    driver_wait = WebDriverWait(driver,10)

    driver.get("put url here")

    email_temp = gerar_email_temp()
    try:
        driver_wait.until(
            ec.presence_of_element_located((By.XPATH, '//*[@class="alone_button submit_alike gui_pos_rel"]'))).click()
    except Exception as e:
        pass

    driver_wait.until(ec.presence_of_element_located((By.XPATH,'//*[@class="alone_button vote_button gui_pos_rel"]'))).click()
    driver_wait.until(ec.presence_of_element_located((By.XPATH,'//*[@id="login_reminder"]/div[2]/div/ul/li/div/div[3]/a'))).click()

    campo_email = driver.find_element(By.NAME, 'email')
    campo_email.send_keys(email_temp)
    campo_email.send_keys(Keys.RETURN)
    driver_wait.until(ec.presence_of_element_located((By.XPATH,'//*[@id="login_reminder"]/div[2]/div/ul/li/div/article/div[2]/div/div/a'))).click()

    time.sleep(20)

    id_message = pegar_email_temp(email_temp)

    link_confirmacao = pegar_link_confirmacao(email_temp, id_message)

    driver.get(link_confirmacao)


    driver.quit()
