import streamlit as st
import pandas as pd

st.set_page_config(page_title="Ingredient Aggregator", layout="wide")

st.title("📦 Universal Batch Calculator")
st.write("Upload your Excel file to combine all sheets into one shopping list.")

uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])

if uploaded_file:
    # Read every sheet in the Excel file
    all_sheets = pd.read_excel(uploaded_file, sheet_name=None)
    combined_data = []

    for name, df in all_sheets.items():
        # Look for columns that might contain ingredients and totals
        # This looks for the word 'Ingredient' or 'Item' and 'Scaled' or 'Final'
        cols = df.columns.tolist()
        item_col = next((c for c in cols if "ingredient" in str(c).lower() or "item" in str(c).lower()), cols[0])
        qty_col = next((c for c in cols if "scaled" in str(c).lower() or "final" in str(c).lower() or "quantity" in str(c).lower()), cols[-1])
        
        subset = df[[item_col, qty_col]].copy()
        subset.columns = ['Ingredient', 'Total']
        combined_data.append(subset)

    # Merge and Sum
    full_df = pd.concat(combined_data)
    full_df['Total'] = pd.to_numeric(full_df['Total'], errors='coerce')
    final_list = full_df.groupby('Ingredient')['Total'].sum().reset_index()
    
    st.dataframe(final_list.sort_values(by='Total', ascending=False))
    
    csv = final_list.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download Master List", csv, "master_list.csv", "text/csv")
