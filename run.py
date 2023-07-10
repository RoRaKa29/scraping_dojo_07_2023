import os
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv


class Scraper:
    def __init__(self):
        load_dotenv()
        self.url = os.getenv('INPUT_URL')
        self.output_file = os.getenv('OUTPUT_FILE')
        chrome_options = Options()
        webdriver_service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)

    def scrape(self):
        self.driver.get(self.url)
        quotes = []

        while True:
            time.sleep(10)

            quote_elements = self.driver.find_elements(By.CLASS_NAME, "quote")
            for quote_element in quote_elements:
                text = quote_element.find_element(By.CLASS_NAME, "text").text
                author = quote_element.find_element(By.CLASS_NAME, "author").text
                tag_elements = quote_element.find_elements(By.CLASS_NAME, "tag")
                tags = [tag_element.text for tag_element in tag_elements]
                quote = {
                    "text": text,
                    "by": author,
                    "tags": tags
                }
                quotes.append(quote)

            next_buttons = self.driver.find_elements(By.XPATH, "//li[@class='next']/a")
            if len(next_buttons) == 0:
                break

            next_button = next_buttons[0]
            ActionChains(self.driver).move_to_element(next_button).click(next_button).perform()

        with open(self.output_file, 'w') as f:
            for quote in quotes:
                f.write(json.dumps(quote) + "\n")

        self.driver.quit()


if __name__ == "__main__":
    scraper = Scraper()
    scraper.scrape()
