import google.generativeai as genai
import pandas as pd
import time
import streamlit as st

# Configure the API key
genai.configure(api_key="AIzaSyCph9QDeLIesEAISH83slBt7gIs-22mjuI")

# Function to load and preview CSV data
def load_excel_data(file_path):
    # Load the CSV file into a DataFrame
    data = pd.read_csv(file_path)
    # Convert the entire DataFrame to a readable string format for the prompt
    data_context = data.to_string(index=False)
    return data_context

# Function to send a request to the model
def send_request(chat, context, question):
    try:
        # Combine context and question into a single prompt
        prompt = f"Here is the data:\n\n{context}\n\nQuestion: {question}"
        response = chat.send_message(prompt)
        return response
    except Exception as e:
        st.error(f"Error occurred: {e}")
        time.sleep(5)  # Wait before retrying
        return None

# Apply custom CSS for theme and visibility
st.markdown(
    """
    <style>
        /* Background and layout styles */
        .main {
            background-color: #e0f7fa;
            color: #263238;
        }
        
        /* Input, file uploader, and button styles */
        .stTextInput > div > div > input,
        .stFileUploader > div > div > div > input {
            background-color: #ffffff;  /* White background for input fields */
            color: #263238;  /* Dark text color */
            border: 1px solid #4db6ac;
        }
        
        /* File uploader text style */
        .stFileUploader > div > label {
            color: #263238; /* Dark text color for file uploader text */
        }

        /* Set text color to black for all elements */
        * {
            color: #263238 !important;
        }

        .stButton > button {
            background-color: #e0f7fa;
            color: #ffffff;
            border-radius: 5px;
        }
        .stButton > button:hover {
            background-color: #e0f7fa;
        }
        
        /* Card style for loaded data */
        .data-card {
            background-color: #f1f8e9;
            padding: 10px;
            border-radius: 8px;
            border: 1px solid #c5e1a5;
            color: #263238;
        }
        
        .question-card {
            background-color: #e8f5e9;
            padding: 10px;
            border-radius: 8px;
            border: 1px solid #81c784;
        }
        
        .response-card {
            background-color: #f3e5f5;
            padding: 10px;
            border-radius: 8px;
            border: 1px solid #ce93d8;
        }
    </style>
    """, unsafe_allow_html=True
)

# Main function to load data, format it, and interact with the user through Streamlit
def ask_model_with_excel(file_path):
    # Load CSV data and format it
    data_context = load_excel_data(file_path)
    
    # Start a chat with the model
    model = genai.GenerativeModel(model_name="gemini-1.5-pro")
    chat = model.start_chat()

    # Streamlit app components
    st.title("📊 AI Assistant for CSV Data Analysis")

    # Display the loaded data preview in a styled card
    st.markdown("### Loaded Data:")
    st.markdown(f"<div class='data-card'>{data_context}</div>", unsafe_allow_html=True)

    # User input for the question
    question = st.text_input("Ask a question about the data:")

    # If the user enters a question
    if question:
        with st.spinner("Fetching answer..."):
            response = send_request(chat, data_context, question)
        
        if response:
            # Extract and display the answer from the model's response
            answer = response.candidates[0].content.parts[0].text
            st.markdown("### Answer:")
            st.markdown(f"<div class='response-card'>{answer}</div>", unsafe_allow_html=True)
        else:
            st.error("No response received.")
    
    # Option to quit (user can close the tab or app to exit)
    if st.button("Quit"):
        st.write("Exiting...")

# Streamlit file uploader component
uploaded_file = st.file_uploader("Upload your CSV file", type="csv")

# Check if the user has uploaded a file
if uploaded_file is not None:
    # Save the uploaded file to a temporary path
    file_path = uploaded_file.name
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    # Call the function to ask questions based on the uploaded CSV data
    ask_model_with_excel(file_path)
else:
    st.info("Please upload a CSV file to get started.")
