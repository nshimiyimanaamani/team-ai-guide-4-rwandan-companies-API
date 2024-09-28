# Use the official Python image from the Docker Hub
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /home/app

# Copy the requirements.txt into the container
COPY requirements.txt .

# Install any Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire current directory into the container
COPY . .

# Set environment variables (if you have them)
# You can also pass these in from the docker-compose.yml or through CLI
# ENV VAR_NAME=value
ENV PINE_CONE_API_KEY=f79e423e-a302-4df2-9a21-7f31ddc454d8

# Expose the port Flask will run on
EXPOSE 5000

# Command to run the Flask app
CMD ["python", "app.py"]
