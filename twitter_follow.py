from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import traceback
from selenium.webdriver.common.action_chains import ActionChains

options = Options()
options.add_experimental_option("debuggerAddress", "localhost:9222")

driver = webdriver.Chrome(options=options)

driver.get("https://x.com/home")
    # driver.execute_script("window.scrollBy(0, 500);")
    # time.sleep(3)

start_index = 0
max_scrolls = 2
count = 0

try:
    while max_scrolls > 0:
        elements = WebDriverWait(driver, 60).until(
            lambda e: e.find_elements(By.XPATH, "//div[@data-testid='cellInnerDiv']")
        )

        print(f"Found {len(elements)} elements. Processing from index {start_index} to {len(elements) - 1}")

        for i in range(start_index, len(elements)):
            element = elements[i]
            try:
                caret = element.find_element(By.XPATH, ".//button[@data-testid='caret']")
                print("Page is ready!", caret)
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", caret)
                time.sleep(2)
                caret.click()
                time.sleep(2)

                dropdown = WebDriverWait(driver, 20).until(
                    lambda e: e.find_element(By.XPATH, "//div[@data-testid='Dropdown']")
                )

                print("Dropdown text:", dropdown.text)
                time.sleep(2)

                if "Follow" not in dropdown.text:
                    print("No follow button found in dropdown, skipping...")
                    ActionChains(driver).send_keys(Keys.ESCAPE).perform()
                    time.sleep(3)
                    continue

                follow_button = dropdown.find_element(
                    By.XPATH, ".//div[@role='menuitem'][contains(., 'Follow') and not(contains(., 'Unfollow'))]"
                )

                print("Follow button found:", follow_button.text)
                follow_button.click()

                driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
                time.sleep(3)
                count += 1

            except Exception as e:
                print("Skipping element due to error:", e)
                traceback.print_exc()

        # Scroll down and update starting index
        max_scrolls -= 1
        start_index = len(elements)  # Only process new tweets on next scroll
        driver.execute_script("arguments[0].scrollIntoView(false);", elements[-1])
        print("Scrolled down")
        time.sleep(3)

except Exception as e:
    print("An error occurred:", e)
    traceback.print_exc()

print(f"Total follow actions performed: {count}")





# "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\Personal-space\eternity\chrome-profile"

