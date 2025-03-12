# Use an latest Python image
FROM python:3

# Set the working directory inside the container
WORKDIR /usr/src/app

# Copy requirements.txt to root
COPY requirements.txt ./

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container
COPY . ./

# Expose the port the service runs on
EXPOSE 8001

# Command to run the ASR API
CMD ["uvicorn", "asr_api:app", "--host", "0.0.0.0", "--port", "8001"]