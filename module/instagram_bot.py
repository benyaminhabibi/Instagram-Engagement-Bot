from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

class InstagramBot:
    def __init__(self, graphic_mode:bool):
        options = webdriver.ChromeOptions()
        if not graphic_mode:
            options.add_argument('--headless')
            options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    def login(self, username, password):
        self.driver.get('https://www.instagram.com/accounts/login/')
        time.sleep(5)
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        time.sleep(5)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        time.sleep(5)
        self.driver.find_element(By.XPATH, '//button[@type="submit"]').click()
        time.sleep(10)

        if "Sorry, your password was incorrect" in self.driver.page_source:
            return False
        return True

    def get_driver(self):
        return self.driver

    def quit(self):
        self.driver.quit()