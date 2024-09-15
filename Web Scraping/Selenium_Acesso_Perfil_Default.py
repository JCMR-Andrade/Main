from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd

chrome_options = Options()
chrome_options.add_argument("user-data-dir=C:\\Users\\HP\\AppData\\Local\\Google\\Chrome\\User Data")
chrome_options.add_argument("--profile-directory=Default") 
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)

time.sleep(8)

driver.get("https://linkedin.com.br/")
time.sleep(20)

pd.read_excel()
