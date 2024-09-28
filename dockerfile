FROM python:3.10-slim

WORKDIR /home/app

# Copy the requirements.txt into the container
COPY requirements.txt .

# Install any Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire current directory into the container
COPY . .


EXPOSE 5000

# Command to run the Flask app
CMD ["python", "app.py"]
