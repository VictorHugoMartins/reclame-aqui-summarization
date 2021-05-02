import utils

import selenium
from lxml import html
from selenium import webdriver
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import logging
import sqlite3
from datetime import datetime
import database
import time

conn = sqlite3.connect('database.db')  # You can create a new database by changing the name within the quotes
now = datetime.now().strftime("%B %d, %Y %I:%M%p")

class Ratings():
    # Prepare the driver and get the reviews exploring the pages
    def get_reviews(enterprise, n_pages_to_scrape):
        if n_pages_to_scrape == None:
            n_pages_to_scrape = 10
            
        for page in range(1, n_pages_to_scrape + 1):
            print("Scrapping page " + str(page))
            url = 'https://www.reclameaqui.com.br/empresa/' + enterprise + '/lista-reclamacoes/?pagina=' + str(page)
            driver = utils.prepare_driver(url)

            if ( Ratings.check_if_end_of_list(driver)):
                break
            else:
                Ratings.get_complains_of_list(driver, enterprise)

            driver.quit()

    # Check if has more elements to scrape in the page
    def check_if_end_of_list(driver):
        complain_list = driver.find_elements_by_xpath('//ul[@class="complain-list"]/li')
        if len(complain_list) == 0:
            return True
        else:
            return False

    def handle_page(enterprise, subcategory, page):
        url = 'https://www.reclameaqui.com.br/empresa/' + enterprise + '/lista-reclamacoes/'
        url = url + '?pagina=' + str(page)
        if subcategory != '':
            url = url + '&' + subcategory
        return url

    # Get the individual link of each complain and explore them
    def get_complains_of_list(driver, enterprise, category='', subcategory='', subcategory_id=''):
        complain_list = driver.find_elements_by_xpath('//ul[@class="complain-list"]/li')
        for complain in complain_list:
            this_one = complain.find_element_by_xpath('a')
            link = this_one.get_attribute('href')
            title = this_one.find_element_by_xpath('descendant::p').get_attribute('title')
            
            print("Scrapping " + title)
            Ratings.get_individual_complain(link, title, enterprise, category, subcategory, subcategory_id)

    # Get a individual complain in the complain's list
    def get_individual_complain(url, title, enterprise, category='', subcategory='', subcategory_id=''):
        try:
            driver_complain = utils.prepare_driver(url)

            # position_in_chat represents control the position in the conversation (if first complain, enterprise's answer, reply, etc)
            position_in_chat = 0
            complain_body = driver_complain.find_element_by_css_selector('#complain-detail .container .complain-body p').text
            
            obj = (enterprise, title, complain_body, position_in_chat, url, category, subcategory, subcategory_id, now)

            database.insert_in_rating(conn, obj)
            
            try:
                '''
                Para casos em que há mais de uma mensagem do consumidor, criar na tabela um campo "posicao",
                em que cada mensagem do consumidor tem uma possível resposta.
                A primeira mensagem é a 0
                e as outras vão seguindo
                '''

                replies = driver_complain.find_elements_by_xpath('//div[@class="reply-content"]')
                for reply in replies:
                    position_in_chat = position_in_chat + 1

                    # a reply_obj is each answer to the posted original complain
                    reply_obj = (enterprise, title, reply.text, position_in_chat, url, category, subcategory, subcategory_id, now)
                    database.insert_in_rating(conn, reply_obj)
            except selenium.common.exceptions.NoSuchElementException:
                pass
        except selenium.common.exceptions.WebDriverException:
            pass
        finally:
            driver_complain.quit()

    def get_reviews_categories(enterprise):
        url = 'https://www.reclameaqui.com.br/empresa/' + enterprise
        driver = utils.prepare_driver(url)

        categories = driver.find_elements_by_css_selector('.fIQOyq .problem-types-cards button')
        
        scrolls = 0
        scroll_height = 200
        i = 0
        while True:
            
            try:
                categories[i].click()
                i = i + 1
            except selenium.common.exceptions.ElementClickInterceptedException:
                driver.execute_script("window.scrollBy(0, " + str(scroll_height) + ");")
                scroll_height = scroll_height + 20
            except selenium.common.exceptions.WebDriverException:
                break
            except IndexError:
                break

        buttons = driver.find_elements_by_xpath('//div[@id="problem-types"]//a')

        super_category = ''
        is_super_category = False
        for b in buttons:
            if b.text == 'Ver tudo':
                continue
            if '%' in b.text:
                super_category = b.text.split('%')[1]
                is_super_category = True
            else:
                is_super_category = False

            link = b.get_attribute("href")
            name = b.text
            code = link.split('lista-reclamacoes/?')[1]

            obj = (name, super_category, code, link, enterprise, is_super_category, now)
            database.insert_in_category(conn, obj)

        driver.quit()

    def get_categorized_reviews(enterprise, n_pages_to_scrape = 3):
        rows = database.get_reviews_categories(conn, enterprise)

        for row in rows:
            (subcategory, category, code) = row

            print("Scrapping subcategory ", + subcategory)
            for page in range(1, n_pages_to_scrape + 1):
                url = Ratings.handle_page(enterprise, code, page)
                print("Scrapping page " + str(page))

                driver = utils.prepare_driver(url)

                if ( Ratings.check_if_end_of_list(driver)):
                    break
                else:
                    Ratings.get_complains_of_list(driver, enterprise, category, subcategory, code)

                driver.quit()
    
    ''' verificar quando a pagina não existe '''

# Set the function as static (a static method is bound to a class rather than the objects for that class)
Ratings.get_reviews = staticmethod(Ratings.get_reviews)
Ratings.check_if_end_of_list = staticmethod(Ratings.check_if_end_of_list)
Ratings.get_complains_of_list = staticmethod(Ratings.get_complains_of_list)
Ratings.get_individual_complain = staticmethod(Ratings.get_individual_complain)
Ratings.get_categorized_reviews = staticmethod(Ratings.get_categorized_reviews)
Ratings.get_reviews_categories = staticmethod(Ratings.get_reviews_categories)