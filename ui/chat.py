import streamlit as st
import requests
import json

def post_data(api_endpoint, data):
    try:
        print('data ', data)
        response = requests.post(api_endpoint, data=json.dumps(data))
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except Exception as e:
        st.error(f"Error occurred: {e}")
        return None

def main():
    st.title("Langchain Chatbot Interface")

    api_endpoint = "http://localhost:9091/chat"


    param1 = st.text_input("Query")
    # param2 = st.slider("Parameter 2", min_value=0, max_value=100, value=50)
    # param3 = st.checkbox("Parameter 3")

    if api_endpoint:
        if st.button("Send"):
            data = {
                "query": str(param1),
                "chat_history": [],
            }

            data = post_data(api_endpoint, data)

            if data:
                st.markdown(data['response']['answer'])
                st.header("Source Documents")
                doc_num_init = 1
                for msg in data['response']['source_documents']:
                    st.markdown(f"""### Document **[{doc_num_init}]**: \n__{msg.get('metadata').get('source')}__\n\n*Page Content:*\n\n```{msg.get('page_content')}```""")
                    doc_num_init += 1

            else:
                st.warning("Failed to fetch data from the API endpoint. Please check the endpoint URL.")

if __name__ == "__main__":
    main()
