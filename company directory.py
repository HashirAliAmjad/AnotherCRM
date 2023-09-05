from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import openpyxl
import time
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configure Chrome options
chrome_options = Options()
chrome_options.add_argument("--incognito")
chrome_options.binary_location = "C:\Program Files\Google\Chrome\Application\chrome.exe"

# Provide the path to the ChromeDriver executable
driver = webdriver.Chrome(options=chrome_options)

wb = openpyxl.load_workbook('C:\\Users\\jorda\\OneDrive\\Desktop\\uslinks.xlsx')
sh1 = wb['Sheet1']

# Set your LinkedIn credentials
username = 'hashirpc60@gmail.com'
password = 'Xav58678'

'''
driver.get('https://www.linkedin.com/directory/companies')
driver.implicitly_wait(5)



#Clicking sign in
si=driver.find_element(By.CSS_SELECTOR,'button[class="authwall-join-form__form-toggle--bottom form-toggle"]')
si.click()
driver.implicitly_wait(5)



# Find the username and password input fields, and enter your credentials
username_field = driver.find_element(By.ID, "session_key")
username_field.send_keys(username)

password_field = driver.find_element(By.ID, "session_password")
password_field.send_keys(password)

# Submit the login form
password_field.send_keys(Keys.RETURN)
driver.implicitly_wait(5)
'''
ro=0
driver.get('https://www.google.com/')
search_input = driver.find_element(By.NAME,"q")   
search_input.send_keys("What is linkedin company directory")   
search_input.send_keys(Keys.RETURN)
# Find the first search result and open it
first_result = driver.find_element(By.CSS_SELECTOR,'a[jsname="qOiK6e"]')
first_result.click()
driver.implicitly_wait(5)
time.sleep(4)

#In this loop you put abc 
for u in range(1,25):
    #Finding a and clicking it
    alpha=driver.find_element(By.CSS_SELECTOR,'ol[class="pagination-links__list"]')
    alpha=driver.find_elements(By.CSS_SELECTOR,'a[class="pagination-links__link"]')
    alpha[u].click()
    driver.implicitly_wait(5)
    time.sleep(3)
    
    lp=driver.find_element(By.XPATH,'//*[@id="main-content"]/div/ol')
    lp=lp.find_elements(By.TAG_NAME,'li')
    leng=len(lp)
    
    for j in range(0,leng):
        time.sleep(1)
        src=driver.find_element(By.XPATH,'//*[@id="main-content"]/ol/li[1]/a')
        driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });", src)
        time.sleep(2)
        lp=driver.find_element(By.XPATH,'//*[@id="main-content"]/div/ol')
        lp=lp.find_elements(By.TAG_NAME,'li')
        lpi=lp[j]
        lpi=lpi.find_element(By.CSS_SELECTOR,'a[class="pagination-links__link"]')
        lpi.click()
        driver.implicitly_wait(10)
        time.sleep(1)
        
        #finding links and pasting it excel
        ul=driver.find_elements(By.CSS_SELECTOR,'li[class="listings__entry"]')
        for i, lin in enumerate(ul):
            lini=lin.find_element(By.CSS_SELECTOR,'a[class="listings__entry-link"]')
            link_url = lini.get_attribute("href")
            print(link_url)
            
            # Write the link URL to the Excel file
            sh1.cell(row=ro+1, column=1, value=link_url)
            ro=ro+1           
        wb.save('C:\\Users\\jorda\\OneDrive\\Desktop\\uslinks.xlsx')    

    
    
    
    
    
    
    
    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    