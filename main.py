import selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Hunting:
    def __init__(self):
        self.driver_path = "seu_caminho/chromedriver.exe"
        self.service = Service(self.driver_path)
        self.browser = webdriver.Chrome(service=self.service)
    
    def do_login(self, username, password):
        self.browser.get("https://www.linkedin.com/")
        username_field = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="session_key"]'))
        )
        
        password_field = self.browser.find_element(By.XPATH, '//*[@id="session_password"]')
        username_field.send_keys(username)
        password_field.send_keys(password)
        
        login_button = WebDriverWait(self.browser, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="main-content"]/section[1]/div/div/form/div/button'))
        )
        login_button.click()
        
        self.browser.implicitly_wait(10)

    def do_search_by_people(self, search_term):
        search_field = self.browser.find_element(By.XPATH, '//*[@id="global-nav-typeahead"]/input')
        search_field.send_keys(search_term)
        search_field.send_keys(Keys.ENTER)
        self.browser.implicitly_wait(10)
        for page_number in range(1, 101):
            page_url = f"https://www.linkedin.com/search/results/people/?keywords={search_term}&origin=SWITCH_SEARCH_VERTICAL&page={page_number}&sid=2dK"
            self.browser.get(page_url)
            self.browser.implicitly_wait(10)
            self.add_not_added_users()
            page_number += 1

    def add_not_added_users(self):
        entire_results = self.browser.find_element(By.XPATH, '//*[@class="search-results-container"]/div/div[1]/ul[1]')
        for person in entire_results.find_elements(By.TAG_NAME, 'li'):
            buttons = person.find_elements(By.TAG_NAME, 'button')
            for button in buttons:
                if "Conectar" in button.text:
                    button.click()
                    self.browser.implicitly_wait(10)
            
                    WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.ID, 'artdeco-modal-outlet')))
            
                    # Encontrar o botão "Enviar" dentro do popup
                    send_button = self.browser.find_element(By.XPATH, '//button[contains(@aria-label, "Enviar agora")]')
                    send_button.click()
                    break
            



if __name__ == "__main__":
    hunting = Hunting()
    username = "usuario"
    password = "senha"
    search_term = "tech recruiter"
    hunting.do_login(username, password)
    hunting.do_search_by_people(search_term)
