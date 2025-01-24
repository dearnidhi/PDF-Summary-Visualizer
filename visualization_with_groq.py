import os
import streamlit as st
import PyPDF2
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re
from groq import Groq  # Assuming you have the Groq client installed



# Groq API Key
GROQ_API_KEY = ""  # Your provided API key

# Initialize the Groq client with your API key
client = Groq(api_key=GROQ_API_KEY)  # Directly passing the API key to the client

# Function to extract text from PDF using PyPDF2
def extract_text_from_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text += page.extract_text()
    return text

# Function to summarize text using Groq API (with Groq client)
def summarize_text_with_groq(text):
    try:
        chat_completion = client.chat.completions.create(
            messages=[{
                "role": "user", 
                "content": f"Summarize the following text: {text}"
            }],
            model="llama-3.3-70b-versatile",  # Use appropriate model
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

# Function to process and visualize data
def process_and_visualize(text):
    # Use Groq for text summarization
    summarized_text = summarize_text_with_groq(text)
    st.write("Summarized Text:")  
    st.write(summarized_text)  # Display summarized text

    # Convert summarized text into a dictionary (assuming it returns key-value pairs)
    data = {}
    for line in summarized_text.splitlines():
        if ':' in line:
            key, value = line.split(':', 1)
            data[key.strip()] = value.strip()

    st.write("Extracted Data:")  # Check the key-value pairs
    st.write(data)

    # Filter out non-numeric 'Value' entries
    numeric_data = {}
    for key, value in data.items():
        # Try to extract numeric values using regular expressions
        numeric_value = re.findall(r"[-+]?\d*\.\d+|\d+", value)
        if numeric_value:
            numeric_data[key] = float(numeric_value[0])

    st.write("Numeric Data:")  # Check the numeric data extracted
    st.write(numeric_data)

    # Convert to DataFrame
    df = pd.DataFrame(list(numeric_data.items()), columns=['Key', 'Value'])

    # Check if DataFrame is empty and handle visualizations
    if not df.empty and df['Value'].notna().any():
        # Visualization options
        visualization_type = st.selectbox("Select Visualization Type", ["Bar Plot", "Pie Chart", "Line Plot", "Histogram"])

        # Generate Plot based on Visualization Type
        if visualization_type == "Bar Plot":
            plt.figure(figsize=(12, 6))
            sns.barplot(x='Key', y='Value', data=df)
            plt.xticks(rotation=45, ha='right')  # Rotate and align labels properly
            plt.title('Bar Plot - Data Visualization')
            st.pyplot(plt)
        
        elif visualization_type == "Pie Chart":
            # Check if there are any non-positive values and filter them out
            df = df[df['Value'] > 0]

            # Ensure that there are still valid values after filtering
            if not df.empty:
                plt.figure(figsize=(8, 8))
                plt.pie(df['Value'], labels=df['Key'], autopct='%1.1f%%', startangle=90)
                plt.title('Pie Chart - Data Proportions')
                st.pyplot(plt)
        
        elif visualization_type == "Line Plot":
            plt.figure(figsize=(12, 6))
            plt.plot(df['Key'], df['Value'], label="Value over Categories")
            plt.xlabel('Category')
            plt.ylabel('Value')
            plt.title('Line Plot - Trends Over Categories')
            st.pyplot(plt)
        
        elif visualization_type == "Histogram":
            plt.figure(figsize=(12, 6))
            plt.hist(df['Value'].dropna(), bins=10)  # Drop NaN values for histogram
            plt.xlabel('Value')
            plt.ylabel('Frequency')
            plt.title('Histogram - Distribution of Values')
            st.pyplot(plt)

    else:
        st.write("No valid data found for visualization.")

# Streamlit App
st.title("PDF and Text Summarization App with Groq API")

# Tab structure for different functionalities
tab1, tab2 = st.tabs(["PDF Visualization", "Text Summarization"])

# PDF Summarization Tab
with tab1:
    st.header("Upload a PDF for Summarization and Visualization")
    uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")
    if uploaded_file is not None:
        st.write("File uploaded successfully!")
        text = extract_text_from_pdf(uploaded_file)
        process_and_visualize(text)
    else:
        st.write("Please upload a PDF file.")

# Text Summarization Tab
with tab2:
    st.header("Enter Text for Summarization")
    user_text = st.text_area("Enter your text here:")
    if st.button("Summarize Text"):
        if user_text.strip():
            summarized_text = summarize_text_with_groq(user_text)
            st.write("Summarized Text:")
            st.write(summarized_text)
        else:
            st.write("Please enter some text to summarize.")
