from selenium import webdriver
import time

lien = "https://ville-data.com/chomage/Besancon-25-25056"

#navigateur = webdriver.Chrome(executable_path="chromedriver.exe")
navigateur = webdriver.Firefox(executable_path="geckodriver.exe")
navigateur.maximize_window()
navigateur.get(lien)

navigateur.execute_script("window.scrollTo(0, 800);")
time.sleep(2)
navigateur.find_elements_by_class_name("google-visualisation-table-page-next").click()