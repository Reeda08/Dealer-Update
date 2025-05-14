import os
import time
import zipfile
import subprocess
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ✅ Tera manually set download path (as you gave)
download_dir = r"C:\Users\dsajekar\Downloads\FinalStock"

# ✅ Create the folder if it doesn't exist
os.makedirs(download_dir, exist_ok=True)
print(f"📁 Files will download here: {download_dir}")

# ✅ Chrome options to set download directory
options = webdriver.ChromeOptions()
prefs = {
    "download.default_directory": download_dir,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True
}
options.add_experimental_option("prefs", prefs)

# ✅ Login URL and credentials
url = "https://data.findmeacar.in/admincp/master_inventory/get_master_inventory"
username = "dsarjeka"
password = "dsarjeka@jlr123"

# ✅ Start Chrome driver
driver = webdriver.Chrome(options=options)
driver.maximize_window()
driver.get(url)

wait = WebDriverWait(driver, 10)

try:
    username_field = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='userid']")))
    username_field.send_keys(username)

    password_field = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='password']")))
    password_field.send_keys(password)

    login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='login_btn']")))
    login_button.click()
    print("✅ Logged in successfully.")

    view_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='navbar']/ul[1]/li[2]")))
    view_button.click()
    print("✅ View button clicked.")

    inventory_file = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Inventory File')]")))
    inventory_file.click()
    print("✅ Inventory file link clicked.")

    download_file = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/h1/a[3]")))
    download_file.click()
    print("⬇️ Download started.")

    time.sleep(3)
    driver.minimize_window()

except Exception as e:
    print(f"⚠️ Error during automation steps: {e}")

# ✅ Wait for the downloaded file
def wait_for_download(folder, extension, timeout=60):
    start_time = time.time()
    while time.time() - start_time < timeout:
        files = [f for f in os.listdir(folder) if f.endswith(extension)]
        if files:
            files.sort(key=lambda x: os.path.getmtime(os.path.join(folder, x)), reverse=True)
            return os.path.join(folder, files[0])
        time.sleep(2)
    return None

# ✅ Extract ZIP file
latest_zip = wait_for_download(download_dir, ".zip")

if latest_zip:
    print(f"✅ Downloaded ZIP File: {latest_zip}")
    try:
        with zipfile.ZipFile(latest_zip, 'r') as zip_ref:
            zip_ref.extractall(download_dir)
        print(f"✅ ZIP extracted to: {download_dir}")
        subprocess.Popen(f'explorer "{download_dir}"')
    except Exception as e:
        print(f"⚠️ Error extracting ZIP: {e}")
else:
    print("❌ No ZIP file found in download folder.")

# ✅ Check for latest CSV after extraction
latest_csv = wait_for_download(download_dir, ".csv")
if latest_csv:
    print(f"📄 Found CSV File: {latest_csv}")
else:
    print("❌ No CSV file found after extraction.")

time.sleep(3)