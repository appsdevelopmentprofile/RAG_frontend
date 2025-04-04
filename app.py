import streamlit as st
import requests
import json
from langchain.chat_models import ChatDatabricks

# Databricks API and model details
DATABRICKS_HOST = "https://dbc-e594eadf-a63a.cloud.databricks.com"
DATABRICKS_TOKEN = "dapib1af9d7c614db5bc8a6a923002cba7f0"
ENDPOINT = "dbdemos_endpoint_main_rag_chatbot"
MODEL = "workspace.rag_sagd_papers.dbdemos_chatbot_model"
chat_model = ChatDatabricks(endpoint=ENDPOINT)

# Set up Streamlit page
st.set_page_config(page_title="RAG Lakehouse Search", layout="wide")
st.title("🔍 RAG Lakehouse Search")

# User input for query
user_query = st.text_input("Ask a question about the SAGD repository:", "Which SAGD techniques are currently being used in these papers?")

if user_query:
    try:
        # Query the model with the user input
        response = chat_model.predict(user_query, max_tokens=200)
        st.subheader("💡 Model Answer")
        st.write(response)
    except Exception as e:
        # Display error message if the model call fails
        st.error(f"❌ Error: {str(e)}")

# Search button to query Databricks API
if st.button("Search"):
    with st.spinner("Retrieving information..."):
        headers = {
            "Authorization": f"Bearer {DATABRICKS_TOKEN}",
            "Content-Type": "application/json"
        }
        
        # Send the query from user input
        payload = json.dumps({"query": user_query})
        
        # Request the data from Databricks model
        response = requests.post(
            f"{DATABRICKS_HOST}/serving-endpoints/{ENDPOINT}/invocations", 
            headers=headers, 
            data=payload
        )
        
        if response.status_code == 200:
            result = response.json()
            retrieved_docs = result.get("retrieved_documents", [])
            answer = result.get("response", "No answer available.")
            
            # Display answer
            st.subheader("💡 Model Answer")
            st.write(answer)
            
            # Display retrieved documents
            st.subheader("📄 Relevant Documents")
            for i, doc in enumerate(retrieved_docs):
                st.markdown(f"**{i+1}.** {doc}")
        else:
            st.error("❌ Failed to retrieve response from Databricks model.")
