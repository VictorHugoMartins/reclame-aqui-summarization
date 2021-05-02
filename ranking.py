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

conn = sqlite3.connect('database.db')  # You can create a new database by changing the name within the quotes
now = datetime.now().strftime("%B %d, %Y %I:%M%p")

class Ranking():
    def get_ranking():
        driver = utils.prepare_driver('https://www.reclameaqui.com.br/ranking')
        columns = driver.find_elements_by_class_name('box-gray')
        
        for column in columns:
            category = column.find_element_by_xpath('h2[@class="ng-binding"]')
            day = column.find_element_by_xpath('p[@class="ng-binding"]')
            
            get_enterprises(column, category.text, day.text)

        driver.quit()

    def get_enterprises(column, category, day):
        enterprises = column.find_elements_by_xpath('descendant::ol/li')
        
        position = 1
        for enterprise in enterprises:
            this_one = enterprise.find_element_by_xpath('descendant::a[@class="business-name ng-binding ng-scope"]')
            name = this_one.get_attribute('title')
            category_percentage = this_one.find_element_by_xpath('span').text
            
            obj = (category, name, category_percentage, position, day, now)
            database.insert_in_ranking(conn, obj)
            position = position + 1

Ranking.get_ranking = staticmethod(Ranking.get_ranking)
Ranking.get_enterprises = staticmethod(Ranking.get_enterprises)