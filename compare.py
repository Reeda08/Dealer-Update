import os
import pandas as pd
from datetime import datetime

# --- File Paths ---
vista_download_dir = r"C:\Users\dsajekar\Downloads"
stocklocator_dir = r"C:\Users\dsajekar\Downloads\FinalStock"

# --- Get latest filtered Vista file ---
def get_latest_filtered_vista(folder):
    files = [f for f in os.listdir(folder) if f.startswith("Filtered_Vista_Status_") and f.endswith(".csv")]
    if not files:
        return None
    files.sort(key=lambda f: os.path.getmtime(os.path.join(folder, f)), reverse=True)
    return os.path.join(folder, files[0])

# --- Get latest StockLocator file ---
def get_latest_stock_file(folder):
    files = [f for f in os.listdir(folder) if f.endswith("master_inv_data.csv")]
    if not files:
        return None
    files.sort(key=lambda f: os.path.getmtime(os.path.join(folder, f)), reverse=True)
    return os.path.join(folder, files[0])

# --- Load files ---
vista_file = get_latest_filtered_vista(vista_download_dir)
if not vista_file:
    print("❌ No filtered Vista file found.")
    exit()

stock_file = get_latest_stock_file(stocklocator_dir)
if not stock_file:
    print("❌ No StockLocator file found.")
    exit()

print(f"📥 Reading Vista file: {vista_file}")
print(f"📥 Reading StockLocator file: {stock_file}")

vista_df = pd.read_csv(vista_file, dtype=str)
stock_df = pd.read_csv(stock_file, dtype=str)

vista_df.columns = vista_df.columns.str.strip()
stock_df.columns = stock_df.columns.str.strip()

# --- Validate required columns ---
if "Destination" not in vista_df.columns:
    print("❌ 'Destination' column not found in Vista file.")
    exit()

if "Dealer ID" not in stock_df.columns or "Current Allocationr" not in stock_df.columns:
    print("❌ 'Dealer ID' or 'Current Allocation' column missing in StockLocator file.")
    exit()

# --- Drop duplicates to avoid mismatched names ---
stock_lookup = stock_df[["Dealer ID", "Current Allocation"]].drop_duplicates(subset="Dealer ID")

# --- Map Destination → Correct Dealer Name ---
dealer_map = dict(zip(stock_lookup["Dealer ID"], stock_lookup["Current Allocation"]))
vista_df.insert(
    vista_df.columns.get_loc("Destination") + 1,
    "Correct Dealer Name",
    vista_df["Destination"].map(dealer_map)
)

# --- Save updated Vista file ---
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
output_file = os.path.join(vista_download_dir, f"Vista_With_CorrectDealerName_{timestamp}.csv")
vista_df.to_csv(output_file, index=False)

print(f"✅ 'Correct Dealer Name' column added next to 'Destination'")
print(f"📁 Final file saved at: {output_file}")