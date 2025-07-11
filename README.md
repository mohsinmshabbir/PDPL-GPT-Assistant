# KSA PDPL GPT Assistant
[![Ask DeepWiki](https://devin.ai/assets/askdeepwiki.png)](https://deepwiki.com/mohsinmshabbir/PDPL-GPT-Assistant)

This repository hosts a specialized chatbot designed to answer questions about the Kingdom of Saudi Arabia's (KSA) Personal Data Protection Law (PDPL). Built with the OpenAI Assistants API and a Streamlit frontend, it serves as an interactive tool to help users understand and navigate PDPL compliance requirements.

## Snapshot
<img width="1915" height="1065" alt="image" src="https://github.com/user-attachments/assets/36e43425-f82d-4d98-b257-b5537f01a9ec" />


## Features

*   **Specialized Knowledge:** The assistant is configured to act as a Data Governance and Privacy Consultant specializing in KSA PDPL.
*   **Context-Aware Responses:** If a user refers to an article without specifying a law, the assistant defaults to the KSA "Personal Data Protection Law".
*   **Interactive Guidance:** Suggests relevant follow-up questions to help users explore technical topics and related articles.
*   **Chat History Management:** Allows users to clear the current conversation or export the entire chat to a `.txt` file for documentation.

## How It Works

The application architecture consists of a user-facing frontend and a powerful backend:

*   **Frontend:** A web interface built with Streamlit (`chatbot_assistant.py`) captures user input and displays the conversation.
*   **Backend:** An OpenAI Assistant is configured with a specific persona, instructions, and knowledge base. The instructions in `instructions_for_assistant.txt` guide the assistant's behavior, ensuring responses are accurate, focused on data privacy, and helpful.

When a user sends a message, Streamlit forwards it to the OpenAI Assistant, which processes the query based on its instructions and returns a tailored response.

## Getting Started

Follow these instructions to set up and run the application locally or with Docker.

### Prerequisites

*   Python 3.12+
*   An OpenAI API Key.
*   Docker (for containerized deployment)

### Configuration

Before running the application, you need to configure it with your own OpenAI credentials.

1.  **Create an OpenAI Assistant:**
    *   Go to the [OpenAI Assistants page](https://platform.openai.com/assistants).
    *   Create a new Assistant.
    *   For the **Instructions**, copy and paste the content from `instructions_for_assistant.txt`.
    *   Choose a model (e.g., `gpt-4o-mini`).
    *   Save the Assistant and copy its **Assistant ID** (e.g., `asst_...`).

2.  **Update the Source Code:**
    *   Open `chatbot_assistant.py` in a text editor.
    *   Replace the placeholder `ASSISTANT_ID` with your new Assistant ID.
    *   Replace the placeholder `api_key` with your OpenAI API key.

    ```python
    # chatbot_assistant.py

    # Replace with your Assistant ID
    ASSISTANT_ID = 'YOUR_ASSISTANT_ID_HERE' 
    # Replace with your OpenAI API Key
    client = OpenAI(api_key="YOUR_OPENAI_API_KEY_HERE") 
    ```

### Running Locally

1.  **Clone the repository:**
    ```sh
    git clone https://github.com/mohsinmshabbir/pdpl-gpt-assistant.git
    cd pdpl-gpt-assistant
    ```

2.  **Install dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

3.  **Run the Streamlit application:**
    ```sh
    streamlit run chatbot_assistant.py
    ```

    The application will be available at `http://localhost:8501`.

### Running with Docker

1.  **Clone the repository:**
    ```sh
    git clone https://github.com/mohsinmshabbir/pdpl-gpt-assistant.git
    cd pdpl-gpt-assistant
    ```

2.  **Build the Docker image:**
    ```sh
    docker build -t pdpl-gpt-assistant .
    ```

3.  **Run the Docker container:**
    ```sh
    docker run -p 8501:8501 pdpl-gpt-assistant
    ```

    Access the application in your browser at `http://localhost:8501`.

## File Descriptions

*   `chatbot_assistant.py`: The main Streamlit application file that creates the UI and handles communication with the OpenAI API.
*   `new_chatbot.py`: An alternative version of the chatbot with experimental message editing functionality.
*   `instructions_for_assistant.txt`: A text file containing the core instructions, persona, and response guidelines for the OpenAI Assistant.
*   `requirements.txt`: A list of Python packages required to run the application.
*   `dockerfile`: Instructions for building a Docker container to run the application in an isolated environment.
