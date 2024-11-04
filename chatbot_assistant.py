import time
from openai import OpenAI
import streamlit as st

# Assistant ID (can be a hard-coded ID)
ASSISTANT_ID = 'asst_7Edb8yE5trutp3qXbOeWoPm4'
# Create an OpenAI client
client = OpenAI(api_key="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")

# Initialize Streamlit app
st.set_page_config(page_title="KSA PDPL",
                   page_icon="🕵️")
st.title("ChatGPT-KSA PDPL")
st.subheader("Making Compliance Easy")

# Initialize session state variables if not already set
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4o-mini"

if "messages" not in st.session_state:
    st.session_state["messages"] = []

if "thread_id" not in st.session_state:
    st.session_state["thread_id"] = None  # Store thread ID for continuity

# Function to submit a message to the assistant
def submit_message(assistant_id, thread_id, user_message):
    client.beta.threads.messages.create(thread_id=thread_id, role="user", content=user_message)
    return client.beta.threads.runs.create(thread_id=thread_id, assistant_id=assistant_id.id)

# Function to get a response from the assistant
def get_response(thread_id):
    return client.beta.threads.messages.list(thread_id=thread_id, order="asc")

# Function to wait for the assistant's response with a spinner
def wait_on_run(run, thread_id):
    with st.spinner('Assistant is typing...'):
        while run.status == "queued" or run.status == "in_progress":
            # Check run status
            run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)
            time.sleep(0.1)  # Sleep briefly to avoid overwhelming the API
    return run

# Function to clear the chat
def clear_chat(thread_id):
    st.session_state.messages = []
    client.beta.threads.delete(thread_id)
    st.session_state.thread_id = None  # Reset thread ID when chat is cleared

def export_chat_to_txt(messages):
    chat_text = ""
    for message in messages:
        role = message["role"].capitalize()  # Capitalize role for better readability
        content = message["content"]
        chat_text += f"{role}: {content}\n\n"  # Separate messages with a new line

    return chat_text.strip()  # Remove any trailing whitespace

# Main chat loop
def chat_loop():
    if st.session_state.thread_id is None:
        # Create new assistant and thread if not already set
        assistant = client.beta.assistants.retrieve(ASSISTANT_ID)
        thread = client.beta.threads.create()
        st.session_state.thread_id = thread.id  # Store thread ID in session state
    else:
        # Fetch assistant and thread from session state
        assistant = client.beta.assistants.retrieve(ASSISTANT_ID)
        thread_id = st.session_state.thread_id

    # Clear Chat Button in the Sidebar (fixed position)
    with st.sidebar:
        if st.button("Clear Chat"):
            clear_chat(thread_id)
        if st.button("Export Chat"):
            chat_text = export_chat_to_txt(st.session_state.messages)
            st.download_button("Download Chat", chat_text, "chat.txt")

    # Display past messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Get new user input
    if prompt := st.chat_input("What is up?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Submit user message and get assistant's response
        run = submit_message(assistant, st.session_state.thread_id, prompt)
        run = wait_on_run(run, st.session_state.thread_id)
        responses = get_response(st.session_state.thread_id)

        # Get the latest assistant response and append to session state
        last_assistant_message = responses.data[-1]
        # Update this line to access the content correctly
        assistant_message_content = last_assistant_message.content[0].text.value

        st.session_state.messages.append({"role": "assistant", "content": assistant_message_content})
        with st.chat_message("assistant"):
            st.markdown(assistant_message_content)

chat_loop()
