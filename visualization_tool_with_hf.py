import os
import streamlit as st
import pdfplumber
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re
from transformers import pipeline

# Load Hugging Face summarization model
@st.cache_resource
def load_summarizer():
    return pipeline("summarization", model="facebook/bart-large-cnn")

summarizer = load_summarizer()

# Function to extract text from PDF using pdfplumber
def extract_text_from_pdf(file):
    try:
        with pdfplumber.open(file) as pdf:
            text = ""
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + " "
        return text
    except Exception as e:
        st.write(f"Error extracting text from PDF: {str(e)}")
        return ""

# Split text into manageable chunks
def split_text_into_chunks(text, max_words=500):
    words = text.split()
    for i in range(0, len(words), max_words):
        yield " ".join(words[i:i + max_words])

# Function to summarize text using Hugging Face
def summarize_text_with_huggingface(text):
    try:
        if not text.strip():
            return "Error: No text to summarize."
        chunks = list(split_text_into_chunks(text))
        summarized_chunks = []
        for chunk in chunks:
            summary = summarizer(chunk, max_length=150, min_length=30, do_sample=False)
            summarized_chunks.append(summary[0]["summary_text"])
        return " ".join(summarized_chunks)
    except Exception as e:
        return f"Error: {str(e)}"

# Enhanced function to extract and process data (including numeric values)
def extract_and_process_data(summarized_text):
    data = {}
    numeric_data = {}
    non_numeric_data = {}
    for line in summarized_text.splitlines():
        if ':' in line:
            key, value = line.split(':', 1)
            data[key.strip()] = value.strip()

            # Extract numeric values
            numeric_value = re.findall(r"[-+]?\d*\.\d+|\d+", value)
            if numeric_value:
                numeric_data[key.strip()] = float(numeric_value[0])
            else:
                non_numeric_data[key.strip()] = value.strip()

    return data, numeric_data, non_numeric_data

# Dynamic explanation generation based on plot type
def generate_plot_explanation(plot_type, data):
    if plot_type == "Line Plot":
        explanation = f"This line plot shows the trends of numeric values across {len(data)} categories. Each point represents a category, and the line highlights changes between them. Use it to identify increases, decreases, or stable patterns."
    elif plot_type == "Pie Chart":
        explanation = f"This pie chart visualizes the proportion of values across {len(data)} categories. Each slice represents a category, and its size reflects its share of the total. Useful for understanding relative contributions."
    elif plot_type == "Histogram":
        explanation = f"This histogram shows the distribution of {len(data)} numeric values. Each bar represents a range (bin), and its height indicates the frequency of values within that range. Ideal for spotting patterns or outliers."
    else:
        explanation = "Visualization explanation not available."
    return explanation

# Function to process and visualize data with dynamic explanations
def process_and_visualize(text):
    try:
        # Extract data without summarizing
        data, numeric_data, non_numeric_data = extract_and_process_data(text)

        # Handle numeric data visualization
        if numeric_data:
            st.write("### Extracted Numeric Data:")
            st.write(numeric_data)

            # Plot the numeric data
            df = pd.DataFrame(list(numeric_data.items()), columns=['Key', 'Value'])
            visualization_type = st.selectbox("Select Visualization Type", ["Pie Chart", "Line Plot", "Histogram"])

            # Set plot size for better visibility
            plt.figure(figsize=(12, 6))  # Larger figure for better resolution

            if visualization_type == "Line Plot":
                plt.plot(df['Key'], df['Value'], marker='o', linestyle='-', color='b')
                plt.xlabel('Category')
                plt.ylabel('Value')
                plt.title('Line Plot - Trends Over Categories')
                plt.xticks(rotation=45, ha='right')
                st.pyplot(plt)

            elif visualization_type == "Pie Chart":
                df = df[df['Value'] > 0]
                if not df.empty:
                    plt.pie(df['Value'], labels=df['Key'], autopct='%1.1f%%', startangle=90)
                    plt.title('Pie Chart - Data Proportions')
                    st.pyplot(plt)

            elif visualization_type == "Histogram":
                plt.hist(df['Value'].dropna(), bins=10, color='skyblue', edgecolor='black')
                plt.xlabel('Value')
                plt.ylabel('Frequency')
                plt.title('Histogram - Distribution of Values')
                st.pyplot(plt)

            # Add dynamic explanation for the selected plot
            explanation = generate_plot_explanation(visualization_type, numeric_data)
            st.write("### Visualization Explanation:")
            st.write(explanation)

        # Handle non-numeric data visualization
        elif non_numeric_data:
            st.write("### Extracted Non-Numeric Data:")
            for key, value in non_numeric_data.items():
                st.write(f"{key}: {value}")
            st.write("This non-numeric data includes descriptive or categorical information from the document.")

        else:
            st.write("No numeric or non-numeric data found to display.")
    except Exception as e:
        st.write(f"Error during processing and visualization: {str(e)}")

# Streamlit App
st.title("PDF and Text Visualization App")

tab1, tab2 = st.tabs(["PDF Visualization", "Text Summarization"])

with tab1:
    st.header("Upload a PDF for Data Visualization")
    uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")
    if uploaded_file is not None:
        if uploaded_file.size > 3 * 1024 * 1024:  # Limit file size to 3MB
            st.write("File size exceeds the 3MB limit. Please upload a smaller file.")
        else:
            st.write("File uploaded successfully!")
            text = extract_text_from_pdf(uploaded_file)
            if text.strip():
                process_and_visualize(text)
            else:
                st.write("Could not extract any readable text from the PDF. Please check the file.")

with tab2:
    st.header("Enter Text for Summarization")
    user_text = st.text_area("Enter your text here:")
    if st.button("Summarize Text"):
        if user_text.strip():
            summarized_text = summarize_text_with_huggingface(user_text)
            st.write("Summarized Text:")
            st.write(summarized_text)
        else:
            st.write("Please enter some text to summarize.")
