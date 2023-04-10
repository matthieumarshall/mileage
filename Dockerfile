# Base image
FROM python:3.8

# Set the working directory
WORKDIR /app

# Copy the app files to the container
COPY . /app

# Install the necessary packages
RUN pip install --no-cache-dir -r requirements.txt

# Expose the app port
EXPOSE 8050

# Start the app
CMD ["python", "app.py"]
