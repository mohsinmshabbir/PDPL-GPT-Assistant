import time
from openai import OpenAI
import streamlit as st
from streamlit.components.v1 import html

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

if "edit_message_id" not in st.session_state:
    st.session_state["edit_message_id"] = None  # Message being edited

# Function to submit a message to the assistant
def submit_message(assistant_id, thread_id, user_message):
    response = client.beta.threads.messages.create(thread_id=thread_id, role="user", content=user_message)
    return response.id, client.beta.threads.runs.create(thread_id=thread_id, assistant_id=assistant_id.id)

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

# Function to export the chat to a text file
def export_chat_to_txt(messages):
    chat_text = ""
    for message in messages:
        role = message["role"].capitalize()  # Capitalize role for better readability
        content = message["content"]
        chat_text += f"{role}: {content}\n\n"  # Separate messages with a new line
    return chat_text.strip()  # Remove any trailing whitespace

def modify_message(thread_id, message_id, new_content):
    # 1. Mark the message as modified using metadata
    try:
        client.beta.threads.messages.update(
            message_id=message_id,
            thread_id=thread_id,
            metadata={
                "modified": "true"
            }
        )

        # 2. Update the local message with new content
        for message in st.session_state.messages:
            if message["id"] == message_id:
                message["content"] = new_content
                message["metadata"] = {"modified": "true"}
                break
        st.write("Message modified successfully.")

        # 3. Resubmit the modified message to OpenAI
        run = submit_message(ASSISTANT_ID, thread_id, new_content)
        run = wait_on_run(run, thread_id)
        responses = get_response(thread_id)

        # 4. Append the assistant's response to the session state
        last_assistant_message = responses.data[-1]
        assistant_message_content = last_assistant_message.content[0].text.value

        st.session_state.messages.append({
            "role": "assistant",
            "content": assistant_message_content,
            "id": f"msg_{len(st.session_state.messages)}"
        })
        with st.chat_message("assistant"):
            st.markdown(assistant_message_content)

    except Exception as e:
        st.write(f"Failed to update message: {str(e)}")


# Main chat loop
def chat_loop():

    if "messages" not in st.session_state:
        st.session_state.messages = []

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

    # Display past messages only if there are any
    if st.session_state.messages:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                # Check if the message contains an 'id' before proceeding
                if "id" in message:
                    if message["role"] == "user" and message["id"] != st.session_state.edit_message_id:
                        st.markdown(message["content"])
                        st.button("✏️", key=message["id"], on_click=lambda m=message: st.session_state.update({"edit_message_id": m["id"]}))
                    elif message["role"] == "user" and message["id"] == st.session_state.edit_message_id:
                        # Show an input box for editing the message
                        new_content = st.text_input("Edit your message", value=message["content"])
                        if st.button("Save", key=f"save_{message['id']}"):
                            modify_message(thread_id=st.session_state.thread_id, message_id=message["id"], new_content=new_content)
                            st.session_state.edit_message_id = None  # Reset edit state
                else:
                    st.markdown(message["content"])  # Just display the message if no 'id']

    else:
        st.write("No messages in this thread yet. Start the conversation!")

    # Get new user input
    if prompt := st.chat_input("What is up?"):
        # Submit user message and get assistant's response
        message_id, run = submit_message(assistant, st.session_state.thread_id, prompt)
        st.session_state.messages.append({"role": "user", "content": prompt, "id": message_id})

        with st.chat_message("user"):
            st.markdown(prompt)

        # Wait for assistant response
        run = wait_on_run(run, st.session_state.thread_id)
        responses = get_response(st.session_state.thread_id)

        # Get the latest assistant response and append to session state
        last_assistant_message = responses.data[-1]
        assistant_message_content = last_assistant_message.content[0].text.value
        st.session_state.messages.append({"role": "assistant", "content": assistant_message_content, "id": last_assistant_message.id})

        with st.chat_message("assistant"):
            st.markdown(assistant_message_content)

chat_loop()