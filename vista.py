import time
import os
import pandas as pd
import pyperclip
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select

# Define download directory
download_dir = r"C:\Users\dsajekar\Downloads\FinalStock"

# Get the latest filtered BU + Additional Dealer CSV
def get_latest_filtered_csv(folder):
    files = [f for f in os.listdir(folder) if f.startswith("filtered_BU_Additional_Dealer_") and f.endswith(".csv")]
    if not files:
        return None
    files.sort(key=lambda x: os.path.getmtime(os.path.join(folder, x)), reverse=True)
    return os.path.join(folder, files[0])

latest_csv = get_latest_filtered_csv(download_dir)
if latest_csv:
    df = pd.read_csv(latest_csv)
    if 'Cso No' in df.columns:
        cso_numbers = df['Cso No'].dropna().astype(str).tolist()
    else:
        print("'Cso No' column not found in CSV!")
        exit()
else:
    print("No filtered CSV file found!")
    exit()

print("CSO Numbers to be updated:")
print("\n".join(cso_numbers))

# Copy to clipboard
cso_string = '\n'.join(cso_numbers)
pyperclip.copy(cso_string)
print("CSO numbers copied to clipboard!")

# Selenium Automation
url = "https://www.jlrvista.jlrext.com/Vista-NewWeb/rest/HomeController/VIEW/dashboard"

options = webdriver.EdgeOptions()
driver = webdriver.Edge(options=options)

try:
    driver.get(url)
    driver.maximize_window()
    time.sleep(10)

    btn1 = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="bySelection"]/div[2]'))
    )
    btn1.click()
    time.sleep(10)

    advanced_search_btn = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="wrapper"]/div[1]/div/div/div/div/div/div/ul/li[2]/a/span[1]/span/img'))
    )
    advanced_search_btn.click()
    time.sleep(10)

    dropdown = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="collapseOne"]/div/div/div/form/div/table/tbody/tr[2]/td/select'))
    )
    select = Select(dropdown)
    select.select_by_visible_text('Order Number')
    time.sleep(10)

    print("Order Number option selected successfully.")

    textarea = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="collapseOne"]/div/div/div/form/textarea'))
    )
    textarea.click()
    time.sleep(1)

    ActionChains(driver).key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
    print("Pasted CSO numbers into textarea using Ctrl+V")
    time.sleep(10)

    driver.execute_script("arguments[0].scrollIntoView();", textarea)

    search_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="wrapper"]/div[2]/div/div/div[2]/div/div[1]/div[4]/button'))
    )
    ActionChains(driver).move_to_element(search_button).click().perform()
    time.sleep(20)

    specified_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="myNavbar"]/ul/li[2]/a/img'))
    )
    specified_button.click()
    time.sleep(10)

    long_download_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/div[3]/div/div/div/div[2]/div/table[1]/tbody/tr[7]/td[2]/button'))
    )
    long_download_button.click()

    time.sleep(20)

finally:
    driver.quit()