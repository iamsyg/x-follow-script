from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import traceback

options = Options()
options.add_experimental_option("debuggerAddress", "localhost:9222")

driver = webdriver.Chrome(options=options)

driver.get("https://x.com/home")

try:

    elements = WebDriverWait(driver, 60).until(
        lambda e: e.find_elements(By.XPATH, "//div[@data-testid='cellInnerDiv']")
    )

    for element in elements:
        caret = element.find_element(By.XPATH, ".//button[@data-testid='caret']")
        print("Page is ready!", caret)
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", caret)
        time.sleep(1)
        caret.click()
        time.sleep(5)


        dropdown = WebDriverWait(driver, 20).until(
            lambda e: e.find_element(By.XPATH, ".//div[@data-testid='Dropdown']")
        )

        print("Follow button found and clicked:", dropdown.text)
        time.sleep(5)

        follow_button = dropdown.find_element(
            By.XPATH, ".//div[@role='menuitem'][contains(., 'Follow') and not(contains(., 'Following'))]"
        )

        print("Follow button found:", follow_button.text)
        follow_button.click()

        body = driver.find_element(By.TAG_NAME, "body")
        body.send_keys(Keys.ESCAPE)
        time.sleep(3)
        driver.execute_script("window.scrollBy(0, 500);")
        time.sleep(3)

except Exception as e:
    print("An error occurred:", e)
    traceback.print_exc()

    





# "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\Personal-space\eternity\chrome-profile"

