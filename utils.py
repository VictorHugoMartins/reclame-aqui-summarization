
import selenium
from selenium import webdriver
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

def prepare_driver(url):
	for atempt in range(0, 10):
		try:
			options = Options()
			binary = FirefoxBinary('C:\\Program Files\\Mozilla Firefox\\firefox.exe')
			driver = webdriver.Firefox(firefox_binary=binary, executable_path=r'C:\\geckodriver.exe', options=options)
			driver.get(url)
			wait = WebDriverWait(driver, 10)
			return driver
		except:
			continue

