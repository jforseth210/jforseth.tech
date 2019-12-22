import time
from selenium import webdriver
driver = webdriver.Firefox()
driver.get(r"http://192.168.1.1")
#Login
username_field = driver.find_element_by_id("user_name_field")
password_field = driver.find_element_by_id("password_field")
login_btn = driver.find_element_by_id("login_btn")

username_field.send_keys("admin")
password_field.send_keys("e6951f5e")
login_btn.click()

#Main Menu
#time.sleep(3)
#advanced_btn=driver.find_element_by_id("nav_advanced")
#advanced_btn.click()

#Port Forwarding
driver.get("http://192.168.1.1/#/html/advanced/security/advanced_security_advancedportforwarding.html")