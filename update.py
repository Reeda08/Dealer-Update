import os
import time
import pandas as pd
import pyperclip
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

# --- Configuration ---
VISTA_DIR = r"C:\Users\dsajekar\Downloads"
URL = "https://data.findmeacar.in/admincp/master_inventory/get_master_inventory"
USERNAME = "dsarjeka"
PASSWORD = "dsarjeka@jlr123"

# --- Setup WebDriver ---
driver = webdriver.Chrome()
driver.maximize_window()
wait = WebDriverWait(driver, 15)

def login():
    driver.get(URL)
    wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='userid']"))).send_keys(USERNAME)
    wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='password']"))).send_keys(PASSWORD)
    wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='login_btn']"))).click()
    print("✅ Login successful!")

def navigate_to_bulk_to_bulk():
    # Hover and click flow       

    update = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='navbar']/ul[1]/li[4]/a")))
    update.click()
    time.sleep(1)

    bulk_to_bulk = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='navbar']/ul[1]/li[4]/ul/li[3]/a")))
    bulk_to_bulk.click()
    print("✅ Navigated: URL → Update → Bulk to Bulk")

def get_latest_vista_file():
    files = [f for f in os.listdir(VISTA_DIR) if f.startswith("Vista_With_CorrectDealerName_") and f.endswith(".csv")]
    if not files:
        print("❌ No Vista_With_CorrectDealerName_ file found.")
        driver.quit()
        exit()
    files.sort(key=lambda x: os.path.getmtime(os.path.join(VISTA_DIR, x)), reverse=True)
    return os.path.join(VISTA_DIR, files[0])

def extract_data(filepath):
    df = pd.read_csv(filepath, dtype=str).fillna("")
    required_cols = {"Order Number", "Correct Dealer Name", "Destination"}
    if not required_cols.issubset(set(df.columns)):
        print("❌ Required columns missing.")
        driver.quit()
        exit()

    return {
        "order_numbers": df["Order Number"].tolist(),
        "correct_dealers": df["Correct Dealer Name"].tolist(),
        "destinations": df["Destination"].tolist()
    }

def select_dropdowns():
    Select(wait.until(EC.element_to_be_clickable((By.ID, "drop_down1")))).select_by_index(5)   # Current Allocation
    Select(wait.until(EC.element_to_be_clickable((By.ID, "drop_down2")))).select_by_index(46)  # Ordering Dealer
    Select(wait.until(EC.element_to_be_clickable((By.ID, "drop_down3")))).select_by_index(3)   # DLR ID
    print("✅ Dropdowns selected")

def paste_textarea(xpath, data, label):
    textarea = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
    textarea.click()
    pyperclip.copy('\n'.join(data))
    ActionChains(driver).key_down(Keys.CONTROL).send_keys("v").key_up(Keys.CONTROL).perform()
    print(f"✅ Pasted {label}")

def submit_form():
    wait.until(EC.element_to_be_clickable((By.XPATH,"//*[@id='static_value_btn']"))).click()
    print("🚀 Submitted the form. Waiting for confirmation...")

    try:
        success = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'successfully updated')]"))
        )
        print("✅ Update confirmed successfully!")
    except:
        print("⚠️ No confirmation message found.")

# --- MAIN ---
login()
navigate_to_bulk_to_bulk()

vista_file = get_latest_vista_file()
print(f"📄 Using file: {vista_file}")

data = extract_data(vista_file)
select_dropdowns()

paste_textarea("//*[@id='order_number']", data["order_numbers"], "Order Numbers")
paste_textarea("//*[@id='text_area1']", data["correct_dealers"], "Correct Dealer Name (Current Allocation)")
paste_textarea("//*[@id='text_area2']", data["correct_dealers"], "Correct Dealer Name (Ordering Dealer)")
paste_textarea("//*[@id='text_area3']", data["destinations"], "Destination (Dealer ID)")

submit_form()

time.sleep(5)
driver.quit()