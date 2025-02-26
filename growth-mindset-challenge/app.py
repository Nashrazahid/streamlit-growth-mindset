import streamlit as st
import pandas as pd
import os
from io import BytesIO
import random

st.set_page_config(page_title="Data Sweeper", layout="wide")
st.title("FileFlow 🌊 ")

motivational_quotes = [
    "Empower Your Data, Empower Your Decisions!",
    "Transform Data, Transform Insights!",
    "Every Dataset Tells a Story—Make Yours Count!",
    "Clean Data, Clear Insights, Better Decisions!",
    "Turn Raw Data into Meaningful Insights!"
]

st.write(random.choice(motivational_quotes))

uploaded_files = st.file_uploader("Upload your files (CSV or Excel):", type=["csv", "xlsx"], accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()
        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"Unsupported file type: {file_ext}")
            continue

        st.write(f"**File Name:** {file.name}")
        st.write(f"**File Size:** {file.size / 1024:.2f} KB")

        st.write("Preview the Head of the DataFrame")
        st.dataframe(df.head())

        st.subheader("Data Cleaning Options")
        if st.checkbox(f"Clean Data for {file.name}"):
            col1, col2 = st.columns(2)
            with col1:
                if st.button(f"Remove Duplicates from {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write("Duplicates Removed")
            with col2:
                if st.button(f"Fill Missing Values for {file.name}"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write("Missing values have been filled!")

        st.subheader("Select Columns to Convert")
        columns = st.multiselect(f"Choose columns for {file.name}", df.columns, default=df.columns)
        df = df[columns]

        st.subheader("Data Visualization")
        if st.checkbox(f"Show Visualization for {file.name}"):
            st.bar_chart(df.select_dtypes(include='number').iloc[:, :2])

        st.subheader("🔁 Conversion Options")
        conversion_type = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=file.name)
        if st.button(f"Convert {file.name}"):
            buffer = BytesIO()
            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
                file_name = file.name.replace(file_ext, ".csv")
                mime_type = "text/csv"
            else:
                df.to_excel(buffer, index=False)
                file_name = file.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            buffer.seek(0)
            st.download_button(
                label=f"📥 Download {file.name} as {conversion_type}",
                data=buffer,
                file_name=file_name,
                mime=mime_type
            )

else:
    st.subheader("No File? Create Your Own Dataset")
    categories = {
        "Sales": ["Date", "Customer Name", "Product", "Quantity", "Price"],
        "HR": ["Employee ID", "Name", "Department", "Salary"],
        "Finance": ["Transaction ID", "Amount", "Category", "Date"],
        "E-Commerce": ["Order ID", "Customer Name", "Product Name", "Category", "Price", "Quantity", "Order Date", "Shipping Address"]
    }
    selected_category = st.selectbox("Select a Category", list(categories.keys()))
    fields = categories[selected_category]
    
    st.write("Fields for Selected Category:")
    field_values = {field: st.text_input(field) for field in fields}
    
    if st.button("Generate CSV"):
        df = pd.DataFrame([field_values])
        buffer = BytesIO()
        df.to_csv(buffer, index=False)
        buffer.seek(0)
        st.download_button(
            label="📥 Download Generated CSV",
            data=buffer,
            file_name=f"{selected_category}.csv",
            mime="text/csv"
        )
