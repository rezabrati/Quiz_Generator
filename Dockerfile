# Use an official Python runtime as the base image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install dependencies listed in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port your app will run on (Streamlit default is 8501)
EXPOSE 8501

# Run the Streamlit app
CMD ["streamlit", "run", "main.py"]

