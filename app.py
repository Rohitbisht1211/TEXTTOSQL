from dotenv import load_dotenv
import streamlit as st
import os
import sqlite3
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Debugging: Check if API Key is loaded
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    st.error("❌ GOOGLE_API_KEY is not set! Please check your environment variables.")
    st.stop()  # Stop execution if API Key is missing

# Configure API Key
genai.configure(api_key=api_key)

# Function to load Google Gemini model and generate SQL query
def get_gemini_response(question, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([prompt[0], question])
    
    # Clean up the response (remove ```sql and unnecessary formatting)
    cleaned_response = response.text.replace("```sql", "").replace("```", "").strip()
    
    return cleaned_response  # Return clean SQL query

# Function to retrieve data from SQLite database
def read_sql_query(sql, db):
    conn = sqlite3.connect(db)
    cur = conn.cursor()

    try:
        cur.execute(sql)
        rows = cur.fetchall()  # Fetch results
    except sqlite3.Error as e:
        conn.close()
        return f"❌ SQL Error: {e}"

    conn.close()
    return rows


# Define prompt for Gemini
prompt = [
    """
    You are an expert in converting English questions to SQL queries! 
    The SQL database has the name STUDENT and has the following columns: 
    NAME, CLASS, SECTION, and MARKS. 

    Examples:
    - "How many entries are present?" → `SELECT COUNT(*) FROM STUDENT;`
    - "Tell me all students in Data Science class?" → `SELECT * FROM STUDENT WHERE CLASS = 'Data Science';`

    ⚠️ **Rules**:
    - **Do not** include `'''` at the beginning or end of the SQL output.
    - **Do not** include the word `SQL` in the output.
    - If asked for the second-highest marks in each class, use this query:

    ```
    SELECT NAME, CLASS, MARKS 
    FROM STUDENT S1
    WHERE (
        SELECT COUNT(*) 
        FROM STUDENT S2 
        WHERE S2.CLASS = S1.CLASS AND S2.MARKS > S1.MARKS
    ) = 1;
    ```

    This query finds the student with the **second-highest marks per class** and works on all SQLite versions.
    """
]

# Streamlit UI
st.set_page_config(page_title="I can Retrieve Any SQL Query")
st.header("App To Retrieve SQL Data Using Text")

# Input Field
question = st.text_input("Enter your question:", key="input")
submit = st.button("Ask the question")

# If submit button is clicked
if submit:
    # Generate SQL query
    response = get_gemini_response(question, prompt)
    st.subheader("🔍 Generated SQL Query:")
    st.code(response, language="sql")  # Show SQL query properly formatted

    # Fetch data from SQLite
    data = read_sql_query(response, "student.db")

    # Display results
    if isinstance(data, str):  # If error occurs
        st.error(data)
    elif len(data) == 0:
        st.warning("⚠️ No records found in the database.")
    else:
        st.subheader("📊 Query Results:")
        st.write(data)  # Display table results
