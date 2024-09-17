import streamlit as st
import pandas as pd
import numpy as np
from io import BytesIO

# Function to reformat phone numbers
def reformat_phone(phone_number):
    phone_str = str(phone_number).strip()  

    if phone_str.startswith('0'):
        return '84' + phone_str[1:]

    # Check if the phone number has exactly 9 digits
    if len(phone_str) == 9 and phone_str.isdigit():
        return str('84' + phone_str)

    return phone_str

def read_xlsx_to_pd(file_path: str) -> pd.DataFrame:
    """
    Reads an Excel file and converts integer values to strings.

    Args:
        file_path (str): Path to the Excel file.

    Returns:
        pd.DataFrame: DataFrame with integer values converted to strings.
    """
    # Read the Excel file into a DataFrame
    df = pd.read_excel(file_path, dtype=str)
    
    for col in df.columns:
        df[col] = df[col].astype(str)

    return df



def save_df_to_xlsx(df):
    """
    Converts the DataFrame to an XLSX file and returns it as a bytes object.
    """
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')
    output.seek(0)
    return output


def add_otp_column(df):
    df['otp'] = [str(np.random.randint(3000, 10000)) for _ in range(len(df))]
    
    cols = df.columns.tolist()
    cols = [cols[0]] + ['otp'] + cols[1:-1]

    df = df[cols]
    
    return df

# App layout
st.title('CSV Phone Number Reformatter')

# Button for uploading file
st.write("Please upload your CSV file using the button below:")

# Upload button
uploaded_file = st.file_uploader("Upload your CSV file", type=["xlsx"], label_visibility="collapsed")

if uploaded_file:
    df = read_xlsx_to_pd(uploaded_file)

    # Check if 'phone' column exists
    if 'phone' in df.columns:
        df['phone'] = df['phone'].apply(reformat_phone)

        df = add_otp_column(df)

        st.write("First 5 row in result", df[:5])

        # Convert DataFrame to CSV
        xlsx = save_df_to_xlsx(df)

        # Button to download the modified file
        st.write("Click the button below to download the modified XLSX file:")
        st.download_button(
            label="Download modified XLSX",
            data=xlsx,
            file_name="modified_phone_numbers.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
    else:
        st.error("The upload file must contain a 'phone' column.")

