# Use the official Python 3.12.5 image from the Docker Hub
FROM python:3.12.5-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file and the application code
COPY requirements.txt ./
COPY chatbot_assistant.py ./
COPY instructions_for_assistant.txt ./

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port the app runs on
EXPOSE 8501

# Command to run the application
CMD ["streamlit", "run", "chatbot_assistant.py", "--server.port=8501", "--server.address=0.0.0.0"]