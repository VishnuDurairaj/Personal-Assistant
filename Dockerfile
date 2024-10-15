# Use the official Python 3.12 image from Docker Hub
FROM python:3.12

# Set the working directory
WORKDIR /app

# Copy the requirements file into the working directory
COPY requirements.txt /app/

# Install dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . /app

# Expose port 8088 for the Chainlit app
EXPOSE 8088

# Start the Chainlit application on port 8088
CMD ["chainlit", "run", "assistant.py", "--port", "8088"]
