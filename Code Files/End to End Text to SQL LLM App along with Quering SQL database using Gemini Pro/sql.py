from dotenv import load_dotenv
load_dotenv()  # load environment variables

import streamlit as st
import os
import pandas as pd
import sqlite3
import google.generativeai as genai

# Configure GenAI key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load Google Gemini Model and provide queries as response
def get_gemini_response(question, prompt):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content([prompt[0], question])
    return response.text.strip()

# Function to retrieve query from the database
def read_sql_query(sql, db):
    conn = sqlite3.connect(db)
    try:
        rows = pd.read_sql_query(sql, conn)
    except Exception as e:
        st.error(f"Error executing query: {e}")
        rows = pd.DataFrame()  # return an empty DataFrame if error occurs
    conn.close()
    return rows

# Define the prompt
prompt = [
    """
    You are an expert in converting English questions to SQL query!
    The SQL database has the name STUDENT and has the following columns - NAME, CLASS, 
    SECTION \n\nFor example,\nExample 1 - How many entries of records are present?, 
    the SQL command will be something like this SELECT COUNT(*) FROM STUDENT ;
    \nExample 2 - Tell me all the students studying in Data Science class?, 
    the SQL command will be something like this SELECT * FROM STUDENT 
    where CLASS="Data Science"; 
    also the sql code should not have ``` in beginning or end and sql word in output
    """
]

# Streamlit App configuration
st.set_page_config(page_title="Gemini App To Retrieve SQL Data")
st.header("Gemini App to Retrieve SQL Data")

# User input and submit button
question = st.text_input("Input: ", key="input")
submit = st.button("Ask the question")

# If submit is clicked
if submit:
    # Get Gemini response and SQL query
    sql_query = get_gemini_response(question, prompt)
    st.write("Generated SQL Query:", sql_query)  # Display the generated SQL query
    response_df = read_sql_query(sql_query, "student.db")
    
    # Display results in a table
    st.subheader("Query Results")
    if not response_df.empty:
        st.dataframe(response_df)  # Dynamically display results as a table
    else:
        st.write("No results found or error in query execution.")
