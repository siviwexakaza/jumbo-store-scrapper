from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import csv
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)
driver.get("https://online.masscash.co.za/")
stock = []

def wait(seconds):
    time.sleep(seconds)

try:
    #Login and accept terms and conditions
    login_username = driver.find_element_by_class_name("username")
    login_password = driver.find_element_by_id("password")
    login_username.send_keys("email")
    login_password.send_keys("password")
    login_password.send_keys(Keys.ENTER)
    wait(3)
    accept_terms = driver.find_elements_by_xpath("//*[contains(text(), 'Accept Terms')]")
    accept_terms[0].click()
    #end of login

    #steps to get products
    wait(3)
    catalog = driver.find_elements_by_xpath("//*[contains(text(), 'Catalogue')]")
    catalog[0].click()

    products = driver.find_elements_by_xpath("//*[contains(text(), 'Products')]")
    products[0].click()

    wait(5)
    items = driver.find_elements_by_tag_name("tr")
    

    for item in items:
        tds = item.find_elements_by_tag_name("td")
        product = {}
        for i, td in enumerate(tds):
            if i == 0:
              product["productCode"] = td.text
            elif i == 2:
                product["description"] = td.text
            elif i == 3:
                product["sellingPrice"] = td.text
            elif i == 4:
                product["unitSize"] = td.text
            elif i == 6:
                product["stockOnHand"] = td.text
            elif i == 7:
                product["taxable"] = td.text

        stock.append(product)
        
    
    fname = "output.csv"
    with open(fname,"w") as f:
        fieldnames = ["productCode","description","sellingPrice","unitSize","stockOnHand","taxable"]
        writer = csv.DictWriter(f,fieldnames=fieldnames)
        writer.writeheader()

        for s in stock:
            writer.writerow(s)
            
    
    print("CSV created")

except Exception as e:
    print(e)
    driver.quit()
wait(3)
driver.quit()