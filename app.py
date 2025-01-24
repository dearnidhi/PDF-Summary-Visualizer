import streamlit as st
import PyPDF2
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re  # For cleaning text

# Function to extract text from PDF using PyPDF2
def extract_text_from_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text += page.extract_text()
    return text

# Function to process and visualize data
def process_and_visualize(text):
    # Convert text into a dictionary (assuming it returns key-value pairs)
    data = {}
    for line in text.splitlines():
        if ':' in line:
            key, value = line.split(':', 1)
            data[key.strip()] = value.strip()

    # Filter out non-numeric 'Value' entries
    numeric_data = {}
    for key, value in data.items():
        # Try to extract numeric values from text using regular expressions
        numeric_value = re.findall(r"[-+]?\d*\.\d+|\d+", value)
        if numeric_value:
            numeric_data[key] = float(numeric_value[0])

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

            # Add legend (though bar plots typically don't have a legend, we can add a label)
            plt.legend(title="Categories", labels=df['Key'].tolist())
            st.pyplot(plt)
            
            # Show key data used for the plot
            st.write("Data used for Bar Plot:")
            st.write(df.head())  # Show top 5 rows of the data
            
            # Explanation with purpose
            st.write(f"Explanation: A bar plot is drawn to visualize the comparison of different categories. "
                     f"In this case, it shows the growth of AUM (Assets Under Management) for various periods, "
                     f"such as: {', '.join(df['Key'].head(5))}.")
        
        elif visualization_type == "Pie Chart":
            plt.figure(figsize=(8, 8))
            plt.pie(df['Value'], labels=df['Key'], autopct='%1.1f%%', startangle=90)
            plt.title('Pie Chart - Data Proportions')
            
            # Add legend
            plt.legend(df['Key'], title="Categories")
            st.pyplot(plt)
            
            # Show key data used for the plot
            st.write("Data used for Pie Chart:")
            st.write(df.head())  # Show top 5 rows of the data
            
            # Explanation with purpose
            st.write(f"Explanation: A pie chart is used to show the relative proportions of categories in the data. "
                     f"In this case, it represents the percentage share of different assets in the portfolio, "
                     f"such as: {', '.join(df['Key'].head(5))}.")
        
        elif visualization_type == "Line Plot":
            plt.figure(figsize=(12, 6))
            plt.plot(df['Key'], df['Value'], label="Value over Categories")
            plt.xlabel('Category')
            plt.ylabel('Value')
            plt.title('Line Plot - Trends Over Categories')

            # Add legend
            plt.legend(title="Value Trend")
            st.pyplot(plt)
            
            # Show key data used for the plot
            st.write("Data used for Line Plot:")
            st.write(df.head())  # Show top 5 rows of the data
            
            # Explanation with purpose
            st.write(f"Explanation: A line plot is used to show trends over time or categories. "
                     f"Here, it shows how the values of categories like {', '.join(df['Key'].head(5))} "
                     f"have changed over time or across different variables.")
        
        elif visualization_type == "Histogram":
            plt.figure(figsize=(12, 6))
            plt.hist(df['Value'].dropna(), bins=10)  # Drop NaN values for histogram
            plt.xlabel('Value')
            plt.ylabel('Frequency')
            plt.title('Histogram - Distribution of Values')

            # Add legend
            plt.legend(["Frequency Distribution"], title="Distribution")
            st.pyplot(plt)
            
            # Show key data used for the plot
            st.write("Data used for Histogram:")
            st.write(df.head())  # Show top 5 rows of the data
            
            # Explanation with purpose
            st.write(f"Explanation: A histogram is used to show the distribution of values within the data. "
                     f"Here, it shows the frequency distribution of asset values like: {', '.join(map(str, df['Value'].head(5)))}.")

    else:
        st.write("No valid data found for visualization.")

# Streamlit App
st.title("PDF Visualization App")

# File uploader
uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

if uploaded_file is not None:
    st.write("File uploaded successfully!")
    text = extract_text_from_pdf(uploaded_file)
    
    # Process and visualize data
    process_and_visualize(text)
else:
    st.write("Please upload a PDF file.")
