import os
import pandas as pd
from datetime import datetime  

download_dir = r"C:\Users\dsajekar\Downloads\FinalStock"

# ✅ Only get StockLocator file (contains 'master_inv_data.csv')
def get_latest_stocklocator_csv(folder):
    stock_files = [f for f in os.listdir(folder) if f.endswith("master_inv_data.csv")]
    if not stock_files:
        return None
    stock_files.sort(key=lambda x: os.path.getmtime(os.path.join(folder, x)), reverse=True)
    return os.path.join(folder, stock_files[0])

def process_stocklocator_csv():
    latest_csv = get_latest_stocklocator_csv(download_dir)
    if latest_csv:
        print(f"📥 Processing StockLocator CSV: {latest_csv}")
        df = pd.read_csv(latest_csv, encoding='utf-8', low_memory=False)
        df.columns = df.columns.str.strip()

        required_columns = ['Cso No', 'BU/LM', 'Current Allocation', 'Ordering Dealer', 'Dealer ID']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            print(f"❌ Required columns missing in CSV: {missing_columns}")
            return
        
        # ✅ Normalize and clean columns
        df['BU/LM'] = df['BU/LM'].astype(str).str.strip().str.upper()
        df['Current Allocation'] = df['Current Allocation'].astype(str).str.strip()

        print("🔍 Unique values in 'BU/LM':", df['BU/LM'].dropna().unique())

        # ✅ Apply both filters: BU + Additional Dealer Stock
        filtered_df = df[
            (df['BU/LM'] == "BU") &
            (df['Current Allocation'].str.contains("Additional Dealer Stock", na=False))
        ]

        print(f"📊 Total rows before filtering: {len(df)}")
        print(f"✅ Total rows after BU + Additional Dealer filtering: {len(filtered_df)}")

        if filtered_df.empty:
            print("⚠️ No matching data found for 'BU' and 'Additional Dealer Stock'.")
            return

        # ✅ Only keep selected columns
        selected_columns = ['Cso No', 'Current Allocation', 'Ordering Dealer', 'Dealer ID']
        final_df = filtered_df[selected_columns]

        # ✅ Save filtered data to one file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S") 
        output_file = os.path.join(download_dir, f"filtered_BU_Additional_Dealer_{timestamp}.csv")
        final_df.to_csv(output_file, index=False)

        print(f"\n✅ Final filtered data saved to:\n{output_file}")
    else:
        print("❌ No StockLocator CSV file found to process.")

# Run the function
process_stocklocator_csv()
print("\n🏁 CSV processing completed!")